---
title: "NPGA: Neural Parametric Gaussian Avatars"
authors: [Giebenhain, Simon; Kirschstein, Tobias; Rünz, Martin; Agapito, Lourdes; Nießner, Matthias]
venue: SIGGRAPH Asia 2024
year: 2024
tags: [neural, digital-human, blendshapes, rig-generation, appearance]
source: raw/papers/2405.19331.pdf
---

## Summary
NPGA conditions 3D Gaussian avatar dynamics on the NPHM neural parametric head model rather than mesh-based 3DMMs (FLAME), unlocking broader expression capability — including hair, ears, and non-FLAME shapes — while remaining driveable from monocular video. A backward-to-forward deformation field distillation step makes NPHM's deformation compatible with Gaussian splatting. Per-Gaussian latent features enable fine expression-dependent appearance detail. Outperforms prior Gaussian avatar methods by ~2.6 dB PSNR.

## Problem
GaussianAvatars and similar methods bind Gaussians to FLAME triangles, inheriting FLAME's limited shape and expression space (no hair, teeth poorly handled, capped at 50 expression PCA components). NPHM's richer expression space could unlock better avatars, but NPHM uses backward deformation fields (canonical → posed) incompatible with Gaussian splatting's forward rendering.

## Method
**NPHM expression conditioning:** Each Gaussian is driven by the NPHM expression code $\mathbf{z}_\text{exp}$ via a learned MLP that outputs per-Gaussian position offsets $\delta\mu_i(\mathbf{z}_\text{exp})$.

**Backward-to-forward distillation:** NPHM's backward deformation field $f_\text{exp}^{-1}$ is distilled into a forward-compatible deformation by sampling the backward field at canonical positions and inverting locally via a learned forward network. This is necessary for Gaussian splatting (which needs world-space Gaussian positions).

**Per-Gaussian latent features:** Each Gaussian carries a small feature vector $\mathbf{h}_i$ fed into a tiny MLP alongside $\mathbf{z}_\text{exp}$ to predict color and opacity changes — capturing expression-dependent shading (teeth visibility, eye glint changes).

**Training:** NeRSemble multi-view video dataset; joint optimization of Gaussian params and NPHM expression codes per frame.

## Key Results
- +2.6 dB PSNR vs prior Gaussian avatar methods on NeRSemble.
- Better expression generalization than FLAME-conditioned methods on extreme expressions.
- Animatable from monocular video at inference.

## Limitations
- Requires NPHM as a prerequisite (multi-view scan dataset for NPHM training is not publicly available at scale).
- Backward-to-forward distillation introduces approximation error for large deformations.
- Per-subject training; not a generalizable reconstruction method.

## Connections
- [[concepts/nonlinear-face-models]] — NPHM-conditioned Gaussian avatar; successor to GaussianAvatars
- [[papers/giebenhain-2023-nphm]] — NPHM provides the expression conditioning space
- [[papers/qian-2024-gaussian-avatars]] — predecessor: FLAME-conditioned 3DGS avatars
- [[papers/ma-2024-gaussian-blendshapes]] — concurrent: explicit Gaussian blendshape bases (FLAME-based)
- [[authors/niessner-matthias]]
