---
title: "Biomechanical Face Model — Architecture Design"
tags: [muscles, neural, digital-human, blendshapes, rig-generation, python]
---

## Definition
A learning-based facial deformation model that takes **muscle tensions** (scalar stretch ratios) and a **jaw rigid body transform** as expression inputs, and decodes them to per-vertex mesh deltas. Contrasts with statistical PCA-based models: controls are biomechanically meaningful rather than abstract latent axes.

Source: `raw/assets/face model architecture.pdf` — design conversation log for this wiki's own face model project.

## Problem Statement
Given thousands of 3D head meshes in varied poses/expressions across multiple subjects, each with:
- A neutral pose per subject
- Fitted skull and mandible per mesh
- Extracted muscle lines per pose

**Goal**: represent each pose via biomechanically meaningful controls (muscle stretch scalars + jaw SE(3)) rather than statistical PCA axes, so that new poses can be generated from new control values.

## Architecture

### Input Encoding

**Identity code $z_{id}$** (64-dim, fixed per subject):
- PCA of neutral mesh vertex positions (scipy / PyTorch3d convention)
- 64 components capture sufficient variance (head shape, jaw width, orbital depth, etc.)
- Coefficients are fixed at inference — no gradient flows through identity during training

**Expression code** (47-dim):
- Jaw: SE(3) parameterized as quaternion (4) + translation (3) of mandible relative to skull
  - Quaternion is unit-normalized before concatenation
  - Translation normalized by per-subject skull scale for cross-subject comparability
- Muscles: scalar stretch ratios `len_posed / len_neutral` — raw ratios from Houdini, zero-mean normalized at runtime in DataLoader

### MLP Trunk
```
Linear(111)  →  LayerNorm → GELU
Linear(1024) →  LayerNorm → GELU
Linear(1024) →  LayerNorm → GELU
Linear(2048) →  LayerNorm → GELU
```
- Input dim: 64 (z_id) + 47 (expression) = 111
- **LayerNorm over BatchNorm**: stable at batch size 1 during inference
- **GELU over ReLU**: smoother gradients for mesh deformation
- Output layer is always linear (no activation) — deltas are signed

### Convolutional Upsampler (UV space)
MLP trunk output is reshaped into a UV-space feature map, then upsampled via Conv2d blocks to a 256×256 UV delta map:
```
Each block: Conv2d → GELU → Conv2d(64)
```

**UV space rationale**:
- Regular grid → convolutional inductive bias is valid
- Consistent UVs → same UV pixel = same semantic region across all subjects
- Bilinear interpolation handles vertex sampling implicitly (no barycentric baking needed)
- Single island → no cross-seam conv artifacts; seam is placed in low-deformation region

**Vertex extraction**:
```python
deltas = F.grid_sample(
    uv_delta_map,
    uv_coords,
    mode='bilinear',
    padding_mode='border',  # clean clamping at single boundary seam
    align_corners=True
)
```

### Parameter Budget
| Component | Parameters |
|-----------|-----------|
| MLP trunk (111→2048) | ~5M |
| Conv upsampler | ~7M |
| **Total** | **~12M** |

## Design Decisions Table

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Muscle representation | Scalar stretch ratio `len_posed / len_neutral` | Simple, interpretable, maps to muscle activation |
| Decoder | MLP + Conv upsample | Learns nonlinear muscle interactions |
| Jaw parameterization | Full SE(3), skull-relative | Handles cross-subject variation; network sees consistent frame |
| Identity/expression | Shared model, disentangled | Generalizes across subjects; swap expressions between identities |
| UV decoding | Single-island UV map, 256×256 | Consistent UVs across subjects, conv-friendly regular grid |
| Vertex count | ~30k, shared topology | Direct vertex correspondence, no template fitting needed |

## Loss Function
1. **Vertex L1**: per-vertex position error
2. **Laplacian loss**: per-vertex mean-of-neighbours deviation (precomputed adjacency on shared template topology) — penalises high-frequency surface noise
3. **Neutral anchor**: separate forward pass each batch with zeroed expression vector, supervised to produce zero deltas — forces decoder to treat neutral expression as identity
4. **Disentanglement (optional)**:
   - Expression swap consistency: identity A + expression B should produce consistent output
   - Orthogonality regularization: penalize correlation between $z_{id}$ and expression across batch

## Data Format

```
dataset.h5
└── subjects/
    └── <subject_id>/
        ├── neutral_verts     # neutral mesh vertices
        ├── skull_scale       # per-subject normalization scalar
        ├── identity_pca      # 64-dim PCA coefficients
        └── poses/
            ├── muscles       # stretch ratios (zero-mean normalized at runtime)
            ├── jaw_quat      # [x, y, z, w] skull-relative
            ├── jaw_trans     # skull-local frame, cm, normalized by skull scale
            └── delta_verts   # pre-subtracted in Houdini (no neutral lookup per pose)
```

One HDF5 file per split: `train.h5`, `val.h5`.

## Project Structure
```
face_model/
├── requirements.txt
├── config/train.yaml
├── data/
│   ├── dataset.py       # HDF5 Dataset + DataLoader factory
│   └── preprocess.py    # PCA neutral computation, UV coord baking
├── model/
│   ├── encoder.py       # neutral mesh PCA encoder
│   ├── decoder.py       # MLP trunk + conv upsample
│   └── model.py         # top-level FaceModel wrapper
└── training/
    ├── losses.py         # vertex L1, laplacian, neutral anchor
    ├── trainer.py        # train loop, validation, checkpointing
    ├── metrics.py        # per-region error, muscle correlation
    └── train.py          # entry point
```

## Training Notes
- UV delta maps can be logged as RGB images (zero delta = grey) — useful for debugging disentanglement early
- Expect: lips/jaw region activate for jaw poses, cheek region for smile muscles

## Next Steps (from doc)
1. Houdini data extraction — muscle stretch ratios, skull-relative jaw SE(3), vertex deltas, export to HDF5
2. UV sanity check — verify single island, seam in low-deformation region, bake per-vertex UV coords to `[-1, 1]`
3. Neutral PCA — compute on neutral meshes, confirm 64 components capture sufficient variance
4. Dataset class — HDF5 loader, runtime normalization of muscles and jaw trans
5. Training scaffold — loss functions, wandb logging

## Connections
- [[concepts/muscles]] — muscle lines as rig controls; this model uses extracted muscle lengths
- [[papers/bao-2019-face-capture-muscles]] — anatomy-based face capture using muscle activations (similar input space)
- [[papers/zeng-2021-neuromuscular-face]] — neuromuscular face control; directly related approach
- [[papers/cong-2015-anatomy-pipeline]] — automatically generating anatomical face simulation models
- [[concepts/latent-generative-modelling]] — UV-space convolutional decoder architecture inspired by latent diffusion VAE decoders
- [[concepts/nonlinear-face-models]] — this model is a nonlinear face model using biomechanical controls rather than PCA or implicit neural representations
- [[concepts/digital-human-appearance]] — same mesh topology used for appearance + deformation jointly
