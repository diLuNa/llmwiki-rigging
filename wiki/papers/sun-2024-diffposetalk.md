---
title: "DiffPoseTalk: Speech-Driven Stylistic 3D Facial Animation and Head Pose Generation via Diffusion Models"
authors: [Sun, Zhiyao; Lv, Tian; Ye, Sheng; Lin, Matthieu; Sheng, Jenny; Wen, Yu-Hui; Yu, Minjing; Liu, Yong-Jin]
venue: ACM SIGGRAPH 2024 (Journal Track)
year: 2024
tags: [speech-driven-animation, neural, blendshapes, digital-human, simulation]
source: raw/papers/2310.00434.pdf
---

## Summary
DiffPoseTalk uses a diffusion model conditioned on speech and a style encoder (fed a short reference video) to jointly generate diverse, stylistic 3D facial expression sequences and head pose, directly on 3DMM parameters. Classifier-free guidance enables control over style strength. By training on 3DMM parameters reconstructed from an audio-visual dataset, it bypasses 3D scan data scarcity. The first diffusion-based method to jointly model facial motion style *and* head pose from speech — published in ACM TOG SIGGRAPH 2024.

## Problem
FaceFormer and CodeTalker produce deterministic, style-agnostic output — the same speech produces the same animation regardless of the speaker's idiosyncratic style (head nod frequency, expressiveness level, jaw amplitude). Head pose is rarely modeled jointly. Diffusion models naturally handle the one-to-many speech-to-motion mapping but haven't been applied to stylistic 3D facial animation.

## Method
**Diffusion backbone:** A DDPM over 3DMM parameter sequences (expression coefficients $\psi^t$ + head pose $\theta_\text{head}^t$ per frame). The denoising network is a Transformer conditioned on:
- Speech features (wav2vec 2.0).
- Style embedding from a reference video clip (a few seconds of the target speaking style).

**Classifier-free guidance:** Style conditioning uses CFG — dropping style during training with probability $p$, enabling inference with arbitrary style strength $\gamma$.

**Training data:** 3DMM parameters reconstructed from a large audio-visual dataset (no 3D scan required). Expression and pose sequences serve as training targets.

**Joint expression + pose:** Head pose is modeled alongside facial expression in the same diffusion process — capturing the coupled dynamics of speaking style (nodders vs. still speakers).

## Key Results
- Diverse, stylistic outputs from a single speech input (diffusion stochasticity + style control).
- Better lip-sync and style similarity vs FaceFormer, CodeTalker, EmoTalk.
- First joint speech animation + head pose generation via diffusion.
- ACM SIGGRAPH 2024.

## Limitations
- Diffusion inference requires multiple denoising steps — not real-time.
- 3DMM parameter output — same retargeting limitation to arbitrary meshes.
- Style encoder requires a reference video clip; zero-shot style generalization is limited.

## Connections
- [[concepts/speech-driven-animation]] — diffusion-based stylistic 3D speech animation; current SIGGRAPH SOTA
- [[papers/fan-2022-faceformer]] — primary baseline
- [[papers/xing-2023-codetalker]] — discrete motion prior baseline
- [[papers/peng-2023-emotalk]] — EmoTalk handles emotion (not style); complementary
- [[papers/zou-2024-4d-expression-diffusion]] — concurrent: diffusion for 4D expression sequences (not speech-driven)
