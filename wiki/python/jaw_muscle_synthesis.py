"""
Jaw + muscle driven face mesh synthesis from a PCA expression model.

Given 100k animated poses (each: 382 PCA expression coefficients), plus the ability
to decode to vertex positions and extract jaw SE(3) + muscle stretch ratios, this
module provides four synthesis approaches:

  Option A  — Linear regression  (jaw+muscles → expression params)
  Option B  — K-NN blending      (nearest poses in jaw+muscle space)
  Option C  — MLP decoder        (jaw+muscles → mesh vertex deltas)
  Option D  — Houdini Python SOP (KNN query from live rig controls)

Inputs assumed
--------------
expression_params : (N, 382)  PCA expression coefficients for N training poses
pca_basis         : (382, V*3) decoder matrix  (expression_params @ pca_basis + mean_face = verts)
mean_face         : (V*3,)     flattened mean face vertices
jaw_mask          : (K,)       vertex indices covering the mandible/jaw bone
muscle_attachments: list of lists of np.ndarray — per muscle: list of vertex-index arrays
                    (one array per control point along the polyline; averaged to centroid)
"""

import numpy as np
from scipy.spatial.transform import Rotation
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.neighbors import NearestNeighbors

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    _TORCH = True
except ImportError:
    _TORCH = False
    print("PyTorch not found — Option C (MLP) unavailable. pip install torch")


# ---------------------------------------------------------------------------
# FLAME muscle attachment definitions (5023-vertex topology approximations)
# ---------------------------------------------------------------------------

FLAME_MUSCLE_ATTACHMENTS = {
    "zygomaticus_major_L": [np.arange(1900, 1940), np.arange(3050, 3070)],
    "zygomaticus_major_R": [np.arange(2060, 2100), np.arange(3080, 3100)],
    "orbicularis_oris":    [np.arange(3440, 3480), np.arange(3480, 3560)],
    "levator_labii_L":     [np.arange(2140, 2180), np.arange(3100, 3130)],
    "levator_labii_R":     [np.arange(2200, 2240), np.arange(3200, 3230)],
    "depressor_anguli_L":  [np.arange(600,  640),  np.arange(3000, 3030)],
    "depressor_anguli_R":  [np.arange(640,  680),  np.arange(3060, 3090)],
    "masseter_L":          [np.arange(1850, 1900), np.arange(400,  450)],
    "masseter_R":          [np.arange(2020, 2060), np.arange(450,  500)],
    "frontalis_L":         [np.arange(1320, 1400), np.arange(1400, 1480)],
    "frontalis_R":         [np.arange(1560, 1640), np.arange(1480, 1560)],
}

FLAME_JAW_MASK = np.arange(400, 620)  # mandible region


# ---------------------------------------------------------------------------
# Jaw SE(3) extraction
# ---------------------------------------------------------------------------

