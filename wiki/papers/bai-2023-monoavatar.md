---
title: "Learning Personalized High Quality Volumetric Head Avatars from Monocular RGB Videos"
authors: [Bai, Ziqian; Tan, Feitong; Huang, Zeng; Sarkar, Kripasindhu; Tang, Danhang; Qiu, Di; Meka, Abhimitra; Du, Ruofei; Dou, Mingsong; Orts-Escolano, Sergio; Pandey, Rohit; Tan, Ping; Beeler, Thabo; Fanello, Sean; Zhang, Yinda]
venue: CVPR 2023
year: 2023
tags: [neural, digital-human, blendshapes, facial-capture, appearance]
source: raw/papers/2304.01436.pdf
---

## Summary
MonoAvatar combines 3DMM geometry priors with a neural radiance field through localized CNN features anchored to the 3D morphable model surface. Features are predicted in UV space (capturing spatial topology), deformed with the 3DMM, and spatially interpolated at NeRF query points. This anchoring reduces over-smoothing and improves expression generalization compared to purely implicit or mesh-based approaches. From Google — demonstrates high-quality avatars from 1-minute monocular capture.

## Problem
Pure NeRF avatars lose spatial coherence under novel expressions (no mesh prior). Pure mesh-based avatars lack fine-grained detail. A hybrid that uses 3DMM geometry for structural regularization while letting a NeRF capture appearance detail, with fast training from short monocular video, is missing.

## Method
**UV-space feature CNN:** A CNN operates in the UV parameterization of the 3DMM, predicting per-vertex feature vectors. The UV space preserves spatial topology — nearby face regions stay nearby in feature space.

**3DMM-anchored deformation:** UV features are attached to 3DMM vertices. When the 3DMM deforms (expression/pose change), features deform with it via mesh skinning. NeRF samples look up their nearest-vertex feature by spatial interpolation.

**NeRF rendering:** An MLP maps (sample position, view direction, deformed feature) → (RGB, density). Volume rendered at target resolution.

**Training:** From ~1 minute monocular video; 3DMM parameters tracked per-frame as conditioning.

## Key Results
- Superior expression detail and generalization vs FLAME-mesh-only or pure NeRF baselines.
- High quality from short (1-minute) monocular capture.
- Google production pipeline context — tested on broadcast-quality video.

## Limitations
- Expression control bounded by 3DMM expressiveness.
- UV-CNN requires fixed 3DMM topology — not generalizable to arbitrary mesh.
- Still a per-subject model; not generalizable across identities.

## Connections
- [[concepts/nonlinear-face-models]] — 3DMM-anchored NeRF hybrid avatar
- [[papers/bai-2024-monoavatar-pp]] — direct follow-up replacing NeRF with hash-table blendshapes for real-time
- [[papers/zielonka-2023-insta]] — concurrent: also anchors NeRF to FLAME; different anchoring strategy
- [[papers/li-2017-flame]] — 3DMM backbone
- [[authors/beeler-thabo]]
