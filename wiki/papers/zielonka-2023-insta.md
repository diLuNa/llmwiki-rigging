---
title: "Instant Volumetric Head Avatars"
authors: [Zielonka, Wojciech; Bolkart, Timo; Thies, Justus]
venue: CVPR 2023
year: 2023
tags: [neural, digital-human, blendshapes, facial-capture, appearance]
source: raw/papers/2211.12499.pdf
---

## Summary
INSTA (Instant Neural STandard Avatar) wraps an Instant-NGP hash-grid neural radiance field around FLAME mesh correspondences, enabling photorealistic head avatar reconstruction in under 10 minutes on a single GPU from a single monocular RGB video. FLAME's geometry provides a structural prior that regularizes the NeRF, giving controllable expression and pose synthesis while the NeRF captures detail beyond mesh resolution. From the same author as MICA — creates a direct MICA→INSTA pipeline pairing for metric identity then volumetric detail.

## Problem
Subject-specific NeRF avatars require hours of training and minutes of dense multi-view capture per subject. FLAME-based avatars train quickly but lack NeRF's photorealistic detail. A method that achieves NeRF-level quality in minutes from a short monocular video is missing.

## Method
**Hybrid representation:** A FLAME mesh provides the articulation skeleton and approximate geometry. An Instant-NGP hash-grid NeRF (with learned hash features) is anchored to FLAME's surface coordinates, providing per-point density and color conditioned on local mesh context.

**FLAME anchoring:** NeRF query points are transformed into FLAME's canonical surface coordinate system before hash-grid lookup. When FLAME deforms (new expression/pose), all NeRF samples deform accordingly — expression control comes for free.

**Training speed:** Instant-NGP's multi-resolution hash grids provide extremely fast feature lookup. Combined with a short (few-minute) capture, reconstruction completes in <10 minutes.

## Key Results
- <10 min reconstruction from monocular video.
- Better rendering quality than prior fast-reconstruction methods.
- Controllable expression and pose via FLAME parameters.
- Natural companion to MICA (same authors): MICA → identity shape → INSTA → volumetric avatar.

## Limitations
- Expression control bounded by FLAME's parametric space.
- Hash-grid NeRF can't represent very thin geometry (hair strands, eyelashes) well.
- Monocular capture — back-of-head reconstruction is extrapolated, not captured.

## Connections
- [[concepts/nonlinear-face-models]] — fast FLAME-anchored NeRF avatar
- [[papers/zielonka-2022-mica]] — MICA provides the identity prior; same authors
- [[papers/giebenhain-2023-nphm]] — NPHM is the implicit SDF alternative for topology flexibility
- [[papers/qian-2024-gaussian-avatars]] — GaussianAvatars achieves similar goals with 3DGS (faster rendering)
- [[papers/li-2017-flame]] — FLAME is the structural backbone
- [[authors/bolkart-timo]]