def extract_jaw_se3(
    posed_verts: np.ndarray,
    neutral_verts: np.ndarray,
    jaw_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Fit SE(3) of mandible between posed and neutral mesh via SVD.
    Returns (R, t) such that posed[jaw] ≈ R @ neutral[jaw] + t.
    R: (3,3), t: (3,)
    """
    p = posed_verts[jaw_mask]
    n = neutral_verts[jaw_mask]
    pc, nc = p.mean(0), n.mean(0)
    H = (p - pc).T @ (n - nc)
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1
        R = Vt.T @ U.T
    return R, pc - R @ nc


def jaw_se3_to_vec(R: np.ndarray, t: np.ndarray) -> np.ndarray:
    """SE(3) → 7-dim vector [quat xyzw (4) | translation (3)]."""
    q = Rotation.from_matrix(R).as_quat()
    return np.concatenate([q, t]).astype(np.float32)


# ---------------------------------------------------------------------------
# Muscle stretch ratio
# ---------------------------------------------------------------------------

def polyline_length(points: np.ndarray) -> float:
    return float(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)))


def muscle_stretch_ratio(
    posed_verts: np.ndarray,
    neutral_verts: np.ndarray,
    attachment_indices: list,
) -> float:
    """
    Stretch ratio = current_length / rest_length.
    attachment_indices: list of vertex index arrays (one per control point).
    """
    def centroid(verts, idx):
        return verts[idx].mean(0)

    posed_pts   = np.stack([centroid(posed_verts,   i) for i in attachment_indices])
    neutral_pts = np.stack([centroid(neutral_verts, i) for i in attachment_indices])
    rest = polyline_length(neutral_pts)
    return polyline_length(posed_pts) / rest if rest > 1e-8 else 1.0


# ---------------------------------------------------------------------------
# Batch extraction: (N, 382) → (N, 7) jaw vecs + (N, M) muscle ratios
# ---------------------------------------------------------------------------

def extract_biomechanical_signals(
    expression_params: np.ndarray,
    pca_basis: np.ndarray,
    mean_face: np.ndarray,
    jaw_mask: np.ndarray | None = None,
    muscle_attachments: dict | None = None,
    batch_size: int = 2000,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Returns
    -------
    jaw_vecs      : (N, 7)   per-pose jaw SE(3) flat vector
    muscle_ratios : (N, M)   per-pose stretch ratio for each muscle
    muscle_names  : list[str]
    """
    if jaw_mask is None:
        jaw_mask = FLAME_JAW_MASK
    if muscle_attachments is None:
        muscle_attachments = FLAME_MUSCLE_ATTACHMENTS

    N = len(expression_params)
    V = mean_face.shape[0] // 3
    neutral = mean_face.reshape(V, 3)
    muscle_names = list(muscle_attachments.keys())
    M = len(muscle_names)

    jaw_vecs = np.empty((N, 7),  dtype=np.float32)
    muscle_ratios = np.empty((N, M), dtype=np.float32)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        batch = expression_params[start:end].astype(np.float32)
        verts_batch = (batch @ pca_basis.astype(np.float32) + mean_face).reshape(-1, V, 3)

        for bi, verts in enumerate(verts_batch):
            R, t = extract_jaw_se3(verts, neutral, jaw_mask)
            jaw_vecs[start + bi] = jaw_se3_to_vec(R, t)
            for mi, name in enumerate(muscle_names):
                att = muscle_attachments[name]
                muscle_ratios[start + bi, mi] = muscle_stretch_ratio(verts, neutral, att)

        if start % (batch_size * 10) == 0:
            print(f"  extracted {end:>7,} / {N:,}")

    return jaw_vecs, muscle_ratios, muscle_names


# ---------------------------------------------------------------------------
# Option A — Linear regression
# ---------------------------------------------------------------------------

def fit_linear(
    jaw_vecs: np.ndarray,
    muscle_ratios: np.ndarray,
    expression_params: np.ndarray,
    alpha: float = 1e-3,
) -> tuple:
    X = np.concatenate([jaw_vecs, muscle_ratios], axis=1).astype(np.float32)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    reg = Ridge(alpha=alpha)
    reg.fit(Xs, expression_params)
    print(f"[A] Linear R²: {reg.score(Xs, expression_params):.4f}")
    return reg, scaler


def synthesize_linear(
    jaw_vec, muscle_ratio,
    reg, scaler,
    pca_basis, mean_face,
) -> np.ndarray:
    x = np.concatenate([jaw_vec, muscle_ratio])[None]
    xs = scaler.transform(x)
    expr = reg.predict(xs)
    V = mean_face.shape[0] // 3
    return (expr @ pca_basis + mean_face).reshape(V, 3)


# ---------------------------------------------------------------------------
# Option B — K-NN blending
# ---------------------------------------------------------------------------

def build_knn(
    jaw_vecs: np.ndarray,
    muscle_ratios: np.ndarray,
    expression_params: np.ndarray,
    k: int = 8,
) -> tuple:
    X = np.concatenate([jaw_vecs, muscle_ratios], axis=1).astype(np.float32)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    knn = NearestNeighbors(n_neighbors=k, algorithm='ball_tree', n_jobs=-1)
    knn.fit(Xs)
    return knn, scaler, Xs, expression_params


def synthesize_knn(
    jaw_vec, muscle_ratio,
    knn, scaler, Xs, expression_params,
    pca_basis, mean_face,
    k: int = 8,
) -> np.ndarray:
    x = np.concatenate([jaw_vec, muscle_ratio])[None].astype(np.float32)
    xs = scaler.transform(x)
    dists, idxs = knn.kneighbors(xs, n_neighbors=k)
    dists, idxs = dists[0], idxs[0]
    sigma = dists.mean() + 1e-8
    w = np.exp(-0.5 * (dists / sigma) ** 2)
    w /= w.sum()
    expr = (w[:, None] * expression_params[idxs]).sum(0)
    V = mean_face.shape[0] // 3
    return (expr @ pca_basis + mean_face).reshape(V, 3)


# ---------------------------------------------------------------------------
# Option C — MLP decoder (requires PyTorch)
# ---------------------------------------------------------------------------

if _TORCH:
    class BiomechanicalDecoder(nn.Module):
        """(jaw_vec 7 + muscle_ratios M) → mesh delta (V, 3)."""
        def __init__(self, n_muscles: int, n_verts: int, hidden: int = 512):
            super().__init__()
            in_dim = 7 + n_muscles
            self.net = nn.Sequential(
                nn.Linear(in_dim, hidden),    nn.LayerNorm(hidden),    nn.GELU(),
                nn.Linear(hidden, hidden),    nn.LayerNorm(hidden),    nn.GELU(),
                nn.Linear(hidden, hidden * 2), nn.LayerNorm(hidden * 2), nn.GELU(),
                nn.Linear(hidden * 2, n_verts * 3),
            )
            self.n_verts = n_verts

        def forward(self, x):
            return self.net(x).reshape(x.shape[0], self.n_verts, 3)

    def train_mlp(
        jaw_vecs: np.ndarray,
        muscle_ratios: np.ndarray,
        expression_params: np.ndarray,
        pca_basis: np.ndarray,
        mean_face: np.ndarray,
        epochs: int = 50,
        batch_size: int = 256,
        lr: float = 1e-3,
        device: str = "cpu",
    ) -> tuple:
        N = len(expression_params)
        V = mean_face.shape[0] // 3
        neutral = mean_face.reshape(1, V, 3)

        print("[C] Pre-computing mesh deltas ...")
        all_deltas = np.empty((N, V, 3), dtype=np.float32)
        bs = 2000
        for s in range(0, N, bs):
            e = min(s + bs, N)
            verts = (expression_params[s:e].astype(np.float32) @ pca_basis.astype(np.float32) + mean_face)
            all_deltas[s:e] = verts.reshape(-1, V, 3) - neutral

        X = np.concatenate([jaw_vecs, muscle_ratios], axis=1).astype(np.float32)
        x_mean, x_std = X.mean(0), X.std(0) + 1e-8
        X = (X - x_mean) / x_std

        model = BiomechanicalDecoder(muscle_ratios.shape[1], V).to(device)
        opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)

        Xt = torch.from_numpy(X).to(device)
        Yt = torch.from_numpy(all_deltas).to(device)

        for epoch in range(epochs):
            idx = torch.randperm(N, device=device)
            total_loss = 0.0; n_steps = 0
            for s in range(0, N, batch_size):
                i = idx[s:s + batch_size]
                pred = model(Xt[i])
                loss = F.l1_loss(pred, Yt[i])
                opt.zero_grad(); loss.backward(); opt.step()
                total_loss += loss.item(); n_steps += 1
            sched.step()
            if epoch % 10 == 0:
                print(f"  Epoch {epoch:3d}  loss={total_loss/n_steps:.5f}")

        return model, x_mean, x_std

    def synthesize_mlp(
        jaw_vec, muscle_ratio,
        model, x_mean, x_std, mean_face,
        device: str = "cpu",
    ) -> np.ndarray:
        x = np.concatenate([jaw_vec, muscle_ratio]).astype(np.float32)
        x = (x - x_mean) / x_std
        with torch.no_grad():
            delta = model(torch.from_numpy(x[None]).to(device)).cpu().numpy()[0]
        V = mean_face.shape[0] // 3
        return mean_face.reshape(V, 3) + delta


