---
title: "Nonlinear Face Model — Moving Beyond PCA"
date: 2026-04-22
tags: [muscles, neural, digital-human, blendshapes, rig-generation, python, pose-space]
context: "Face PCA model with 253 identity + 382 expression parameters, 100k animated poses with jaw SE(3) and muscle stretch ratios."
---

## Motivation — Why Leave PCA

A PCA expression model is a linear map: `verts = mean + expr_params @ basis`. This means:
- **No muscle co-activation**: AU12 + AU26 together is exactly the sum of each alone; real tissue coupling is ignored
- **Volume loss**: linear blending collapses volume on wide jaw-opens, compound smiles, extreme deformations
- **No identity coupling**: the same expression components applied to a wide vs narrow face look identical in delta space; identity-specific deformation patterns are invisible
- **No semantic controls**: the 382 PCA axes are ordered by variance, not anatomy; you cannot directly drive jaw opening or zygomaticus contraction

The goal is to replace the linear decode with a model that maps **physically meaningful controls** directly to vertex positions, learning the nonlinear interactions from data.

---

## Architecture Overview

Three components learned jointly from the 100k pose dataset:

```
neutral_mesh (V,3)
    │
    ▼ IdentityEncoder
z_id (64-dim)  ──────────────────┐
                                  │
jaw SE(3):   [R_6d (6) | t (3)]  ├─► concat (64+9+M×S) ──► MLPDecoder ──► delta_verts (V,3)
muscle_segs: (M×S,) zero-mean   ┘   S=3 segments per muscle (origin/belly/insertion)
                                  │
                                  ▼
                   posed_verts = neutral_verts + delta_verts
```

### Identity Encoder

Maps a neutral mesh to a per-subject identity code `z_id`.

**Learned encoder** (for large multi-character datasets):
```
neutral_flat (V*3,) → Linear(512) → LN → GELU → Linear(512) → LN → GELU → Linear(64)
```
Input is mean/std-normalized across all subjects before encoding. Gradient does not flow through identity during expression training — `z_id` is treated as a fixed conditioning signal.

**PCA encoder** (for small datasets, ≤ ~200 subjects):
`z_id = pca.transform(neutral_flat)` — no learning required; 64 components typically explain ≥ 95% of neutral mesh variance across characters. Fast and interpretable.

### Jaw Parameterization — 6D Rotation

Quaternions have an antipodal ambiguity (q and −q represent the same rotation) and a unit-sphere discontinuity that complicates gradient flow. Instead, use the **6D continuous rotation representation** (Zhou et al. 2019): store the first two columns of the rotation matrix (6 floats), recover the third via cross product:

```python
def rotation_to_6d(R):           # (3,3) → (6,)
    return R[:, :2].T.flatten()

def rotation_from_6d(x):         # (6,) → (3,3) — Gram-Schmidt
    a1, a2 = x[:3], x[3:]
    b1 = normalize(a1)
    b2 = normalize(a2 - dot(b1, a2) * b1)
    b3 = cross(b1, b2)
    return stack([b1, b2, b3], axis=-1)
```

Final jaw input: `[R_6d (6) | t / skull_scale (3)]` → 9-dim vector. Jaw translation is normalized by per-subject skull scale for cross-subject comparability.

### Muscle Segment Ratios

Each muscle contributes **3 segment ratios** (origin / belly / insertion) rather than a single global ratio. The curve is resampled to uniform arc length before segmenting, so each segment covers an equal fraction of the rest-pose muscle length regardless of how many raw control points exist.

Feature layout: `[m0_seg0, m0_seg1, m0_seg2, m1_seg0, ..., mM_seg2]` → **(M × 3,)**. For 11 muscles: 33 muscle features total.

Active (contracted) muscles have `ratio < 1`; passive stretch gives `ratio > 1`. The belly segment (seg1) shows the largest signal during peak activation. Normalization: zero-mean per feature dimension across all training poses.

### MLP Decoder

