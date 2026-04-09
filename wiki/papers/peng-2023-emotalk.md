---
title: "EmoTalk: Speech-Driven Emotional Disentanglement for 3D Face Animation"
authors: [Peng, Ziqiao; Wu, Haoyu; Song, Zhenbo; Xu, Hao; Zhu, Xiangyu; He, Jun; Liu, Hongyan; Fan, Zhaoxin]
venue: ICCV 2023
year: 2023
tags: [speech-driven-animation, neural, blendshapes, digital-human]
source: raw/papers/2303.11089.pdf
---

## Summary
EmoTalk introduces emotion disentanglement into 3D speech-driven facial animation: an emotion disentangling encoder separates emotional content from semantic (phonetic) content in speech via cross-reconstruction, then drives a 3D talking face with disentangled identity, emotion, and content embeddings. The method contributes 3D-ETF — a large-scale 3D emotional talking face dataset — and outperforms FaceFormer and VOCA on both lip vertex error and emotional vertex error metrics.

## Problem
FaceFormer and CodeTalker generate neutral facial motion regardless of speech emotional content — joy sounds the same as sadness in the output animation. Disentangling emotion from phoneme content in speech, and driving distinct emotional expression on a 3D face, is unaddressed.

## Method
**Emotion disentangling encoder:**
Given speech input, two encoders are trained contrastively:
- *Emotion encoder* $E_\text{emo}$: extracts emotional embedding; cross-reconstruction ensures it ignores semantic content.
- *Content encoder* $E_\text{cnt}$: extracts phonetic embedding; cross-reconstruction ensures it ignores emotion.

**3D face decoder:**
Conditioned on $(E_\text{emo}, E_\text{cnt}, \text{identity})$ → vertex displacement sequence. The identity embedding prevents identity entanglement with emotion.

**3D-ETF dataset:** Collected large-scale 3D facial scan sequences with emotion labels (angry, happy, sad, surprise, fear, disgust, neutral). 3D face meshes reconstructed via blendshape supervision from 2D emotional video.

**Training:** Self-supervised on 3D mesh sequences from 3D-ETF + standard talking face datasets.

## Key Results
- Outperforms FaceFormer and VOCA on both lip-sync (LVE) and emotion expressiveness metrics.
- First 3D speech animation method with explicit emotion disentanglement.
- ICCV 2023.

## Limitations
- 3D-ETF dataset is reconstructed from 2D video via blendshapes — not scan-captured ground truth.
- Fixed mesh topology (VOCASET-compatible); same retargeting limitation as FaceFormer.
- Emotion control requires an emotion label or reference audio clip — not inferred from neutral speech alone.

## Connections
- [[concepts/speech-driven-animation]] — first emotion-disentangled 3D speech animation system
- [[concepts/blendshapes]] — blendshape supervision used for 3D-ETF dataset construction
- [[papers/fan-2022-faceformer]] — primary baseline
- [[papers/xing-2023-codetalker]] — concurrent: discrete motion prior (no emotion)
- [[papers/sun-2024-diffposetalk]] — DiffPoseTalk adds style control via diffusion
