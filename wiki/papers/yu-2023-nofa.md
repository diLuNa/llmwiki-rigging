---
title: "NOFA: NeRF-based One-shot Facial Avatar Reconstruction"
authors: [Yu, Wangbo; Fan, Yanbo; Zhang, Yong; Wang, Xuan; Yin, Fei; Bai, Yunpeng; Cao, Yan-Pei; Shan, Ying; Wu, Yang; Sun, Zhongqian; Wu, Baoyuan]
venue: SIGGRAPH 2023
year: 2023
tags: [neural, digital-human, blendshapes, facial-capture, appearance]
source: raw/papers/2307.03441.pdf
---

## Summary
NOFA reconstructs a NeRF-based controllable facial avatar from a *single* source image, bypassing per-subject multi-view training by leveraging the generative prior of a pretrained 3D-aware GAN (EG3D). GAN inversion maps the input image into the GAN's canonical neural volume; a deformation field provides expression control; a compensation network adds fine facial detail. Expression transfer from any driving video runs at inference without subject-specific retraining.

## Problem
Subject-specific NeRF avatars require minutes-to-hours of multi-view video capture and training per identity. Generalizable NeRF avatars trained across identities sacrifice quality. A one-shot method that matches or exceeds subject-specific quality by exploiting a pretrained generative prior would enable scalable avatar creation from a single photo.

## Method
**3D GAN prior (EG3D):** EG3D pretrains a triplane-based neural volume on large-scale face datasets, encoding a strong prior over plausible 3D face appearance and geometry.

**GAN inversion encoder:** Encodes the input image into EG3D's latent space $\mathbf{w}$ — the canonical neural volume for that identity. This bypasses per-subject NeRF training.

**Expression deformation field:** A learned deformation network maps expression codes (from a FLAME tracker on the driving video) to canonical-volume warp fields, enabling expression transfer.

**Detail compensation network:** A residual MLP adds fine-scale detail (pores, wrinkles) not captured in the GAN's latent.

## Key Results
- Competitive with subject-specific NeRF avatars using only a single input image.
- Supports cross-identity expression reenactment from video.
- Significant inference speed advantage over per-subject training methods.

## Limitations
- Quality bounded by EG3D's generative prior — unusual identities (heavy makeup, facial hair) may not invert well.
- Expression control via FLAME — same expression-space limitations apply.
- Not truly real-time (NeRF volume rendering still slow vs Gaussian splatting).

## Connections
- [[concepts/nonlinear-face-models]] — one-shot NeRF avatar using GAN inversion; avoids per-subject training
- [[papers/zhuang-2022-mofanerf]] — MoFaNeRF is a morphable NeRF model (shared across identities); NOFA uses GAN inversion for per-identity adaptation
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars requires multi-view capture but achieves real-time rendering
- [[papers/feng-2021-deca]] — DECA/FLAME used for expression coefficient extraction from driving video
