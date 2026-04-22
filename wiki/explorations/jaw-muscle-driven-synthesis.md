---
title: "Jaw + Muscle Driven Face Mesh Synthesis from PCA Model"
date: 2026-04-22
tags: [muscles, blendshapes, neural, python, digital-human, pose-space, houdini]
context: "Face PCA model with 253 identity + 382 expression parameters, 100k animated poses. Each pose can have jaw SE(3) and muscle 3D curves computed programmatically."
---

## Problem

Given 100k expression poses (each a vector of 382 PCA expression coefficients), and the ability to compute from each pose:
- A jaw rigid body transform (SE(3): rotation + translation of mandible relative to skull)
- Muscle 3D curves (polyline origin → insertion per muscle), from which stretch/compression ratios can be derived

Build a system that synthesizes a new head mesh given **jaw position** and **muscle stress/compression factors** — without going through the full PCA expression space.

This reparameterizes the face model from abstract statistical axes to biomechanically meaningful controls.

---

## Data Extraction Pipeline

Before fitting any model, extract the biomechanical signals from all 100k poses.

### Step 1 — Jaw SE(3) Extraction

Fit a rigid transform from mandible vertices between neutral and each posed mesh. The jaw SE(3) = rotation R (3×3 or quaternion 4) + translation t (3), skull-relative frame.

```python
import numpy as np
from scipy.spatial.transform import Rotation

# jaw_mask: vertex indices covering mandible/jaw region
# For FLAME topology: roughly np.arange(400, 620) — see FLAME_REGION_MASKS in facs_pose_tsne.py
# Better: use a dedicated mandible segmentation mask

def extract_jaw_se3(posed_verts: np.ndarray, neutral_verts: np.ndarray, jaw_mask: np.ndarray):
    """
    Fit SE(3) of mandible between posed and neutral mesh.
    Returns (R, t) where posed[jaw] ≈ R @ neutral[jaw] + t.
    R: (3,3), t: (3,)
    """
    p = posed_verts[jaw_mask]   # (K, 3)
    n = neutral_verts[jaw_mask]  # (K, 3)
    pc, nc = p.mean(0), n.mean(0)
    H = (p - pc).T @ (n - nc)   # cross-covariance
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:    # reflection fix
        Vt[-1] *= -1
        R = Vt.T @ U.T
    t = pc - R @ nc
    return R, t

def jaw_se3_to_vec(R: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Flatten SE(3) to 7-dim vector: [quat xyzw (4) | translation (3)]."""
    q = Rotation.from_matrix(R).as_quat()  # [x, y, z, w]
    return np.concatenate([q, t])           # (7,)
```

### Step 2 — Muscle Stretch Ratio Extraction

Each muscle is a polyline: a sequence of 3D points from origin to insertion, passing through any intermediate control points. The stretch ratio = `current_length / rest_length`.

```python
def polyline_length(points: np.ndarray) -> float:
    """Arc length of a polyline (N, 3)."""
    return float(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)))

def muscle_stretch_ratio(
    posed_verts: np.ndarray,
    neutral_verts: np.ndarray,
    attachment_indices: list[np.ndarray],
) -> float:
    """
    attachment_indices: list of vertex index arrays, one per control point
    (origin, [via points], insertion). Each array is averaged to a centroid.
    """
    def sample_point(verts, idx_arr):
        return verts[idx_arr].mean(0)

    posed_pts = np.stack([sample_point(posed_verts, idx) for idx in attachment_indices])
    neutral_pts = np.stack([sample_point(neutral_verts, idx) for idx in attachment_indices])

    rest_len = polyline_length(neutral_pts)
    if rest_len < 1e-8:
        return 1.0
    return polyline_length(posed_pts) / rest_len
```

### Step 3 — Batch Extraction

