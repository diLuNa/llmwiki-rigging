---
title: "GaussianAvatars: Photorealistic Head Avatars with Rigged 3D Gaussians"
authors: [Qian, Shenhan; Kirschstein, Tobias; Schoneveld, Liam; Davoli, Davide; Giebenhain, Simon; Nießner, Matthias]
venue: CVPR 2024
year: 2024
tags: [neural, digital-human, blendshapes, rig-generation, appearance]
source: raw/papers/2312.02069.pdf
---

## Summary
GaussianAvatars binds 3D Gaussian splats to local coordinate frames of FLAME mesh triangles, creating a hybrid rig-driven avatar: when FLAME expression/pose parameters change, each Gaussian translates, rotates, and scales accordingly through the triangle's local frame. Gaussian displacement offsets are optimized to capture fine detail beyond FLAME mesh resolution. The result is a photorealistic, real-time-renderable avatar with full rig-based expression control and identity from a short multi-view video capture.

## Problem
NeRF-based head avatars are photorealistic but slow to render and often have imprecise expression control. Mesh-based rigs have precise control but limited geometric detail. 3D Gaussian splatting is fast but lacks a semantic control structure. GaussianAvatars bridges this: rig the Gaussians to FLAME to inherit its control space, then let them optimize offsets for appearance detail beyond the mesh.

## Method
**Binding:** Each Gaussian $g_i$ is attached to a FLAME triangle $T_k$. The Gaussian's world-space position and orientation are computed as:
```math
\mu_i^w = R_k \mu_i^{local} + t_k
```
where $(R_k, t_k)$ is the local frame of triangle $T_k$ in FLAME's posed space. As FLAME deforms (expression, pose change), all Gaussians rigidly follow their parent triangle.

**Offset optimization:** Local position $\mu_i^{local}$, opacity, and covariance are optimized per-Gaussian during reconstruction from multi-view video. This lets Gaussians drift from the mesh surface to capture hair, eyelashes, teeth, and other fine geometry.

**End-to-end training:** FLAME parameters (shape $\beta$, expression $\psi$, pose $\theta$) and Gaussian parameters jointly optimized via differentiable Gaussian splatting.

## Key Results
- Photorealistic quality with real-time rendering (Gaussian splatting).
- Full expression control via FLAME expression parameters — transferable to new expressions and identities.
- Video-driven reenactment outperforms prior NeRF-based avatar methods visually.
- CVPR 2024 Highlight paper.

## Limitations
- Requires multi-view video capture for per-subject training — not a generalizable model.
- Gaussians are bound to FLAME triangles — topology mismatches between Gaussians and true geometry (hair, beard) must be absorbed by offset optimization.
- Expression control is FLAME-quality only; subtle expressions not in FLAME's basis are lost.

## Connections
- [[concepts/nonlinear-face-models]] — hybrid rig + Gaussian representation; Gaussians provide neural appearance on top of parametric control
- [[concepts/facial-blendshape-rigs]] — FLAME expression parameters are the control interface
- [[papers/li-2017-flame]] — FLAME provides the rigged mesh backbone
- [[papers/giebenhain-2023-nphm]] — NPHM replaces FLAME backbone in NPGA (successor)
- [[papers/giebenhain-2024-npga]] — successor: conditions Gaussians on NPHM instead of FLAME
- [[papers/ma-2024-gaussian-blendshapes]] — concurrent work: explicit Gaussian blendshape bases
- [[authors/niessner-matthias]]

## Implementation Notes
The binding to triangle local frames is the key implementation detail. Each Gaussian stores its local-frame position and orientation relative to its parent triangle. During rendering, a single transform per triangle (from FLAME's skinning) propagates to all attached Gaussians — computationally cheap once FLAME is evaluated. Compatible with standard 3DGS rendering pipelines.