```
in_dim = 64 + 9 + M*3   # M muscles × 3 segments

Linear(in_dim → 512) → LayerNorm → GELU
Linear(512 → 512)    → LayerNorm → GELU
Linear(512 → 1024)   → LayerNorm → GELU
Linear(1024 → 2048)  → LayerNorm → GELU
Linear(2048 → V×3)   ← no activation (deltas are signed)
```

- **LayerNorm** not BatchNorm: stable at batch size 1 (inference), no batch statistics drift
- **GELU** not ReLU: smooth second derivative → smoother mesh deformations
- **Linear final layer**: predicts signed deltas; no activation prevents squashing

### UV-Space Convolutional Decoder (optional upgrade)

Replaces the linear output layer with a convolutional upsampler over the UV map, giving the network a spatial inductive bias: nearby UV pixels influence each other, so the network learns spatially coherent surface deformations rather than per-vertex independence.

```
MLP trunk → Linear(2048 × seed_h × seed_h)
         → reshape (B, 2048, seed_h, seed_h)
         → 4× Upsample block (2× each: Conv→GELU→Conv)
         → Conv2d(3)                          ← (B, 3, 256, 256) delta UV map
         → F.grid_sample at vertex UVs        ← (B, V, 3)
```

Requires a **single-island UV layout** with consistent per-vertex UV coordinates across all subjects (baked once in Houdini/Blender). Seam should be placed in a low-deformation region (top of skull or back of head).

---

## Data Preparation

The PCA basis is used **once**, as a data extraction tool, then discarded.

### Step 1 — Decode PCA Poses to Vertex Positions

```python
# One-time batch decode, save to HDF5
V = mean_face.shape[0] // 3
neutral_verts = mean_face.reshape(V, 3)

all_posed = np.empty((N, V, 3), dtype=np.float32)
for s in range(0, N, 2000):
    e = min(s + 2000, N)
    all_posed[s:e] = (expression_params[s:e] @ pca_basis + mean_face).reshape(-1, V, 3)

delta_verts = all_posed - neutral_verts[None]   # (N, V, 3)
```

### Step 2 — Extract Jaw SE(3) and Muscle Ratios

See `[[python/jaw_muscle_synthesis.py]]` → `extract_biomechanical_signals()`.

Output: `jaw_9d (N, 9)`, `muscle_ratios (N, M)`.

### Step 3 — Export to HDF5

```python
from wiki.python.nonlinear_face_model import export_to_hdf5

export_to_hdf5(
    "data/train.h5",
    subject_id="subject_01",
    neutral_flat=neutral_verts.flatten(),
    skull_scale=compute_skull_scale(neutral_verts),   # e.g. max inter-landmark distance
    jaw_9d=jaw_9d,
    muscle_ratios=muscle_ratios,
    delta_verts=delta_verts,
)
```

Multi-subject: call once per subject, all appended to the same HDF5 under different subject keys.

---

## Loss Functions

Three losses combined with weights:

| Loss | Formula | Weight | Purpose |
|---|---|---|---|
| **Vertex L1** | `|pred_delta - gt_delta|` | 1.0 | Primary reconstruction |
| **Laplacian** | `‖L @ pred_delta‖²` | 0.1 | Smoothness; prevent high-frequency noise |
| **Neutral anchor** | `‖decoder(z_id, 0, 0)‖²` | 0.01 | Force neutral expression = zero delta |

The Laplacian matrix `L = I - D⁻¹A` (uniform weighting) or cotangent weighting (more accurate but requires face data). Pre-compute once:

```python
from nonlinear_face_model import build_uniform_laplacian
L = build_uniform_laplacian(mesh_faces, n_verts)   # (V, V) dense
```

The **neutral anchor loss** is the key disentanglement constraint. Without it, the network encodes residual expression information in `z_id` ("cheating" by putting pose information in the identity code).

---

## Training

