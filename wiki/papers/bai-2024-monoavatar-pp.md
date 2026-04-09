---
title: "Efficient 3D Implicit Head Avatar with Mesh-anchored Hash Table Blendshapes"
authors: [Bai, Ziqian; Tan, Feitong; Fanello, Sean; Pandey, Rohit; Dou, Mingsong; Liu, Shichen; Tan, Ping; Zhang, Yinda]
venue: CVPR 2024
year: 2024
tags: [neural, digital-human, blendshapes, facial-capture, appearance]
source: raw/papers/2404.01543.pdf
---

## Summary
MonoAvatar++ replaces MonoAvatar's NeRF volume rendering with per-vertex hash-table blendshapes attached to FLAME mesh vertices: CNN-predicted expression-dependent weights linearly blend per-vertex spatial hash features, which are decoded by a lightweight MLP. Hierarchical nearest-neighbor search accelerates lookup, achieving >30 FPS rendering at 512×512 while maintaining challenging-expression quality that slower NeRF-based methods can't match. The direct follow-up to MonoAvatar.

## Problem
MonoAvatar achieves high quality but NeRF volume rendering is slow. Existing real-time methods sacrifice quality on complex expressions. A hybrid that preserves expression fidelity — especially for subtle and extreme expressions — at real-time speed is missing.

## Method
**Mesh-anchored hash tables:** Each FLAME vertex has a local spatial hash table storing volumetric feature grids (position-dependent). These are the "blendshapes" — not mesh offsets, but *feature offsets* in neural implicit space.

**Expression-dependent blending:** A CNN predicts per-vertex blending weights $w_v(\psi)$ as a function of FLAME expression code $\psi$. The effective feature at any 3D sample is a weighted sum of nearby vertex hash features:
```math
f(\mathbf{x}, \psi) = \sum_v w_v(\psi) \cdot h_v(\mathbf{x})
```
where $h_v(\mathbf{x})$ is the hash-table lookup at vertex $v$.

**Hierarchical nearest-neighbor search:** At query time, only nearby vertices are considered (spatial culling), enabling sub-linear lookup cost.

**Lightweight MLP decoder:** Maps $(f, \text{direction})$ → $(RGB, \sigma)$. Compact enough for >30 FPS.

## Key Results
- >30 FPS at 512×512 on modern GPU (vs <1 FPS for NeRF equivalent).
- Maintains quality advantage of MonoAvatar on complex expressions.
- CVPR 2024.

## Limitations
- Per-subject training — not a generalizable avatar model.
- Expression control via FLAME — expression space limitations apply.
- Hash table blendshapes are in feature space, not vertex space — less interpretable than mesh blendshapes.

## Connections
- [[concepts/nonlinear-face-models]] — real-time implicit head avatar via neural blendshapes in feature space
- [[concepts/blendshapes]] — the hash-table blending is a neural analogue of mesh blendshape evaluation
- [[papers/bai-2023-monoavatar]] — direct predecessor; replaces NeRF with this approach
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars achieves similar real-time goals with 3DGS
- [[papers/li-2017-flame]] — FLAME provides the mesh anchor and expression conditioning