# ---------------------------------------------------------------------------
# Correlation analysis — which muscles drive which expression components
# ---------------------------------------------------------------------------

def muscle_expression_correlation(
    jaw_vecs: np.ndarray,
    muscle_ratios: np.ndarray,
    expression_params: np.ndarray,
    muscle_names: list[str],
    top_n: int = 5,
):
    """
    Pearson correlation between each muscle stretch ratio and each expression PCA component.
    Prints the top-n expression components most correlated with each muscle.
    Returns corr_matrix: (M+7, 382).
    """
    X = np.concatenate([jaw_vecs, muscle_ratios], axis=1).astype(np.float64)
    Y = expression_params.astype(np.float64)
    # Normalize
    Xn = (X - X.mean(0)) / (X.std(0) + 1e-8)
    Yn = (Y - Y.mean(0)) / (Y.std(0) + 1e-8)
    corr = (Xn.T @ Yn) / len(X)  # (7+M, 382)

    feature_names = [f"jaw_{i}" for i in range(7)] + muscle_names
    for fi, fname in enumerate(feature_names):
        top_idx = np.argsort(np.abs(corr[fi]))[::-1][:top_n]
        top_r   = corr[fi][top_idx]
        print(f"{fname:30s}  →  PCA {list(top_idx)}  r={[f'{r:.3f}' for r in top_r]}")

    return corr