```python
def extract_biomechanical_signals(
    expression_params: np.ndarray,  # (N, 382)
    pca_basis: np.ndarray,          # (382, V*3)
    mean_face: np.ndarray,          # (V*3,)
    jaw_mask: np.ndarray,           # mandible vertex indices
    muscle_attachments: list[list[np.ndarray]],  # per muscle: list of attachment index arrays
    batch_size: int = 2000,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns
    -------
    jaw_vecs    : (N, 7)   jaw SE(3) as [quat | trans] per pose
    muscle_ratios: (N, M)  stretch ratio per muscle per pose
    """
    from scipy.spatial.transform import Rotation

    N = len(expression_params)
    V = mean_face.shape[0] // 3
    neutral_verts = mean_face.reshape(V, 3)
    M = len(muscle_attachments)

    jaw_vecs = np.empty((N, 7), dtype=np.float32)
    muscle_ratios = np.empty((N, M), dtype=np.float32)

    for start in range(0, N, batch_size):
        end = min(start + batch_size, N)
        batch = expression_params[start:end].astype(np.float32)
        verts_batch = (batch @ pca_basis.astype(np.float32) + mean_face).reshape(-1, V, 3)

        for i, verts in enumerate(verts_batch):
            R, t = extract_jaw_se3(verts, neutral_verts, jaw_mask)
            jaw_vecs[start + i] = jaw_se3_to_vec(R, t)
            for m, att in enumerate(muscle_attachments):
                muscle_ratios[start + i, m] = muscle_stretch_ratio(verts, neutral_verts, att)

        if start % (batch_size * 5) == 0:
            print(f"  extracted {end:>7,} / {N:,}")

    return jaw_vecs, muscle_ratios
```

---

## Solution Options

### Overview

| Approach | Complexity | Quality | Real-time? | Invertible? |
|---|---|---|---|---|
| A. Linear regression | Low | Baseline | Yes | Yes (pseudoinverse) |
| B. RBF / K-NN blending | Medium | Good for interpolation | Medium | No |
| C. MLP decoder | High | Best generalization | Yes (fast inference) | No |
| D. Houdini CHOP network | Medium | Production-ready | Yes | Partially |

---

## Option A — Linear Regression

Fit `expression_params ≈ W @ x + b` where `x = [jaw_vec (7) | muscle_ratios (M)]`.

```python
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

def fit_linear_synthesis(
    jaw_vecs: np.ndarray,      # (N, 7)
    muscle_ratios: np.ndarray, # (N, M)
    expression_params: np.ndarray,  # (N, 382)
    alpha: float = 1e-3,
) -> tuple:
    X = np.concatenate([jaw_vecs, muscle_ratios], axis=1)  # (N, 7+M)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    reg = Ridge(alpha=alpha)
    reg.fit(X_scaled, expression_params)

    r2 = reg.score(X_scaled, expression_params)
    print(f"Train R²: {r2:.4f}")
    return reg, scaler

def synthesize_linear(
    jaw_vec: np.ndarray,     # (7,)
    muscle_ratio: np.ndarray,  # (M,)
    reg, scaler,
    pca_basis, mean_face,
) -> np.ndarray:
    x = np.concatenate([jaw_vec, muscle_ratio])[None]  # (1, 7+M)
    x_scaled = scaler.transform(x)
    expr_params = reg.predict(x_scaled)               # (1, 382)
    V = mean_face.shape[0] // 3
    verts = (expr_params @ pca_basis + mean_face).reshape(V, 3)
    return verts
```

**When to use**: quick prototype, interpretable weights, `reg.coef_` shows which muscles drive which PCA components.

**Limitation**: cannot capture jaw-muscle interactions; muscles that co-activate non-linearly will smear.

---

## Option B — RBF / K-NN Blending

Use the 100k poses as a scattered data library. At synthesis time, find the K nearest poses in (jaw, muscle) space and blend their vertex positions.

```python
from sklearn.neighbors import NearestNeighbors
from scipy.interpolate import RBFInterpolator

def build_knn_library(jaw_vecs, muscle_ratios, expression_params, pca_basis, mean_face):
    X = np.concatenate([jaw_vecs, muscle_ratios], axis=1).astype(np.float32)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    knn = NearestNeighbors(n_neighbors=8, algorithm='ball_tree', n_jobs=-1)
    knn.fit(X_scaled)
    return knn, scaler, X_scaled, expression_params

def synthesize_knn(
    jaw_vec, muscle_ratio,
    knn, scaler, X_scaled, expression_params,
    pca_basis, mean_face,
    k: int = 8,
    kernel: str = "gaussian",
):
    x = np.concatenate([jaw_vec, muscle_ratio])[None]
    x_scaled = scaler.transform(x)
    dists, idxs = knn.kneighbors(x_scaled, n_neighbors=k)
    dists = dists[0]; idxs = idxs[0]

    if kernel == "gaussian":
        sigma = dists.mean() + 1e-8
        w = np.exp(-0.5 * (dists / sigma) ** 2)
    else:  # inverse distance
        w = 1.0 / (dists + 1e-8)
    w /= w.sum()

    # Blend expression params (linear blend in PCA space is valid)
    expr = (w[:, None] * expression_params[idxs]).sum(0)  # (382,)
    V = mean_face.shape[0] // 3
    return (expr @ pca_basis + mean_face).reshape(V, 3)
```

