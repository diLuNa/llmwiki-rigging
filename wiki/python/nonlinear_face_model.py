"""
Nonlinear face model: (identity + jaw SE(3) + muscle stretch ratios) → mesh vertices.

Replaces the linear PCA decode with a fully nonlinear neural architecture:

    neutral_mesh  →  IdentityEncoder  →  z_id  (64-dim, per-subject)
    jaw SE(3) (7) + muscle_ratios (M)  →  expression input
    concat(z_id, jaw, muscles)  →  MLPDecoder  →  vertex_deltas  (V, 3)
    posed_mesh  =  neutral_mesh  +  vertex_deltas

Multi-subject: the identity encoder disentangles who from what expression —
the same jaw+muscle input synthesizes correct shapes for different characters.

Two decoder variants:
  MLPDecoder      — pure MLP, ~12M params, works for any topology
  UVConvDecoder   — MLP trunk → UV-space conv upsample, better spatial coherence
                    (requires per-vertex UV coordinates, single-island UV layout)

Requirements
------------
    torch >= 2.0
    numpy, scipy, scikit-learn, h5py
    pip install torch numpy scipy scikit-learn h5py
"""

from __future__ import annotations
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from scipy.spatial.transform import Rotation
from pathlib import Path

try:
    import h5py
    _H5 = True
except ImportError:
    _H5 = False
    print("h5py not found — FaceDataset will only work with numpy arrays. pip install h5py")


# =============================================================================
# Rotation utilities
# =============================================================================

def rotation_to_6d(R: torch.Tensor) -> torch.Tensor:
    """
    Convert rotation matrix (*, 3, 3) to 6D continuous representation (*, 6).
    Uses first two columns; decoder reconstructs R via Gram-Schmidt.
    Preferred over quaternion: no antipodal ambiguity, continuous everywhere.
    """
    return R[..., :, :2].reshape(*R.shape[:-2], 6)


def rotation_from_6d(x: torch.Tensor) -> torch.Tensor:
    """Recover SO(3) matrix from 6D representation (*, 6) → (*, 3, 3)."""
    a1, a2 = x[..., :3], x[..., 3:]
    b1 = F.normalize(a1, dim=-1)
    b2 = F.normalize(a2 - (b1 * a2).sum(-1, keepdim=True) * b1, dim=-1)
    b3 = torch.cross(b1, b2, dim=-1)
    return torch.stack([b1, b2, b3], dim=-1)  # (*, 3, 3)


def np_jaw_to_tensor(R: np.ndarray, t: np.ndarray) -> np.ndarray:
    """SE(3) → 9-dim vector: [6D rotation (6) | translation (3)]."""
    r6d = R[:, :2].T.flatten()  # first two columns, row-major → (6,)
    return np.concatenate([r6d, t]).astype(np.float32)


# =============================================================================
# Identity encoder
# =============================================================================

class IdentityEncoder(nn.Module):
    """
    Encodes a neutral mesh (V, 3) → identity code z_id (latent_dim,).

    For small datasets (<~200 subjects), a simpler alternative is pre-computed
    PCA of neutral meshes — call `pca_identity_encoder()` instead of training this.

    Architecture: MLP with residual skip; processes flattened vertex positions.
    Input is centered + normalized by per-vertex std before encoding.
    """

    def __init__(self, n_verts: int, latent_dim: int = 64, hidden: int = 512):
        super().__init__()
        in_dim = n_verts * 3
        self.norm_mean = nn.Parameter(torch.zeros(in_dim), requires_grad=False)
        self.norm_std  = nn.Parameter(torch.ones(in_dim),  requires_grad=False)
        self.enc = nn.Sequential(
            nn.Linear(in_dim, hidden),     nn.LayerNorm(hidden), nn.GELU(),
            nn.Linear(hidden, hidden),     nn.LayerNorm(hidden), nn.GELU(),
            nn.Linear(hidden, latent_dim),
        )

    def set_normalization(self, neutral_meshes: np.ndarray):
        """neutral_meshes: (N_subjects, V*3) — call once before training."""
        m = torch.from_numpy(neutral_meshes.astype(np.float32))
        self.norm_mean.data = m.mean(0)
        self.norm_std.data  = m.std(0).clamp(min=1e-6)

    def forward(self, neutral_flat: torch.Tensor) -> torch.Tensor:
        """neutral_flat: (B, V*3) → z_id: (B, latent_dim)."""
        x = (neutral_flat - self.norm_mean) / self.norm_std
        return self.enc(x)


