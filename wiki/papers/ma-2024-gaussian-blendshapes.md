---
title: "3D Gaussian Blendshapes for Head Avatar Animation"
authors: [Ma, Shengjie; Weng, Yanlin; Shao, Tianjia; Zhou, Kun]
venue: ACM SIGGRAPH 2024
year: 2024
tags: [neural, digital-human, blendshapes, rig-generation, appearance]
source: raw/papers/2404.19398.pdf
---

## Summary
A direct 3D Gaussian analogue of classical mesh blendshapes: a neutral Gaussian point cloud plus per-expression Gaussian offset bases, linearly blended by expression coefficients — the 3DGS equivalent of $M(\alpha) = M_0 + \sum_i \alpha_i \Delta_i$. Reconstructed from monocular video, the avatar renders at ~370 fps (14× faster than NeRF blendshape baselines) while capturing high-frequency appearance detail beyond what mesh-based rigs express. Expression coefficients map directly to standard FACS-compatible parametric model controls.

## Problem
Existing 3DGS avatars either lack explicit expression control or require complex deformation fields. Mesh-based blendshape rigs have direct expression control but cannot represent hair, translucency, or fine geometry. A 3DGS avatar with the *same evaluation semantics* as a blendshape rig — linear combination of per-expression delta point clouds — combines real-time rendering with semantic controllability.

## Method
**Representation:**
- Neutral Gaussian set $G_0$: $N$ Gaussians with position, opacity, covariance, color (SH).
- Expression blendshapes $\{G_i\}_{i=1}^K$: per-expression Gaussian offset bases ($\Delta\mu_i$, $\Delta$opacity, $\Delta$covariance).
- Driven avatar: $G(\alpha) = G_0 + \sum_{i=1}^K \alpha_i G_i$ — identical structure to mesh blendshapes.

**Reconstruction from monocular video:**
1. Initialize neutral Gaussians from SfM point cloud.
2. Fit expression coefficients $\alpha$ per frame using a parametric face tracker.
3. Jointly optimize $G_0$ and $\{G_i\}$ via Gaussian splatting photometric loss.

Expression coefficients $\alpha$ come from a standard face tracker (DECA/EMOCA-style) — not trained end-to-end.

## Key Results
- ~370 fps rendering (RTX 3090) — 14× faster than NeRF-based blendshape avatars.
- Captures high-frequency detail (eyelashes, teeth, hair) absent from mesh rigs.
- Comparable or better expression fidelity vs prior 3DGS avatar methods.
- ACM SIGGRAPH 2024.

## Limitations
- Linear blending in Gaussian space: same algebraic structure as mesh blendshapes, so the same interaction/corrective limitations apply (blending two expressions produces an average, not physically correct combined expression).
- Requires per-subject training from video — not generalizable.
- Expression coefficient source (face tracker) is a separate system; errors in tracking propagate to avatar.

## Connections
- [[concepts/nonlinear-face-models]] — 3DGS blendshape representation as an alternative to mesh-based avatars
- [[concepts/facial-blendshape-rigs]] — direct Gaussian analogue of the blendshape evaluation formula
- [[concepts/blendshapes]] — same $M_0 + \sum \alpha_i \Delta_i$ structure applied to Gaussians
- [[papers/qian-2024-gaussian-avatars]] — concurrent work: binds Gaussians to FLAME triangles rather than explicit blendshape bases
- [[papers/feng-2021-deca]] — DECA/EMOCA used for tracking expression coefficients at train time
- [[authors/niessner-matthias]]

## Implementation Notes
The blendshape evaluation in Gaussian space is computationally trivial — same BLAS operations as mesh blendshapes, just on position/opacity/covariance arrays instead of vertex positions. The bottleneck is the Gaussian splatting rasterizer, which runs at 370 fps with ~100K Gaussians. Expression coefficient inference is separate (any FLAME tracker).