**When to use**: exact interpolation through training poses, no training required beyond indexing, good for dense libraries.

**Limitation**: slow at query time for 100k poses unless you use an ANN index (FAISS); blending in PCA expression space is linear — nonlinear deformation interactions need vertex-space blending instead.

---

## Option C — MLP Decoder (Biomechanical Face Model)

Train a neural decoder mapping biomechanical controls → mesh vertex deltas. This is the architecture described in `[[concepts/biomechanical-face-model-architecture]]`, adapted for PCA-derived supervision.

The key insight: use the 100k poses as training supervision, with decoded mesh deltas as targets.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BiomechanicalDecoder(nn.Module):
    """
    Maps (jaw SE(3) + muscle scalars) → per-vertex mesh delta.
    
    Input dim:  7 (jaw) + M (muscles)
    Output dim: V * 3 (vertex deltas, flattened)
    """
    def __init__(self, n_muscles: int, n_verts: int, hidden: int = 512):
        super().__init__()
        in_dim = 7 + n_muscles
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),   nn.LayerNorm(hidden), nn.GELU(),
            nn.Linear(hidden, hidden),   nn.LayerNorm(hidden), nn.GELU(),
            nn.Linear(hidden, hidden*2), nn.LayerNorm(hidden*2), nn.GELU(),
            nn.Linear(hidden*2, n_verts * 3),
        )

    def forward(self, x):
        return self.net(x).reshape(x.shape[0], -1, 3)  # (B, V, 3)