def pca_identity_encoder(neutral_meshes: np.ndarray, n_components: int = 64):
    """
    Lightweight alternative to IdentityEncoder for small datasets.
    Returns (pca_object, z_id_matrix) where z_id_matrix is (N, n_components).

    At inference: z_id = pca.transform(neutral_flat[None])
    """
    from sklearn.decomposition import PCA
    flat = neutral_meshes.reshape(len(neutral_meshes), -1)
    pca = PCA(n_components=n_components, random_state=0)
    z_ids = pca.fit_transform(flat).astype(np.float32)
    print(f"Identity PCA: {n_components} components, "
          f"explained variance = {pca.explained_variance_ratio_.sum():.3f}")
    return pca, z_ids


# =============================================================================
# MLP decoder (topology-agnostic)
# =============================================================================

class MLPDecoder(nn.Module):
    """
    (z_id + jaw_6d + muscle_ratios) → vertex_deltas (V, 3).

    Input dim  : latent_dim + 9 (6d rot + trans) + n_muscles
    Output dim : n_verts * 3
    """

    def __init__(
        self,
        latent_dim: int,
        n_muscles: int,
        n_verts: int,
        hidden: int = 512,
    ):
        super().__init__()
        in_dim = latent_dim + 9 + n_muscles  # 9 = 6D rot + 3 trans
        self.n_verts = n_verts
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),      nn.LayerNorm(hidden),      nn.GELU(),
            nn.Linear(hidden, hidden),      nn.LayerNorm(hidden),      nn.GELU(),
            nn.Linear(hidden, hidden * 2),  nn.LayerNorm(hidden * 2),  nn.GELU(),
            nn.Linear(hidden * 2, hidden * 4), nn.LayerNorm(hidden * 4), nn.GELU(),
            nn.Linear(hidden * 4, n_verts * 3),  # linear output — deltas are signed
        )

    def forward(self, z_id, jaw_9d, muscles):
        """
        z_id    : (B, latent_dim)
        jaw_9d  : (B, 9)    — [6D rotation | translation]
        muscles : (B, M)    — zero-mean normalized stretch ratios
        Returns vertex_deltas (B, V, 3).
        """
        x = torch.cat([z_id, jaw_9d, muscles], dim=-1)
        return self.net(x).reshape(-1, self.n_verts, 3)


# =============================================================================
# UV-space convolutional decoder (higher spatial coherence, optional)
# =============================================================================

