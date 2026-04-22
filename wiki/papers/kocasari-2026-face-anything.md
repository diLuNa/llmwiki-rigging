---
title: "Face Anything: 4D Face Reconstruction from Any Image Sequence"
authors: [Kocasarı, Umut; Giebenhain, Simon; Shaw, Richard; Nießner, Matthias]
venue: arXiv 2604.19702
year: 2026
tags: [neural, digital-human, facial-capture, 4d-reconstruction, depth-estimation, canonical-maps]
source: raw/papers/2604.19702v1.pdf
---

## Summary
Face Anything presents a unified feed-forward method for high-fidelity 4D facial reconstruction and dense tracking from image sequences. Instead of predicting frame-to-frame motion, the model predicts **canonical maps** — per-pixel assignments to a normalized FLAME coordinate space — enabling temporally consistent reconstruction and correspondence estimation in a single forward pass.

## Problem
Existing 4D face methods either decouple reconstruction from correspondence (losing temporal consistency) or rely on motion-field formulations that require multiple forward passes and are unstable over long sequences. Parametric models (P3DMM, V-DPM) constrain geometry and are slow.

## Method
**Architecture.** A 1.2B-parameter transformer pretrained on DAViD (monocular facial priors), then finetuned on a custom NeRSemble-derived dataset (414 subjects, ~320k images, 16 cameras). The network jointly predicts:
- $D_i \in \mathbb{R}^{H \times W}$ — depth maps
- $R_i \in \mathbb{R}^{H \times W \times 3}$ — ray maps
- $C_i \in \mathbb{R}^{H \times W \times 3}$ — canonical maps (FLAME coordinate per pixel)

Architecture uses a Dual-DPT head (for depth, based on DA3) plus a DPT head for canonical prediction. Multi-image input is sampled as (1) multi-view from a single timestamp and (2) single-camera across multiple timestamps.

**Canonical Map Prediction.** Each pixel is assigned a 3D coordinate in a shared normalized FLAME space. Correspondences between frames are found via nearest-neighbor search (KD-Tree) in canonical space:

$$\mathbf{q} = \arg\min_{\mathbf{q}' \in \Omega_j} \|C_i(\mathbf{p}) - C_j(\mathbf{q}')\|_2$$

**Loss.** Regression $\mathcal{L}^X_\text{reg}$, confidence-weighted regression $\mathcal{L}^X_\text{conf}$, and gradient losses $\mathcal{L}^X_\text{grad}$ on $X \in \{D, R, C\}$; canonical loss weight $\lambda_C = 5$.

**Dataset.** COLMAP multi-view reconstruction + FLAME tracking used to generate canonical supervision. NeRSemble subsets (414 subjects, diverse expression/pose coverage via farthest-point sampling of blendshape/pose parameters).

## Key Results
- SotA depth accuracy on NeRSemble and Ava-256 (0.040/0.038 AbsRel vs 0.048/0.048 for best prior Sapiens-2B)
- ~3× lower correspondence error than P3DMM/V-DPM on NeRSemble
- 16% better depth accuracy vs V-DPM
- Runtime: 5s vs 40s (V-DPM) for 40 images; fits 470 vs 40 images/GPU (80GB)
- FLAME tracking accuracy (CD-L1): 0.195 vs 0.238 (P3DMM-constrained)

## Limitations
- Face-specialized — does not generalize to non-face regions; nearby accessories (microphones, hands) not reliably canonicalized
- Degrades under strong occlusion, extreme viewpoints, or limited facial visibility
- Canonical map prediction limited to face region; extending to hair/ears is future work

## Connections
- [[papers/li-2017-flame]] — FLAME model used as canonical coordinate space
- [[papers/giebenhain-2023-nphm]] — earlier Nießner/Giebenhain work on neural parametric head models
- [[papers/giebenhain-2024-npga]] — Gaussian avatar work by same group
- [[papers/feng-2021-deca]] — DECA, related monocular 3D face reconstruction
- [[papers/qian-2024-gaussian-avatars]] — Nießner group, Gaussian avatar rendering

## Implementation Notes
- Correspondence search via KD-Tree: <0.2s per image pair on CPU; fully parallelizable
- Resolution: 504×504 base for training; bfloat16 precision; gradient checkpointing
- FLAME tracking used as supervision signal — small parametric misalignments tolerated; network learns to compensate
- For downstream animation: canonical maps directly yield dense temporal correspondences usable for blendshape or avatar animation without re-optimization
