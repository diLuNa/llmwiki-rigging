---
title: "HeadNeRF: A Real-time NeRF-based Parametric Head Model"
authors: [Hong, Yang; Peng, Bo; Xiao, Haiyao; Liu, Ligang; Zhang, Juyong]
venue: CVPR 2022
year: 2022
tags: [neural, digital-human, blendshapes, appearance, rig-generation]
source: raw/papers/2112.05637.pdf
---

## Summary
HeadNeRF replaces the textured mesh proxy of 3DMMs with a neural radiance field, parametrically controlled by identity, expression, and appearance codes. A 2D neural rendering integration reduces per-frame render time from ~5 s (vanilla NeRF) to ~25 ms on modern GPUs, enabling real-time synthesis. HeadNeRF captures fine-grained details absent from mesh-based models — gaps between teeth, wrinkles, beards — while retaining direct semantic control over expression and head pose.

## Problem
Mesh-based 3DMMs (FLAME, Basel) render fast but miss geometric detail bounded by mesh resolution and topology. Pure NeRF avatars are high-quality but slow (seconds per frame) and don't generalize across identities. A shared parametric model that is both high-quality *and* real-time, controllable by semantic latent codes, is missing.

## Method
**Parametric NeRF:** The radiance field is conditioned on latent codes $(\mathbf{z}_\text{id}, \mathbf{z}_\text{exp}, \mathbf{z}_\text{app})$ for identity, expression, and appearance respectively. A shared MLP backbone maps $(x, d, \mathbf{z})$ to $(RGB, \sigma)$.

**2D neural rendering integration:** Rather than full volumetric rendering at target resolution, HeadNeRF renders at low resolution and uses a 2D neural renderer (U-Net style) to upsample and refine. This amortizes the expensive ray marching into a small-resolution volume render + cheap 2D processing.

**Training:** Supervised on a multi-subject captured dataset with 3DMM-fitted codes as weak supervision for semantic control.

## Key Results
- 25 ms inference (real-time) vs 5 s for equivalent vanilla NeRF.
- Better detail than mesh-based 3DMMs: visible teeth gaps, skin wrinkles, hair.
- Semantic control over expression and pose via latent interpolation.

## Limitations
- Expression control via continuous latent, not FACS AUs — not directly compatible with standard production rig workflows.
- Requires multi-view training data per subject for high-quality personalization.
- 2D upsampling step introduces some temporal flickering under animation.

## Connections
- [[concepts/nonlinear-face-models]] — parametric NeRF as alternative to mesh-based 3DMMs; precedes GaussianAvatars
- [[papers/zhuang-2022-mofanerf]] — MoFaNeRF is the closest prior: also a morphable NeRF, but without real-time rendering
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars replaces NeRF rendering with 3DGS for similar goals
- [[papers/li-2017-flame]] — FLAME used for weak semantic supervision of expression codes