```python
from nonlinear_face_model import (
    NonlinearFaceModel, FaceDataset, FaceModelTrainer, DataLoader
)

# --- Dataset ---
muscle_mean, muscle_std = FaceDataset.compute_muscle_stats("data/train.h5")
train_ds = FaceDataset("data/train.h5", muscle_mean, muscle_std)
val_ds   = FaceDataset("data/val.h5",   muscle_mean, muscle_std)
train_dl = DataLoader(train_ds, batch_size=128, shuffle=True,  num_workers=4)
val_dl   = DataLoader(val_ds,   batch_size=256, shuffle=False, num_workers=4)

# --- Model ---
model = NonlinearFaceModel(
    n_verts=5023,
    n_muscles=11,
    latent_dim=64,
    decoder="mlp",      # or "uvconv" if UVs are available
    hidden=512,
)

# Optional: pass Laplacian for smoothness loss
L = build_uniform_laplacian(mesh_faces, 5023)

trainer = FaceModelTrainer(
    model, lr=1e-3, w_laplacian=0.1, w_neutral=0.01,
    laplacian_matrix=L, device="cuda",
)
trainer.fit(train_dl, val_dl, epochs=100, save_path="checkpoints/best.pt")
```

**Expected training curve**: vertex L1 should drop rapidly in the first 10 epochs (linear regime), then slowly improve as the network learns nonlinear interactions. If the neutral anchor loss plateaus above 1e-4, increase its weight — the identity encoder may be encoding expression information.

**Multi-GPU**: wrap model in `torch.nn.DataParallel` before passing to trainer; the trainer is standard PyTorch and GPU-agnostic.

---

## Inference

```python
import torch
from nonlinear_face_model import NonlinearFaceModel, synthesize, cache_identity

# Load checkpoint
ckpt = torch.load("checkpoints/best.pt")
model = NonlinearFaceModel(n_verts=5023, n_muscles=11)
model.load_state_dict(ckpt["model_state"])

# Pre-cache identity (once per character)
z_id = cache_identity(neutral_verts, model, device="cpu")

# Synthesize: jaw open + right smile
from scipy.spatial.transform import Rotation
jaw_R = Rotation.from_euler("x", 15, degrees=True).as_matrix()
jaw_t = np.array([0.0, -1.2, 0.0])  # mandible drop in world cm
muscles = np.ones(11)               # rest (ratio = 1.0)
muscles[0] = 0.82                   # zygomaticus_major_L contracted
muscles[1] = 1.0                    # zygomaticus_major_R at rest (asymmetric smile)

posed_verts = synthesize(
    neutral_verts, jaw_R, jaw_t, muscles,
    model, muscle_mean, muscle_std,
    skull_scale=skull_scale, z_id=z_id,
)
```

At inference: the identity encoder runs **once** per character (`cache_identity`); subsequent synthesis calls skip it entirely — only the decoder runs, giving ~1ms per frame on CPU.

---

## Houdini Python SOP

Integrate the trained model directly into a Houdini SOP network. The jaw null's world transform and live muscle curve lengths drive synthesis in real time.

```python
# Python SOP — cook callback
import hou, numpy as np, torch

node   = hou.pwd()
geo    = node.geometry()

# --- Read jaw transform from jaw null object ---
jaw_obj    = node.parm("jaw_null").evalAsNode()
jaw_xform  = np.array(jaw_obj.worldTransform().asTuple()).reshape(4, 4)
R = jaw_xform[:3, :3]; t = jaw_xform[:3, 3]
jaw_9d = np.concatenate([R[:, :2].T.flatten(), t]).astype(np.float32)

# --- Read muscle stretch ratios from detail attrib ---
muscle_ratios = np.array(geo.attribValue("muscle_ratios"), dtype=np.float32)  # (M,)
muscles_norm  = (muscle_ratios - node._muscle_mean) / node._muscle_std

# --- Synthesize ---
posed = synthesize(
    node._neutral_verts,
    R, t, muscle_ratios,
    node._model, node._muscle_mean, node._muscle_std,
    skull_scale=node._skull_scale,
    z_id=node._z_id,            # pre-cached
)

# --- Write back to geometry ---
for i, v in enumerate(posed):
    geo.point(i).setPosition(hou.Vector3(float(v[0]), float(v[1]), float(v[2])))
```

Cache `_model`, `_z_id`, `_neutral_verts`, `_muscle_mean`, `_muscle_std`, `_skull_scale` on the node object during the first cook (guard with `hasattr(node, "_model")`). Houdini will reuse them across cooks.

---

