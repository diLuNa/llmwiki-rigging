---
title: "MoFaNeRF: Morphable Facial Neural Radiance Field"
authors: [Zhuang, Yiyu; Zhu, Hao; Sun, Xusen; Cao, Xun]
venue: ECCV 2022
year: 2022
tags: [neural, digital-human, blendshapes, rig-generation, appearance]
source: raw/papers/2112.02308.pdf
---

## Summary
MoFaNeRF is the first facial parametric model built entirely on a neural radiance field. It maps facial shape code, expression code, appearance code, 3D coordinate, and view direction jointly through an MLP to radiance — creating a continuous morphable space with photorealistic detail for eyes, mouth, and facial hair that conventional 3DMMs cannot reproduce. A single shared model supports image-based fitting, face generation, expression rigging, semantic editing, and novel-view synthesis.

## Problem
Classical 3DMMs (FLAME, Basel) are separate from appearance models and cannot reproduce photorealistic facial detail. NeRF-based avatars are per-subject — not shared models. A single morphable neural model that spans identity, expression, and view-dependent appearance — all in one differentiable representation — would unify reconstruction, generation, and editing.

## Method
**Factored MLP:**
```
f(x, d, z_shape, z_expr, z_app) → (RGB, σ)
```
where:
- $\mathbf{z}_\text{shape} \in \mathbb{R}^{d_s}$: identity/shape latent
- $\mathbf{z}_\text{expr} \in \mathbb{R}^{d_e}$: expression latent
- $\mathbf{z}_\text{app} \in \mathbb{R}^{d_a}$: per-subject appearance (hair color, skin tone)
- $(\mathbf{x}, \mathbf{d})$: 3D point + view direction (standard NeRF)

The MLP is trained on a multi-subject dataset with known 3DMM parameters as weak shape/expression supervision and appearance reconstructed from multi-view images.

**Identity-specific modulation:** Each subject's $\mathbf{z}_\text{app}$ modulates feature activations via FiLM conditioning, enabling appearance variation independent of geometry codes.

**Applications:** Fitting by optimizing latent codes to match input image; editing by interpolating codes; rigging by changing $\mathbf{z}_\text{expr}$.

## Key Results
- First unified NeRF-based morphable face model supporting all of: fitting, generation, rigging, editing, novel-view synthesis.
- Superior to mesh-based 3DMMs on photorealistic detail (eyes, mouth interior, facial hair).
- Code and data publicly available.

## Limitations
- NeRF rendering is slow (~seconds per frame) — not real-time.
- Expression control is via latent code interpolation, not FACS-compatible — not directly usable with existing animation pipelines.
- Mesh extraction from NeRF requires marching cubes; geometry quality depends on volume density.

## Connections
- [[concepts/nonlinear-face-models]] — foundational NeRF-based morphable face model; predates GaussianAvatars by two years
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars replaces NeRF rendering with 3DGS for real-time performance
- [[papers/giebenhain-2023-nphm]] — NPHM uses SDF (not NeRF) for geometry but shares the parametric-neural-field idea
- [[papers/li-2017-flame]] — FLAME provides weak supervision for shape/expression codes during training
