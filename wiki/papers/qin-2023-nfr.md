---
title: "Neural Face Rigging for Animating and Retargeting Facial Meshes in the Wild"
authors: [Qin, Dafei; Saito, Jun; Aigerman, Noam; Groueix, Thibault; Komura, Taku]
venue: ACM SIGGRAPH 2023
year: 2023
tags: [rig-generation, blendshapes, neural, digital-human, facial-capture, auto-rigging]
source: raw/papers/2305.08296v1.pdf
---

## Summary
Neural Face Rigging (NFR) learns to rig and retarget 3D facial meshes of arbitrary topology without manual blendshape creation or correspondence. A deformation autoencoder encodes a neutral identity mesh and an expression mesh separately, then decodes via Neural Jacobian Fields (NJF) to produce per-triangle deformation Jacobians. The expression latent space is split into FACS-regularized interpretable dimensions ($z_\text{FACS}$, 53-dim) and freely-learned residual dimensions ($z_\text{ext}$, 75-dim). A two-stage training scheme uses ICT FaceKit (synthetic, FACS-labeled) to establish interpretable controls, then Multiface (real 4D scans) to add fine-grained expression detail.

## Problem
Template-based blendshape rigging requires matching topology and dense correspondences. Existing auto-rigging either loses interpretability (PCA modes) or requires manual sculpts. No prior method rigs arbitrary in-the-wild meshes while maintaining human-editable FACS semantics.

## Method
**Identity encoder** $DN_i$: DiffusionNet on per-vertex $(v, n)$ features + front-view CNN rendering features → 100-dim identity code $z_i$.

**Expression encoder** $DN_e$: same architecture → 128-dim expression code:
```math
z_e = [z_\text{FACS};\; z_\text{ext}] \in \mathbb{R}^{53+75}
```
$z_\text{FACS}$ supervised to match ground-truth ARKit FACS values; $z_\text{ext}$ regularized toward zero.

**Decoder (NJF)**: Per-triangle MLP taking triangle center/normal features, $z_i$, $z_e$, and shape code $c_i$ → 3×3 Jacobian $g^*$ per face. Mesh positions recovered from Jacobians via a Poisson solve.

**Loss (Stage 1, ICT FaceKit):**
```math
\mathcal{L} = \lambda_e \|\hat{z}_\text{FACS} - z^*_\text{FACS}\|^2 + \lambda_v \|v_e - v^*_e\|^2 + \lambda_g \|g - g^*\|^2 + \lambda_n \|n_e - n^*_e\|^2
```
**Stage 2** fine-tunes on Multiface real scans with expression-range regularization on $z_\text{FACS}$.

## Key Results
On ICT-Real-AU inverse rigging: mean error 0.443 mm (vs 0.688 mm for Seol et al.; 34% improvement).
On Multiface expression quality: mean 0.879 mm, 32% better Q95 than SpiralNet++.
Triangulation-invariant: performance unchanged when mesh resolution doubles (0.443 vs 0.444 mm).
Successfully retargets expressions across FaceWarehouse, Triplegangers, raw scans, MetaHuman.

## Limitations
- Requires manual removal of internal geometry (eye sockets, mouth cavity) before processing
- Trained for ARKit FACS; other rig parameterizations not evaluated
- ICT FaceKit linear rig limits base expression capability; nonlinear residuals come from Multiface fine-tuning
- No support for meshes with multiple disconnected components (see [[papers/ma-2025-riganyface]])

## Connections
- [[papers/ma-2025-riganyface]] — RigAnyFace extends NFR: disconnected components + 2D-supervised scaling
- [[papers/choi-2022-animatomy]] — Animatomy is a production rig that NFR can drive via retargeting
- [[papers/canrig-2026-neural-face-rigging]] — CANRIG (EG 2026) is a concurrent approach using cross-attention
- [[papers/sumner-2004-deformation-transfer]] — deformation transfer is the classical alternative (requires correspondences)
- [[concepts/auto-rigging]] — NFR is the main neural facial auto-rigging reference
- [[concepts/blendshapes]] — output rig is FACS-compatible blendshape space
- [[authors/saito-jun]]
