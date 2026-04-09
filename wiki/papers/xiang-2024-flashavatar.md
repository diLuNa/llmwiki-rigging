---
title: "FlashAvatar: High-fidelity Head Avatar with Efficient Gaussian Embedding"
authors: [Xiang, Jun; Gao, Xuan; Guo, Yudong; Zhang, Juyong]
venue: CVPR 2024
year: 2024
tags: [neural, digital-human, blendshapes, appearance]
source: raw/papers/2312.02214.pdf
---

## Summary
FlashAvatar embeds a uniform 3D Gaussian field on the surface of a parametric face model (FLAME), with learned spatial offsets to model non-surface regions (hair, eyelashes). Leveraging FLAME's geometry prior and careful initialization, the method reduces the Gaussian count needed for quality output, enabling reconstruction from monocular video in minutes and rendering at 300 FPS on a consumer GPU — the most speed-focused 3DGS head avatar, directly comparable to GaussianAvatars and NPGA.

## Problem
Prior 3DGS head avatars (GaussianAvatars) bind Gaussians tightly to mesh triangles, inheriting FLAME's limited geometry. Methods that learn Gaussian positions freely need many more Gaussians and longer training. A method that uses FLAME as a geometric prior for efficient initialization without being topologically constrained to the mesh is missing.

## Method
**Surface-embedded Gaussian field:** Gaussians are initialized uniformly across the FLAME mesh surface. Each Gaussian stores a learned offset from its surface anchor point, allowing it to model geometry above the mesh (hair, eyelashes, skin pores).

**FLAME expression conditioning:** Gaussians' world-space positions are updated per-expression by applying FLAME's LBS transforms to their anchor points, then adding the learned offset. This gives expression control with minimal compute.

**Efficient initialization:** Starting from a well-distributed surface initialization reduces the number of Gaussians needed to cover the head, keeping the rendering fast (300 FPS at ~100K Gaussians).

## Key Results
- 300 FPS rendering on consumer GPU.
- Minutes-to-reconstruct from monocular video.
- Outperforms prior 3DGS head avatars on perceptual quality metrics.
- CVPR 2024.

## Limitations
- Offset optimization is local — large-scale geometry deviations from FLAME (extreme hair, accessories) require many offset-Gaussians.
- Expression control bounded by FLAME.
- Per-subject model — not generalizable.

## Connections
- [[concepts/nonlinear-face-models]] — surface-embedded 3DGS head avatar; speed-focused
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars binds Gaussians to triangles (tighter coupling); FlashAvatar uses surface anchors with offsets
- [[papers/ma-2024-gaussian-blendshapes]] — Gaussian Blendshapes uses explicit blendshape bases; FlashAvatar uses FLAME LBS directly
- [[papers/giebenhain-2024-npga]] — NPGA uses NPHM expression space for broader expressiveness
- [[papers/li-2017-flame]] — FLAME geometric prior and expression control
