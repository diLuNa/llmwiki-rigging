---
title: "PointAvatar: Deformable Point-based Head Avatars from Videos"
authors: [Zheng, Yufeng; Yifan, Wang; Wetzstein, Gordon; Black, Michael J.; Hilliges, Otmar]
venue: CVPR 2023
year: 2023
tags: [neural, digital-human, blendshapes, facial-capture, appearance]
source: raw/papers/2212.08377.pdf
---

## Summary
PointAvatar represents a head avatar as a deformable point cloud that disentangles intrinsic albedo from normal-dependent shading, bridging the topological flexibility of implicit representations and the efficiency of explicit point-based rendering. Trained from monocular video (smartphone or webcam), it handles cases where mesh-based and NeRF-based methods fail — thin hair strands, accessories, non-FLAME head geometry — while training significantly faster than competing approaches.

## Problem
Mesh-based avatars (FLAME-based) cannot represent hair, accessories, or topology changes. NeRF-based avatars have flexible topology but are slow and sensitive to initialization. A representation that combines topological flexibility with fast training and explicit controllability is missing.

## Method
**Deformable point cloud:** Points are defined in a canonical space; a FLAME-conditioned deformation field maps them to posed space. Each point stores albedo and a compact local feature for normal-dependent shading.

**Albedo-shading disentanglement:** Point color = albedo × shading. Shading is modeled as a function of normal orientation (view-dependent), separating intrinsic material (albedo) from lighting effects. This prevents baking lighting into texture — enabling relighting and better generalization.

**Expression conditioning:** A FLAME expression code drives the canonical-to-posed deformation field. Expressions outside FLAME's basis are approximated by learned residuals.

**Training:** From monocular video using differentiable point rasterization + photometric loss.

## Key Results
- State-of-the-art on in-the-wild monocular video reconstruction, especially on challenging cases (thin hair, accessories).
- Faster training than NeRF-based methods.
- Albedo-shading disentanglement enables relighting.

## Limitations
- Point cloud representation: no explicit surface normal — shading quality depends on point density.
- FLAME deformation backbone — expressions bounded by FLAME's expressiveness.
- Less sharp than Gaussian splatting-based methods at comparable point counts.

## Connections
- [[concepts/nonlinear-face-models]] — point-based avatar bridging mesh and implicit representations
- [[papers/giebenhain-2023-nphm]] — NPHM uses SDF for comparable topology flexibility
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars uses 3DGS (similar point-based idea, different rendering)
- [[authors/black-michael]]
