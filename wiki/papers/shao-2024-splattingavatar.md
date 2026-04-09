---
title: "SplattingAvatar: Realistic Real-Time Human Avatars with Mesh-Embedded Gaussian Splatting"
authors: [Shao, Zhijing; Wang, Zhaolong; Li, Zhuang; Wang, Duotun; Lin, Xiangru; Zhang, Yu; Fan, Mingming; Wang, Zeyu]
venue: CVPR 2024
year: 2024
tags: [neural, digital-human, blendshapes, skinning, appearance]
source: raw/papers/2403.05087.pdf
---

## Summary
SplattingAvatar defines Gaussians via barycentric coordinates and displacement on triangle mesh surfaces (Phong surfaces), cleanly separating low-frequency mesh motion from high-frequency Gaussian appearance. A lifted optimization scheme simultaneously refines Gaussian and mesh parameters. The method achieves >300 FPS for both full-body and head avatars trained from monocular video. Unlike GaussianAvatars, Gaussians are not rigidly tied to triangle frames — the barycentric + displacement parameterization allows smooth interpolated motion across the mesh.

## Problem
GaussianAvatars binds each Gaussian rigidly to one triangle — this causes visible seam artifacts at triangle boundaries as Gaussians don't interpolate smoothly across the mesh. A smoother Gaussian-mesh coupling that inherits all mesh animation capabilities (skeletal animation, blendshapes, mesh editing) while remaining real-time is missing.

## Method
**Phong surface embedding:** Each Gaussian is parameterized by a barycentric coordinate $(u, v, w)$ on a triangle plus a displacement $d$ along the surface normal. Position in world space:
```math
\mu = u \cdot v_0 + v \cdot v_1 + w \cdot v_2 + d \cdot \hat{n}
```
This places the Gaussian smoothly on the interpolated surface, not rigidly at a triangle centroid.

**Orientation from Phong normal:** The Gaussian's orientation tracks the Phong-interpolated surface normal, ensuring appearance is consistent with the local surface orientation.

**Lifted optimization:** Both mesh parameters (deformation) and Gaussian parameters (offsets, opacity, covariance, SH) are jointly optimized via gradient flow through the differentiable Gaussian rasterizer.

**Animation:** Supports any mesh animation mode — skeletal LBS, blendshapes, direct mesh editing — since Gaussians are expressed in barycentric coordinates, not world-space.

## Key Results
- >300 FPS (head), >30 FPS mobile (full body).
- State-of-the-art rendering quality for monocular-video-trained avatars.
- Works for both face and full-body avatars.
- Supports skeletal animation, blendshapes, and direct mesh editing.
- CVPR 2024.

## Limitations
- Requires triangle mesh backbone — not topology-agnostic.
- Mesh must be animated by some external rig; SplattingAvatar provides the rendering layer, not the rig.
- Per-subject training.

## Connections
- [[concepts/nonlinear-face-models]] — barycentric mesh-embedded 3DGS avatar
- [[concepts/blendshapes]] — explicitly supports blendshape animation of the underlying mesh
- [[concepts/linear-blend-skinning]] — supports LBS animation of the underlying mesh
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars uses per-triangle rigid binding; SplattingAvatar uses smooth barycentric embedding
- [[papers/xiang-2024-flashavatar]] — concurrent 3DGS head avatar with surface embedding
