---
title: "Speech-Driven Animation"
tags: [speech-driven-animation, neural, digital-human, facial-capture]
---

## Definition
Techniques that generate facial and inner-mouth animation (lip sync, jaw, tongue) automatically from audio or text input. Ranges from signal-processing-based phoneme-to-viseme mapping to deep learning encoder-decoder models that predict continuous 3D landmark trajectories or blendshape weights.

## Variants / Taxonomy

### Phoneme / Viseme Mapping
Rule-based: parse phonemes from audio/text; map to pre-authored viseme blendshapes. Fast and robust but lacks coarticulation realism.

### Audio-Driven Neural Models
Encoder-decoder networks mapping waveform / feature frames → landmark trajectories or rig parameters. Self-supervised audio encoders (wav2vec, HuBERT) are now standard feature extractors.
- Key paper: [[papers/medina-2022-tongue-animation]] — speech → tongue + jaw + lip animation

### Text-Driven (TTS + Animation)
Text → TTS audio → animation pipeline, or direct text-to-animation with attention alignment.

### Tongue and Inner-Mouth Animation
Specifically targets non-lip articulators. Requires specialized mocap hardware (electromagnetic sensors, ultrasound). Historically underserved in production pipelines.
- Key paper: [[papers/medina-2022-tongue-animation]] — large-scale dataset + deep learning for tongue animation

### 3D Mesh-Based Speech Animation (Neural)

Encode raw audio with a pre-trained speech model; autoregressively decode 3D face vertex displacements or 3DMM parameters. Forms a clear lineage: FaceFormer → CodeTalker → EmoTalk → DiffPoseTalk.

- [[papers/fan-2022-faceformer]] **(FaceFormer, CVPR 2022)** — Transformer + wav2vec 2.0; biased cross-modal attention + periodic positional encoding; canonical VOCASET baseline; every subsequent paper benchmarks against it
- [[papers/xing-2023-codetalker]] **(CodeTalker, CVPR 2023)** — VQ-VAE codebook of real facial motion tokens; speech predicts codebook indices autoregressively; eliminates regression-to-mean collapse
- [[papers/peng-2023-emotalk]] **(EmoTalk, ICCV 2023)** — emotion disentanglement via contrastive cross-reconstruction; separate emotion + phoneme encoders; drives animation with distinct emotional content; 3D-ETF dataset
- [[papers/sun-2024-diffposetalk]] **(DiffPoseTalk, SIGGRAPH 2024)** — DDPM over 3DMM expression + head pose jointly; style encoder from reference video; classifier-free guidance for style strength control; first joint pose+expression diffusion

## Key Papers
- [[papers/fan-2022-faceformer]] — Transformer speech-driven 3D mesh animation; wav2vec 2.0 + biased attention; canonical baseline (CVPR 2022)
- [[papers/xing-2023-codetalker]] — discrete VQ-VAE motion codebook; avoids regression blur (CVPR 2023)
- [[papers/peng-2023-emotalk]] — emotion disentanglement for 3D speech animation; 3D-ETF dataset (ICCV 2023)
- [[papers/sun-2024-diffposetalk]] — diffusion-based stylistic facial animation + head pose (SIGGRAPH 2024)
- [[papers/medina-2022-tongue-animation]] — speech-driven tongue, jaw, and lip animation (CVPR 2022, Epic Games)
- [[papers/taylor-2017-speech-animation]] — LSTM deep learning baseline preceding Transformer era (SIGGRAPH 2017)
- [[papers/zou-2024-4d-expression-diffusion]] — diffusion over 4D expression sequences; multi-modal conditioning (ACM TOMM 2024)

## Connections
- [[concepts/blendshapes]] — viseme, jaw, and FACS blendshapes driven by audio features
- [[concepts/nonlinear-face-models]] — 3DMM parameter output (FaceFormer-era) feeds nonlinear face models for rendering
- [[concepts/digital-human-appearance]] — appearance of inner-mouth (tongue texture, teeth)
- [[papers/choi-2022-animatomy]] — facial rig system that inner-mouth systems animate into

## Notes
**Topology lock-in:** All major 3D speech animation models (FaceFormer, CodeTalker, EmoTalk) output vertex displacements on a fixed VOCASET mesh topology. To use these in production, output must be retargeted to the character's rig — see [[concepts/auto-rigging]] and [[papers/cha-2025-neural-face-skinning]].

**Regression-to-mean:** Deterministic regression (FaceFormer) averages over the many valid animations for a given audio input. CodeTalker addresses this with a discrete codebook; DiffPoseTalk addresses it with diffusion stochasticity.

**Inner-mouth animation (tongue):** Remains a frontier. The tongue is nearly impossible to capture optically during speech, requiring electromagnetic articulography or ultrasound. Neural models trained on such data can generalize to audio-only inference. The output is typically 3D landmarks or phoneme-correlated blend weights, which then drive a production rig's tongue blendshape set.