class UVConvDecoder(nn.Module):
    """
    MLP trunk → reshape to (C, H, H) feature map → Conv2d upsample → 256×256
    delta UV map → bilinear sample at per-vertex UV coords → (V, 3) deltas.

    Requires:
      uv_coords : (V, 2) in [-1, 1], pre-baked per-vertex UV coordinates
                  (single-island UV layout; seam in low-deformation region)

    Why UV space:
      Regular grid → valid convolutional inductive bias.
      Same UV pixel = same semantic face region across all subjects.
      Bilinear sampling handles vertex density variation without special indexing.
    """

    def __init__(
        self,
        latent_dim: int,
        n_muscles: int,
        n_verts: int,
        uv_coords: np.ndarray,      # (V, 2) in [-1, 1]
        trunk_hidden: int = 512,
        map_size: int = 256,
        base_channels: int = 64,
    ):
        super().__init__()
        in_dim = latent_dim + 9 + n_muscles
        self.n_verts = n_verts
        self.map_size = map_size

        # Trunk: → spatial feature seed
        seed_h = map_size // 16
        self.trunk = nn.Sequential(
            nn.Linear(in_dim, trunk_hidden),      nn.LayerNorm(trunk_hidden), nn.GELU(),
            nn.Linear(trunk_hidden, trunk_hidden), nn.LayerNorm(trunk_hidden), nn.GELU(),
            nn.Linear(trunk_hidden, trunk_hidden * 4 * seed_h * seed_h),
        )
        self.seed_h = seed_h
        self.seed_c = trunk_hidden * 4

        # Upsampler: 4 × 2× upsample blocks → map_size × map_size
        def upsample_block(cin, cout):
            return nn.Sequential(
                nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                nn.Conv2d(cin, cout, 3, padding=1), nn.GELU(),
                nn.Conv2d(cout, cout, 3, padding=1), nn.GELU(),
            )

        c = self.seed_c
        self.ups = nn.ModuleList()
        for _ in range(4):
            self.ups.append(upsample_block(c, max(c // 2, base_channels)))
            c = max(c // 2, base_channels)
        self.head = nn.Conv2d(c, 3, 1)  # → (3, H, W) delta map

        # Register UV coords as a buffer (not a parameter)
        uv = torch.from_numpy(uv_coords.astype(np.float32))  # (V, 2)
        self.register_buffer("uv_coords", uv.unsqueeze(0).unsqueeze(0))  # (1, 1, V, 2)

    def forward(self, z_id, jaw_9d, muscles):
        B = z_id.shape[0]
        x = torch.cat([z_id, jaw_9d, muscles], dim=-1)
        seed = self.trunk(x).reshape(B, self.seed_c, self.seed_h, self.seed_h)
        feat = seed
        for up in self.ups:
            feat = up(feat)
        delta_map = self.head(feat)  # (B, 3, H, W)

        # Sample per-vertex deltas from the UV map
        grid = self.uv_coords.expand(B, -1, -1, -1)  # (B, 1, V, 2)
        deltas = F.grid_sample(
            delta_map, grid,
            mode='bilinear', padding_mode='border', align_corners=True,
        )  # (B, 3, 1, V)
        return deltas.squeeze(2).permute(0, 2, 1)  # (B, V, 3)


# =============================================================================
# Full model wrapper
# =============================================================================

class NonlinearFaceModel(nn.Module):
    """
    Full model: IdentityEncoder + Decoder.

    Usage (training):
        model = NonlinearFaceModel(...)
        delta = model(neutral_flat, jaw_9d, muscles)
        posed  = neutral_verts + delta

    Usage (inference, fixed identity):
        z_id = model.encode_identity(neutral_flat)  # once per character
        delta = model.decode(z_id, jaw_9d, muscles)
        posed  = neutral_verts + delta
    """

    def __init__(
        self,
        n_verts: int,
        n_muscles: int,
        latent_dim: int = 64,
        decoder: str = "mlp",      # "mlp" | "uvconv"
        hidden: int = 512,
        uv_coords: np.ndarray | None = None,
    ):
        super().__init__()
        self.identity_encoder = IdentityEncoder(n_verts, latent_dim, hidden)

        if decoder == "uvconv":
            assert uv_coords is not None, "uv_coords required for UVConvDecoder"
            self.decoder = UVConvDecoder(latent_dim, n_muscles, n_verts, uv_coords, hidden)
        else:
            self.decoder = MLPDecoder(latent_dim, n_muscles, n_verts, hidden)

    def encode_identity(self, neutral_flat: torch.Tensor) -> torch.Tensor:
        return self.identity_encoder(neutral_flat)

    def decode(
        self,
        z_id: torch.Tensor,
        jaw_9d: torch.Tensor,
        muscles: torch.Tensor,
    ) -> torch.Tensor:
        return self.decoder(z_id, jaw_9d, muscles)

    def forward(
        self,
        neutral_flat: torch.Tensor,  # (B, V*3)
        jaw_9d: torch.Tensor,        # (B, 9)
        muscles: torch.Tensor,       # (B, M)
    ) -> torch.Tensor:               # returns vertex_deltas (B, V, 3)
        z_id = self.encode_identity(neutral_flat)
        return self.decode(z_id, jaw_9d, muscles)


# =============================================================================
# Loss functions
# =============================================================================

def laplacian_loss(
    pred_deltas: torch.Tensor,   # (B, V, 3)
    L: torch.Tensor,             # (V, V) sparse or dense cotangent Laplacian
) -> torch.Tensor:
    """
    Penalise high-frequency surface noise.
    L @ deltas should be close to zero for smooth deformations.
    """
    # L: (V, V), pred_deltas: (B, V, 3)
    Lv = torch.einsum("ij,bjk->bik", L, pred_deltas)  # (B, V, 3)
    return Lv.pow(2).mean()


def neutral_anchor_loss(
    model: NonlinearFaceModel,
    neutral_flat: torch.Tensor,  # (B, V*3)
    device: str,
) -> torch.Tensor:
    """
    Force decoder(z_id, zero_jaw, zero_muscles) ≈ 0.
    Prevents the network from encoding expression information in z_id.
    """
    B = neutral_flat.shape[0]
    zero_jaw     = torch.zeros(B, 9,  device=device)
    zero_muscles = torch.zeros(B, model.decoder.n_verts if hasattr(model.decoder, 'n_verts') else 1, device=device)
    # Get muscle dim from model
    if isinstance(model.decoder, MLPDecoder):
        M = model.decoder.net[0].in_features - model.identity_encoder.enc[-1].out_features - 9
    else:
        M = model.decoder.trunk[0].in_features - model.identity_encoder.enc[-1].out_features - 9
    zero_muscles = torch.zeros(B, M, device=device)

    with torch.no_grad():
        z_id = model.encode_identity(neutral_flat)
    delta_at_neutral = model.decode(z_id, zero_jaw, zero_muscles)
    return delta_at_neutral.pow(2).mean()


def build_uniform_laplacian(faces: np.ndarray, n_verts: int) -> torch.Tensor:
    """
    Build a uniform-weight Laplacian matrix from face indices.
    faces: (F, 3) triangle indices.
    Returns (V, V) dense tensor; multiply by vertex positions to get Laplacian deviation.
    """
    import scipy.sparse as sp
    rows, cols = [], []
    for tri in faces:
        for i in range(3):
            a, b = tri[i], tri[(i + 1) % 3]
            rows += [a, b]; cols += [b, a]
    data = np.ones(len(rows))
    A = sp.csr_matrix((data, (rows, cols)), shape=(n_verts, n_verts))
    deg = np.array(A.sum(1)).flatten()
    D_inv = sp.diags(1.0 / np.maximum(deg, 1))
    L = sp.eye(n_verts) - D_inv @ A
    return torch.from_numpy(L.toarray().astype(np.float32))


# =============================================================================
# Dataset
# =============================================================================

class FaceDataset(Dataset):
    """
    HDF5-backed dataset for multi-subject face model training.

    Expected HDF5 layout:
        /subjects/<subject_id>/neutral_flat   (V*3,)  float32
        /subjects/<subject_id>/skull_scale    ()      float32
        /subjects/<subject_id>/z_id           (latent_dim,)  float32  [optional, pre-computed]
        /subjects/<subject_id>/poses/
            jaw_9d          (N_poses, 9)    float32
            muscle_ratios   (N_poses, M)    float32
            delta_verts     (N_poses, V*3)  float32

    At runtime, muscle_ratios are zero-mean normalized using dataset statistics.
    Jaw translation is normalized by per-subject skull_scale.
    """

    def __init__(
        self,
        h5_path: str,
        muscle_mean: np.ndarray | None = None,
        muscle_std:  np.ndarray | None = None,
        precomputed_z_ids: dict | None = None,  # {subject_id: z_id array}
    ):
        assert _H5, "h5py required for FaceDataset"
        self.h5_path = h5_path
        self.precomputed_z_ids = precomputed_z_ids or {}
        self._index = []  # list of (subject_id, pose_idx)
        with h5py.File(h5_path, "r") as f:
            for sid in f["subjects"]:
                n_poses = f[f"subjects/{sid}/poses/delta_verts"].shape[0]
                self._index.extend([(sid, i) for i in range(n_poses)])

        self.muscle_mean = muscle_mean
        self.muscle_std  = muscle_std

    @classmethod
    def compute_muscle_stats(cls, h5_path: str) -> tuple[np.ndarray, np.ndarray]:
        """Compute per-muscle mean and std across all poses for normalization."""
        all_ratios = []
        with h5py.File(h5_path, "r") as f:
            for sid in f["subjects"]:
                all_ratios.append(f[f"subjects/{sid}/poses/muscle_ratios"][:])
        all_ratios = np.concatenate(all_ratios, axis=0)
        return all_ratios.mean(0), all_ratios.std(0) + 1e-6

    def __len__(self): return len(self._index)

    def __getitem__(self, idx):
        sid, pose_i = self._index[idx]
        with h5py.File(self.h5_path, "r") as f:
            grp = f[f"subjects/{sid}"]
            neutral_flat = grp["neutral_flat"][:]              # (V*3,)
            skull_scale  = float(grp["skull_scale"][()])
            jaw_9d       = grp[f"poses/jaw_9d"][pose_i]       # (9,)
            muscles      = grp[f"poses/muscle_ratios"][pose_i] # (M,)
            delta_flat   = grp[f"poses/delta_verts"][pose_i]  # (V*3,)

        # Normalize jaw translation by skull scale
        jaw_9d = jaw_9d.copy()
        jaw_9d[6:] /= skull_scale

        # Zero-mean normalize muscle ratios
        if self.muscle_mean is not None:
            muscles = (muscles - self.muscle_mean) / self.muscle_std

        # Pre-computed z_id (e.g. from PCA identity encoder)
        if sid in self.precomputed_z_ids:
            z_id = self.precomputed_z_ids[sid].astype(np.float32)
        else:
            z_id = np.zeros(1, dtype=np.float32)  # placeholder; encoder used at train time

        return {
            "neutral_flat": torch.from_numpy(neutral_flat),
            "z_id":         torch.from_numpy(z_id),
            "jaw_9d":       torch.from_numpy(jaw_9d),
            "muscles":      torch.from_numpy(muscles),
            "delta_verts":  torch.from_numpy(delta_flat.reshape(-1, 3)),
        }


class NumpyFaceDataset(Dataset):
    """
    Lighter alternative to FaceDataset for single-subject use with numpy arrays.
    No HDF5 required.
    """

    def __init__(
        self,
        neutral_flat: np.ndarray,      # (V*3,) — same neutral for all poses
        jaw_9d: np.ndarray,            # (N, 9)
        muscle_ratios: np.ndarray,     # (N, M)
        delta_verts: np.ndarray,       # (N, V, 3) or (N, V*3)
        z_id: np.ndarray | None = None,  # (latent_dim,) — pre-computed, optional
    ):
        self.neutral_flat = torch.from_numpy(neutral_flat.astype(np.float32))
        self.jaw_9d       = torch.from_numpy(jaw_9d.astype(np.float32))
        self.muscles      = torch.from_numpy(muscle_ratios.astype(np.float32))
        N = len(jaw_9d)
        V3 = delta_verts.reshape(N, -1, 3).shape[1]
        self.delta_verts  = torch.from_numpy(delta_verts.reshape(N, V3, 3).astype(np.float32))
        self.z_id         = torch.from_numpy(z_id.astype(np.float32)) if z_id is not None else None

    def __len__(self): return len(self.jaw_9d)

    def __getitem__(self, idx):
        item = {
            "neutral_flat": self.neutral_flat,
            "jaw_9d":       self.jaw_9d[idx],
            "muscles":      self.muscles[idx],
            "delta_verts":  self.delta_verts[idx],
        }
        if self.z_id is not None:
            item["z_id"] = self.z_id
        return item


# =============================================================================
# Trainer
# =============================================================================

class FaceModelTrainer:
    """
    Training loop for NonlinearFaceModel.

    Losses (weighted sum):
      vertex_l1   : primary reconstruction — L1 per-vertex position error
      laplacian   : Laplacian smoothness — penalises high-frequency surface noise
      neutral_anc : neutral anchor — decoder(z_id, 0, 0) ≈ 0
    """

    def __init__(
        self,
        model: NonlinearFaceModel,
        lr: float = 1e-3,
        weight_decay: float = 1e-5,
        w_laplacian: float = 0.1,
        w_neutral: float = 0.01,
        laplacian_matrix: torch.Tensor | None = None,
        device: str = "cpu",
    ):
        self.model    = model.to(device)
        self.device   = device
        self.w_lap    = w_laplacian
        self.w_neu    = w_neutral
        self.L        = laplacian_matrix.to(device) if laplacian_matrix is not None else None

        self.opt   = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
        self.sched = torch.optim.lr_scheduler.CosineAnnealingLR(self.opt, T_max=100)

    def _loss(self, batch):
        neutral = batch["neutral_flat"].to(self.device)
        jaw     = batch["jaw_9d"].to(self.device)
        muscles = batch["muscles"].to(self.device)
        target  = batch["delta_verts"].to(self.device)  # (B, V, 3)

        if "z_id" in batch and batch["z_id"].shape[-1] > 1:
            z_id   = batch["z_id"].to(self.device)
            pred   = self.model.decode(z_id, jaw, muscles)
        else:
            pred   = self.model(neutral, jaw, muscles)

        l_vert = F.l1_loss(pred, target)
        l_lap  = laplacian_loss(pred, self.L) if self.L is not None else torch.tensor(0.0)
        l_neu  = neutral_anchor_loss(self.model, neutral, self.device)

        return l_vert + self.w_lap * l_lap + self.w_neu * l_neu, {
            "vert": l_vert.item(),
            "lap":  l_lap.item() if self.L is not None else 0.0,
            "neu":  l_neu.item(),
        }

    def train_epoch(self, loader: DataLoader) -> dict:
        self.model.train()
        totals = {"vert": 0.0, "lap": 0.0, "neu": 0.0}
        n = 0
        for batch in loader:
            loss, parts = self._loss(batch)
            self.opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.opt.step()
            for k, v in parts.items(): totals[k] += v
            n += 1
        self.sched.step()
        return {k: v / n for k, v in totals.items()}

    @torch.no_grad()
    def val_epoch(self, loader: DataLoader) -> dict:
        self.model.eval()
        totals = {"vert": 0.0, "lap": 0.0, "neu": 0.0}
        n = 0
        for batch in loader:
            _, parts = self._loss(batch)
            for k, v in parts.items(): totals[k] += v
            n += 1
        return {k: v / n for k, v in totals.items()}

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader | None = None,
        epochs: int = 100,
        print_every: int = 10,
        save_path: str | None = None,
    ):
        best_val = float("inf")
        for epoch in range(1, epochs + 1):
            tr = self.train_epoch(train_loader)
            line = (f"[{epoch:3d}/{epochs}] train  vert={tr['vert']:.5f} "
                    f"lap={tr['lap']:.5f} neu={tr['neu']:.5f}")
            if val_loader is not None:
                vl = self.val_epoch(val_loader)
                line += (f"   val  vert={vl['vert']:.5f}")
                if vl["vert"] < best_val and save_path:
                    best_val = vl["vert"]
                    torch.save({
                        "epoch": epoch,
                        "model_state": self.model.state_dict(),
                        "val_vert": best_val,
                    }, save_path)
            if epoch % print_every == 0:
                print(line)
        return self


# =============================================================================
# Inference
# =============================================================================

@torch.no_grad()
def synthesize(
    neutral_verts: np.ndarray,    # (V, 3) neutral mesh for this identity
    jaw_R: np.ndarray,            # (3, 3) rotation matrix, skull-relative
    jaw_t: np.ndarray,            # (3,)   translation (un-normalized; provide skull_scale)
    muscle_ratios: np.ndarray,    # (M,)   stretch ratios (raw, un-normalized)
    model: NonlinearFaceModel,
    muscle_mean: np.ndarray,
    muscle_std:  np.ndarray,
    skull_scale: float = 1.0,
    device: str = "cpu",
    z_id: np.ndarray | None = None,  # pre-cached z_id; if None, computed from neutral
) -> np.ndarray:
    """
    Synthesize a head mesh given jaw SE(3) and muscle stretch ratios.

    Returns posed vertex positions (V, 3).
    """
    model.eval().to(device)
    V = neutral_verts.shape[0]

    if z_id is None:
        neutral_flat = torch.from_numpy(neutral_verts.flatten().astype(np.float32)).unsqueeze(0).to(device)
        z_id_t = model.encode_identity(neutral_flat)
    else:
        z_id_t = torch.from_numpy(z_id.astype(np.float32)).unsqueeze(0).to(device)

    # Build jaw 9d: 6D rotation + normalized translation
    jaw_9d = np.concatenate([jaw_R[:, :2].T.flatten(), jaw_t / skull_scale]).astype(np.float32)
    jaw_t_ = torch.from_numpy(jaw_9d).unsqueeze(0).to(device)

    # Normalize muscles
    muscles_norm = (muscle_ratios - muscle_mean) / muscle_std
    muscles_t = torch.from_numpy(muscles_norm.astype(np.float32)).unsqueeze(0).to(device)

    delta = model.decode(z_id_t, jaw_t_, muscles_t).cpu().numpy()[0]  # (V, 3)
    return neutral_verts + delta


def cache_identity(
    neutral_verts: np.ndarray,
    model: NonlinearFaceModel,
    device: str = "cpu",
) -> np.ndarray:
    """Pre-compute z_id for a character once; pass to synthesize() to skip re-encoding."""
    model.eval().to(device)
    flat = torch.from_numpy(neutral_verts.flatten().astype(np.float32)).unsqueeze(0).to(device)
    with torch.no_grad():
        z_id = model.encode_identity(flat).cpu().numpy()[0]
    return z_id


# =============================================================================
# HDF5 export helper (for converting PCA-derived training data)
# =============================================================================

def export_to_hdf5(
    h5_path: str,
    subject_id: str,
    neutral_flat: np.ndarray,       # (V*3,)
    skull_scale: float,
    jaw_9d: np.ndarray,             # (N, 9)  pre-computed via np_jaw_to_tensor
    muscle_ratios: np.ndarray,      # (N, M)
    delta_verts: np.ndarray,        # (N, V, 3) or (N, V*3)
    mode: str = "a",                # "w" to overwrite, "a" to append
):
    """Write one subject's data to an HDF5 file."""
    assert _H5, "pip install h5py"
    N = len(jaw_9d)
    delta_flat = delta_verts.reshape(N, -1).astype(np.float32)
    with h5py.File(h5_path, mode) as f:
        grp = f.require_group(f"subjects/{subject_id}/poses")
        grp.parent["neutral_flat"] = neutral_flat.astype(np.float32)
        grp.parent["skull_scale"]  = np.float32(skull_scale)
        for k, v in [("jaw_9d", jaw_9d), ("muscle_ratios", muscle_ratios), ("delta_verts", delta_flat)]:
            if k in grp:
                del grp[k]
            grp.create_dataset(k, data=v.astype(np.float32), compression="lzf")
    print(f"Exported {N} poses for subject '{subject_id}' → {h5_path}")


# =============================================================================
# Demo / entry point
# =============================================================================

if __name__ == "__main__":
    import warnings; warnings.filterwarnings("ignore")

    rng  = np.random.default_rng(0)
    N, V, M = 8_000, 5023, 11  # poses, verts, muscles
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {DEVICE}")

    # ── Synthetic data ─────────────────────────────────────────────────────
    neutral_verts = rng.standard_normal((V, 3)).astype(np.float32)
    neutral_flat  = neutral_verts.flatten()

    # Simulate 24 expression clusters with jaw + muscle structure
    n_proto = 24
    jaw_proto    = rng.standard_normal((n_proto, 9)).astype(np.float32) * 0.3
    muscle_proto = rng.standard_normal((n_proto, M)).astype(np.float32) * 0.2
    c_ids = rng.integers(0, n_proto, N)

    jaw_9d        = jaw_proto[c_ids] + rng.standard_normal((N, 9)).astype(np.float32)  * 0.05
    muscle_ratios = muscle_proto[c_ids] + rng.standard_normal((N, M)).astype(np.float32) * 0.02

    # Simple linear ground-truth (for demo reconstruction sanity check)
    W = rng.standard_normal((9 + M, V * 3)).astype(np.float32) * 0.001
    controls = np.concatenate([jaw_9d, muscle_ratios], axis=1)
    delta_verts = (controls @ W).reshape(N, V, 3).astype(np.float32)

    # Normalize muscles
    muscle_mean = muscle_ratios.mean(0)
    muscle_std  = muscle_ratios.std(0) + 1e-6
    muscle_norm = (muscle_ratios - muscle_mean) / muscle_std

    # ── Dataset and DataLoader ──────────────────────────────────────────────
    split = int(0.9 * N)
    train_ds = NumpyFaceDataset(neutral_flat, jaw_9d[:split],    muscle_norm[:split],    delta_verts[:split])
    val_ds   = NumpyFaceDataset(neutral_flat, jaw_9d[split:],    muscle_norm[split:],    delta_verts[split:])
    train_dl = DataLoader(train_ds, batch_size=128, shuffle=True,  num_workers=0)
    val_dl   = DataLoader(val_ds,   batch_size=256, shuffle=False, num_workers=0)

    # ── Model ──────────────────────────────────────────────────────────────
    model = NonlinearFaceModel(
        n_verts=V,
        n_muscles=M,
        latent_dim=64,
        decoder="mlp",
        hidden=256,   # use 512+ for production
    )
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Model params: {total_params:,}")

    # ── Train ──────────────────────────────────────────────────────────────
    trainer = FaceModelTrainer(
        model,
        lr=1e-3,
        w_laplacian=0.0,   # set > 0 and pass L when mesh faces are available
        w_neutral=0.01,
        device=DEVICE,
    )
    trainer.fit(train_dl, val_dl, epochs=30, print_every=5)

    # ── Synthesize ─────────────────────────────────────────────────────────
    from scipy.spatial.transform import Rotation as R_
    jaw_R = R_.from_euler("xyz", [0.05, 0.02, 0.0]).as_matrix()
    jaw_t = np.array([0.0, -0.5, 0.1], dtype=np.float32)
    test_muscles = np.zeros(M, dtype=np.float32)
    test_muscles[0] = 0.85   # zygomaticus_major_L contracted (smile)

    posed = synthesize(
        neutral_verts, jaw_R, jaw_t, test_muscles,
        model, muscle_mean, muscle_std,
        skull_scale=1.0, device=DEVICE,
    )
    print(f"Synthesized mesh shape: {posed.shape}, "
          f"max delta: {np.abs(posed - neutral_verts).max():.4f}")

    # ── PCA identity encoder (alternative to IdentityEncoder, small dataset) ─
    n_subjects = 10
    neutral_meshes = rng.standard_normal((n_subjects, V * 3)).astype(np.float32)
    pca, z_ids = pca_identity_encoder(neutral_meshes, n_components=64)
    print(f"PCA identity codes: {z_ids.shape}")