## What Changes vs PCA Model

| | PCA model | Nonlinear model |
|---|---|---|
| **Control space** | 382 abstract components | jaw SE(3) + M muscle ratios |
| **Runtime decode** | `expr @ basis + mean` (~0.1ms) | MLP forward pass (~1ms) |
| **Muscle coupling** | Linear superposition only | Nonlinear interactions learned |
| **Identity** | Fixed mean face per subject | `z_id` conditions all deformations |
| **New character** | Refit PCA basis | Encode neutral mesh → `z_id`; swap in |
| **Expression swap** | Not straightforward | `z_id` of char A + jaw/muscles of char B |
| **Training needed** | No (PCA is analytic) | Yes (100k poses, ~1hr on GPU) |
| **Interpretability** | Low (PCA axes) | Medium (jaw angle, muscle name) |

---

## Practical Notes

**When to keep PCA**: If your pipeline already uses the 382 PCA params as the rig interface (e.g. a downstream blendshape solver reads them), keep the PCA basis as an intermediate representation and train a small adapter `(jaw, muscles) → expr_params` (Option A in `[[explorations/jaw-muscle-driven-synthesis]]`).

**Skull scale**: compute once as the distance between two stable bony landmarks (e.g. left and right tragion, or inner canthus distance). This normalizes jaw translation across subjects with different head sizes.

**Missing muscles**: if some muscle curves cannot be extracted for a pose (e.g. due to tracking failure), mask those dimensions to the muscle's mean ratio at training time. The model learns to be robust to per-muscle zeroing if ~10% of training samples have masked muscles.

**Expression swap artefacts**: swapping `z_id` between characters while keeping the same jaw/muscle input can produce subtle topology drift near ear and neck regions — areas with high identity variance but low expression variance. Add a small L2 penalty on the identity code magnitude to encourage compact identity representations that generalize across subjects.

**Convergence check**: after 50 epochs, plot a scatter of predicted vs ground-truth vertex positions along one axis for a held-out pose. Expect R² > 0.99 for training poses, > 0.95 for val. Lower val R² indicates the model is memorising training poses rather than generalising — increase Laplacian weight or add dropout (10%) after GELU layers.

---

## Implementation

Full Python implementation: `[[python/nonlinear_face_model.py]]`

Classes and functions:
- `IdentityEncoder` — learned neutral mesh → z_id
- `pca_identity_encoder()` — analytic alternative for small datasets
- `MLPDecoder` — MLP trunk → vertex deltas
- `UVConvDecoder` — MLP trunk + UV-space conv upsample
- `NonlinearFaceModel` — full model wrapper
- `build_uniform_laplacian()` — Laplacian matrix from face indices
- `laplacian_loss()`, `neutral_anchor_loss()` — loss components
- `FaceDataset` — HDF5-backed multi-subject dataset
- `NumpyFaceDataset` — single-subject numpy dataset
- `FaceModelTrainer` — training loop with scheduler + checkpointing
- `synthesize()` — inference from jaw SE(3) + muscle ratios
- `cache_identity()` — pre-compute z_id for a character
- `export_to_hdf5()` — save training data from PCA-decoded poses

---

## Connections

- [[explorations/jaw-muscle-driven-synthesis]] — data extraction pipeline; Options A–C use PCA as runtime intermediary; Option C (MLP) is a simplified version of this model
- [[concepts/biomechanical-face-model-architecture]] — full architecture specification this implements
- [[concepts/nonlinear-face-models]] — broader landscape: CoMA, DECA, NPHM, ImFace
- [[concepts/muscles]] — muscle anatomy and stretch ratio conventions
- [[concepts/latent-generative-modelling]] — UV-space conv upsample inspired by latent diffusion VAE decoders
- [[concepts/pose-space-deformation]] — the PCA expression space this replaces
- [[papers/zeng-2021-neuromuscular-face]] — neuromuscular face control; closest prior work
- [[papers/bao-2019-face-capture-muscles]] — anatomy-based face capture using muscle activations
- [[papers/ranjan-2018-coma]] — CoMA: mesh convolutional autoencoder; alternative nonlinear shape space for identity encoder
