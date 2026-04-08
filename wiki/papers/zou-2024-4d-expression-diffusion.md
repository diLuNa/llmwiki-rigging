---
title: "4D Facial Expression Diffusion Model"
authors: [Zou, Kaifeng; Faisan, Sylvain; Yu, Boyang; Valette, Sébastien; Seo, Hyewon]
venue: ACM Transactions on Multimedia Computing, Communications, and Applications 2024
year: 2024
tags: [neural, digital-human, blendshapes, simulation, speech-driven-animation]
source: raw/papers/2303.16611.pdf
---

## Summary
The first diffusion model for 4D (3D + time) facial expression sequences. A DDPM generates 3D landmark trajectories from conditioning signals (expression labels, text, partial sequences, or geometry alone); a landmark-guided encoder-decoder then maps those trajectories to mesh vertex deformations on an input face mesh. The system learns from a relatively small dataset and produces realistic expression dynamics without a rig or blendshape basis.

## Problem
3D facial expression sequence generation requires both plausible shape (geometry at each frame) and plausible motion (temporal dynamics — onset, apex, offset timing). Prior generative methods either operate on 2D landmarks (losing depth) or require per-frame 3D supervision. A geometry-first generative approach that produces 3D mesh sequences with realistic timing from flexible conditioning signals is missing.

## Method
**Stage 1 — 3D landmark diffusion:**
A DDPM over 3D landmark trajectories $\{L_t\}_{t=1}^T$ where $L_t \in \mathbb{R}^{K \times 3}$ is the landmark configuration at frame $t$. The diffusion model learns the distribution of expression dynamics as a sequence.

Conditioning modes:
- Expression label (discrete class) → class-conditional generation
- Text description → text-conditional generation (via text encoder)
- Partial sequence → sequence completion
- Unconditioned → free generation

**Stage 2 — Landmark-guided mesh deformation:**
An encoder-decoder maps landmark trajectories to dense vertex displacement sequences for the input face mesh. The decoder applies deformations without requiring a rig structure — geometry-driven, not rig-driven.

## Key Results
- Generates realistic, temporally coherent 4D expression sequences.
- Supports multiple conditioning modes (label, text, partial, free).
- Trained on a relatively small 4D scan dataset — data-efficient.
- First DDPM for 4D facial expression sequences.

## Limitations
- Mesh deformation quality bounded by training scan dataset diversity.
- Not real-time; DDPM inference requires multiple denoising steps.
- Expressions generated are not directly addressable by FACS AU controls — not a rig-based system.
- Text conditioning requires a pre-trained text encoder; expression vocabulary in text space is limited.

## Connections
- [[concepts/nonlinear-face-models]] — diffusion-based generative 4D face model
- [[concepts/facial-blendshape-rigs]] — landmark trajectory provides an alternative to blendshape weight sequences
- [[concepts/speech-driven-animation]] — the temporal expression model is applicable to speech-driven facial animation
- [[papers/potamias-2024-shapefusion]] — concurrent: diffusion for static 3D shape editing (no temporal component)
- [[papers/taylor-2017-speech-animation]] — prior deep learning approach to expression sequence generation from audio