# ---------------------------------------------------------------------------
# Demo / entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng = np.random.default_rng(42)
    N, D_expr = 5_000, 382
    V = 5023

    expression_params = rng.standard_normal((N, D_expr)).astype(np.float32) * 2
    pca_basis = rng.standard_normal((D_expr, V * 3)).astype(np.float32) * 0.001
    mean_face = rng.standard_normal(V * 3).astype(np.float32)

    # --- Extract biomechanical signals ---
    jaw_vecs, muscle_ratios, muscle_names = extract_biomechanical_signals(
        expression_params, pca_basis, mean_face,
        batch_size=500,
    )
    print(f"jaw_vecs: {jaw_vecs.shape}, muscle_ratios: {muscle_ratios.shape}")

    # --- Correlation analysis ---
    muscle_expression_correlation(jaw_vecs, muscle_ratios, expression_params, muscle_names)

    # --- Option A ---
    reg, scaler_A = fit_linear(jaw_vecs, muscle_ratios, expression_params)
    mesh_A = synthesize_linear(jaw_vecs[0], muscle_ratios[0], reg, scaler_A, pca_basis, mean_face)
    print(f"[A] synthesized mesh shape: {mesh_A.shape}")

    # --- Option B ---
    knn, scaler_B, Xs, _ = build_knn(jaw_vecs, muscle_ratios, expression_params, k=8)
    mesh_B = synthesize_knn(jaw_vecs[0], muscle_ratios[0], knn, scaler_B, Xs,
                             expression_params, pca_basis, mean_face)
    print(f"[B] synthesized mesh shape: {mesh_B.shape}")

    # --- Option C ---
    if _TORCH:
        model, x_mean, x_std = train_mlp(
            jaw_vecs, muscle_ratios, expression_params, pca_basis, mean_face,
            epochs=20, batch_size=64,
        )
        mesh_C = synthesize_mlp(jaw_vecs[0], muscle_ratios[0], model, x_mean, x_std, mean_face)
        print(f"[C] synthesized mesh shape: {mesh_C.shape}")