def train_biomechanical_decoder(
    jaw_vecs: np.ndarray,        # (N, 7)
    muscle_ratios: np.ndarray,   # (N, M)
    expression_params: np.ndarray,  # (N, 382)
    pca_basis: np.ndarray,       # (382, V*3)
    mean_face: np.ndarray,       # (V*3,)
    epochs: int = 50,
    batch_size: int = 256,
    lr: float = 1e-3,
    device: str = "cpu",
):
    """Pre-decode expression_params → mesh deltas on CPU in batches, then train."""
    N, V3 = len(expression_params), mean_face.shape[0]
    V = V3 // 3
    neutral = mean_face.reshape(1, V, 3)

    # Pre-compute all mesh deltas (supervision targets)
    print("Pre-computing mesh deltas ...")
    all_deltas = np.empty((N, V, 3), dtype=np.float32)
    bs = 2000
    for s in range(0, N, bs):
        e = min(s + bs, N)
        verts = (expression_params[s:e].astype(np.float32) @ pca_basis.astype(np.float32) + mean_face)
        all_deltas[s:e] = verts.reshape(-1, V, 3) - neutral

    X = np.concatenate([jaw_vecs, muscle_ratios], axis=1).astype(np.float32)

    # Normalize inputs
    x_mean = X.mean(0); x_std = X.std(0) + 1e-8
    X = (X - x_mean) / x_std

    model = BiomechanicalDecoder(muscle_ratios.shape[1], V).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)

    X_t = torch.from_numpy(X).to(device)
    Y_t = torch.from_numpy(all_deltas.reshape(N, -1)).to(device)  # (N, V*3)

    for epoch in range(epochs):
        idx = torch.randperm(N, device=device)
        epoch_loss = 0.0
        for s in range(0, N, batch_size):
            i = idx[s:s+batch_size]
            pred = model(X_t[i])          # (B, V, 3)
            target = Y_t[i].reshape(-1, V, 3)
            loss = F.l1_loss(pred, target)
            opt.zero_grad(); loss.backward(); opt.step()
            epoch_loss += loss.item()
        sched.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch:3d}  loss={epoch_loss/(N//batch_size+1):.5f}")

    return model, x_mean, x_std


def synthesize_mlp(
    jaw_vec: np.ndarray,
    muscle_ratio: np.ndarray,
    model, x_mean, x_std, mean_face,
    device: str = "cpu",
) -> np.ndarray:
    x = np.concatenate([jaw_vec, muscle_ratio])
    x = ((x - x_mean) / x_std).astype(np.float32)
    with torch.no_grad():
        delta = model(torch.from_numpy(x[None]).to(device)).cpu().numpy()[0]  # (V, 3)
    V = mean_face.shape[0] // 3
    return mean_face.reshape(V, 3) + delta
```

**When to use**: when generalization to unseen jaw+muscle combinations is needed. The MLP can extrapolate beyond the training distribution (with some degradation) while K-NN cannot. Inference is ~1ms on CPU for V=5023.

**Extensions:**
- Add identity code `z_id` (from neutral mesh PCA) to disentangle who from what expression
- UV-space convolutional upsampler instead of linear output layer — see `[[concepts/biomechanical-face-model-architecture]]`
- Laplacian loss to prevent high-frequency surface noise

---

## Option D — Houdini Network

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  SOP Network                                         │
│                                                      │
│  jaw_ctrl (null/object)                              │
│       ↓ world transform → jaw_SE3 (7 floats)        │
│                                                      │
│  muscle_curves (polylines in rest pose)              │
│       ↓ [Muscle SOP / polyline measure]              │
│  stretch_ratios (M floats, detail attribs)           │
│                                                      │
│  [Python SOP or compiled VEX]                        │
│  ├── concatenate [jaw_SE3 | stretch_ratios]          │
│  ├── query KNN in pose library (detail attrib HDF5)  │
│  └── blend K nearest expression param vectors        │
│       ↓                                              │
│  [Blend SOP] or [PCA decode VEX wrangle]             │
│       ↓                                              │
│  output_mesh                                         │
└─────────────────────────────────────────────────────┘
```

### VEX — Compute Jaw SE(3) from Mandible Vertices

```vex
// Wrangle on geo (jaw vertices only, in object space)
// Input 0: posed jaw verts, Input 1: neutral jaw verts
// Writes jaw_quat and jaw_trans to detail attributes

int npts = npoints(0);
vector posed_centroid = {0,0,0};
vector neutral_centroid = {0,0,0};
for (int i = 0; i < npts; i++) {
    posed_centroid   += point(0, "P", i);
    neutral_centroid += point(1, "P", i);
}
posed_centroid   /= npts;
neutral_centroid /= npts;

// Cross-covariance H = (posed - pc)^T @ (neutral - nc)
matrix3 H = ident();
// ... (SVD not directly available in VEX — use Python SOP for SE(3) fit)
// In practice: pass jaw transform as object-level transform, read via optransform()
matrix jaw_world = optransform("../jaw_null");
vector4 q = quaternion(matrix3(jaw_world));
vector t = cracktransform(XFORM_SRT, XFORM_XYZ, 0, {0,0,0}, jaw_world);
setdetailattrib(0, "jaw_quat", q, "set");
setdetailattrib(0, "jaw_trans", t, "set");
```

### VEX — Compute Muscle Stretch Ratios

```vex
// Detail wrangle, Input 0: posed muscle curves, Input 1: rest muscle curves
// Each primitive = one muscle polyline
int n_muscles = nprimitives(0);
float ratios[];
resize(ratios, n_muscles);
for (int m = 0; m < n_muscles; m++) {
    int pts_posed[]  = primpoints(0, m);
    int pts_rest[]   = primpoints(1, m);
    float len_posed = 0.0, len_rest = 0.0;
    for (int i = 0; i < len(pts_posed)-1; i++) {
        vector a = point(0, "P", pts_posed[i]);
        vector b = point(0, "P", pts_posed[i+1]);
        len_posed += length(b - a);
    }
    for (int i = 0; i < len(pts_rest)-1; i++) {
        vector a = point(1, "P", pts_rest[i]);
        vector b = point(1, "P", pts_rest[i+1]);
        len_rest += length(b - a);
    }
    ratios[m] = (len_rest > 1e-6) ? len_posed / len_rest : 1.0;
}
setdetailattrib(0, "muscle_ratios", ratios, "set");
```

### Python SOP — KNN Query and Expression Blend

```python
# Python SOP node
# Inputs: node with jaw_quat/jaw_trans/muscle_ratios detail attribs

import hou, numpy as np

node = hou.pwd()
geo = node.geometry()

q    = np.array(geo.attribValue("jaw_quat"))    # (4,)
t    = np.array(geo.attribValue("jaw_trans"))   # (3,)
ratios = np.array(geo.attribValue("muscle_ratios"))  # (M,)

query = np.concatenate([q, t, ratios])[None].astype(np.float32)

# Load or cache the pose library (KNN index built at setup time)
import os, pickle
cache_path = hou.getenv("POSE_LIBRARY_PATH", "/path/to/pose_library.pkl")
if not hasattr(node, "_pose_library"):
    with open(cache_path, "rb") as f:
        node._pose_library = pickle.load(f)
lib = node._pose_library  # dict: X_scaled, scaler, expression_params, pca_basis, mean_face, knn

x_scaled = lib["scaler"].transform(query)
dists, idxs = lib["knn"].kneighbors(x_scaled, n_neighbors=8)
dists, idxs = dists[0], idxs[0]
w = np.exp(-0.5 * (dists / (dists.mean() + 1e-8)) ** 2)
w /= w.sum()

expr = (w[:, None] * lib["expression_params"][idxs]).sum(0)
verts = (expr @ lib["pca_basis"] + lib["mean_face"]).reshape(-1, 3)

# Write positions back to Houdini geo
for i, v in enumerate(verts):
    pt = geo.point(i)
    pt.setPosition(hou.Vector3(v))
```

---

## Muscle Attachment Points (FLAME topology approximation)

Approximate vertex index sets per facial muscle, for use with `muscle_stretch_ratio()`:

```python
FLAME_MUSCLE_ATTACHMENTS = {
    "zygomaticus_major_L": [
        np.arange(1900, 1940),   # origin: zygomatic arch
        np.arange(3050, 3070),   # insertion: lip corner
    ],
    "zygomaticus_major_R": [
        np.arange(2060, 2100),
        np.arange(3080, 3100),
    ],
    "orbicularis_oris": [
        np.arange(3440, 3480),   # top ring
        np.arange(3480, 3560),   # bottom ring
    ],
    "levator_labii_L": [
        np.arange(2140, 2180),   # origin: infraorbital margin
        np.arange(3100, 3130),   # insertion: upper lip
    ],
    "levator_labii_R": [
        np.arange(2200, 2240),
        np.arange(3200, 3230),
    ],
    "depressor_anguli_oris_L": [
        np.arange(600,  640),    # origin: mandible base
        np.arange(3000, 3030),   # insertion: lip corner
    ],
    "depressor_anguli_oris_R": [
        np.arange(640,  680),
        np.arange(3060, 3090),
    ],
    "masseter_L": [
        np.arange(1850, 1900),   # origin: zygomatic arch / cheek bone
        np.arange(400,  450),    # insertion: mandible ramus
    ],
    "masseter_R": [
        np.arange(2020, 2060),
        np.arange(450,  500),
    ],
    "frontalis_L": [
        np.arange(1320, 1400),   # origin: hairline / galea
        np.arange(1400, 1480),   # insertion: brow skin
    ],
    "frontalis_R": [
        np.arange(1560, 1640),
        np.arange(1480, 1560),
    ],
}
```

These are rough centroid-based estimates for the 5023-vertex FLAME topology. Replace with precise mesh segmentation for production use.

---

## Practical Notes

**Jaw isolation**: The jaw SE(3) extracted via Procrustes is entangled with expression in PCA models — opening the jaw also deforms lip vertices that are part of the mandible group if the segmentation is imprecise. Use a tight jaw-bone-only mask (zygomatic arch excluded) for the SE(3) fit.

**Muscle sign convention**: `ratio > 1` = stretched (tension / elongated), `ratio < 1` = compressed (contracted, shortened). For most facial muscles, AU activation = shortening, so expect `ratio < 1` for active muscles.

**Completeness**: 12–20 muscles cover most FACS AUs. You don't need all 24 named muscles — the system works with however many curves you can extract. Unmeasured muscles will be captured by the regression's residual or learned implicitly by the MLP.

**Model selection by use case**:
- Realtime rig preview in Houdini → Option D (CHOP/SOP network)
- Offline data analysis / AU correlation study → Option A (linear regression + inspect coefficients)
- New pose generation / generalization → Option C (MLP)
- Closest-pose retrieval / controlled retake → Option B (KNN)

**PCA space linearity**: Blending expression params in PCA space (options A and B) is valid for small deformations but will produce volume loss at extreme jaw-open or combined AU poses. Blending in vertex space (weighted sum of decoded mesh positions) is more accurate but requires decoding each neighbor.

---

## Implementation

Full Python implementation: `[[python/jaw_muscle_synthesis.py]]`

---

## Connections

- [[explorations/facs-pose-tsne]] — companion exploration: UMAP clustering of the same 100k poses by FACS region
- [[concepts/biomechanical-face-model-architecture]] — full neural architecture for this synthesis approach
- [[concepts/muscles]] — muscle anatomy and rig use
- [[concepts/pose-space-deformation]] — the PCA expression space this reparameterizes
- [[concepts/flame-model]] — FLAME 382-component expression space and decoder
- [[papers/bao-2019-face-capture-muscles]] — anatomy-based face capture using muscle activations
- [[papers/zeng-2021-neuromuscular-face]] — neuromuscular face control; directly related
