---
title: "CodeTalker: Speech-Driven 3D Facial Animation with Discrete Motion Prior"
authors: [Xing, Jinbo; Xia, Menghan; Zhang, Yuechen; Cun, Xiaodong; Wang, Jue; Wong, Tien-Tsin]
venue: CVPR 2023
year: 2023
tags: [speech-driven-animation, neural, blendshapes, digital-human]
source: raw/papers/2301.02379.pdf
---

## Summary
CodeTalker reframes speech-driven 3D facial animation as a discrete code-book query problem rather than direct regression. A VQ-VAE learns a finite codebook of realistic facial motion tokens from real face sequences via self-reconstruction; a temporal autoregressive model then predicts codebook indices from speech, generating coherent sequences without the regression-to-mean collapse that plagues deterministic baselines. Outperforms FaceFormer on lip-sync metrics; operates directly on 3D mesh vertex sequences.

## Problem
FaceFormer and other regression-based methods produce over-smoothed, averaged facial motion — the many-to-one mapping from audio to motion collapses to the mean. A discrete motion prior that constrains generation to the manifold of real facial motion would eliminate this regression blur.

## Method
**Stage 1 — Motion codebook (VQ-VAE):**
Temporal encoder compresses 3D face vertex sequences into a sequence of discrete codes $z_q$ from a learned codebook $C = \{c_k\}_{k=1}^K$. Decoder reconstructs vertex sequences from codes. Training: self-reconstruction + commitment loss (standard VQ-VAE).

**Stage 2 — Speech-to-code autoregressive model:**
A Transformer predicts codebook indices autoregressively given speech features. At each step: speech embedding → cross-attention → predict next code index from $C$.

**Inference:** Speech → code index sequence → VQ-VAE decoder → vertex displacement sequence.

The codebook ensures all generated motions lie on the real motion manifold — no averaging of incompatible motion modes.

## Key Results
- Outperforms FaceFormer on lip vertex error (LVE) and max-LVE.
- Better perceptual quality in user studies — more natural, less rubber-faced.
- CVPR 2023.

## Limitations
- Fixed mesh topology (VOCASET); same retargeting limitation as FaceFormer.
- Codebook size limits motion diversity — rare expressions may not be in the codebook.
- Two-stage training; more complex pipeline than end-to-end regression.

## Connections
- [[concepts/speech-driven-animation]] — discrete motion prior for 3D speech animation
- [[papers/fan-2022-faceformer]] — FaceFormer is the primary baseline
- [[papers/peng-2023-emotalk]] — EmoTalk adds emotion control (concurrent)
- [[papers/sun-2024-diffposetalk]] — DiffPoseTalk replaces codebook with diffusion for style control
