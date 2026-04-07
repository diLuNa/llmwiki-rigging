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

## Key Papers
- [[papers/medina-2022-tongue-animation]] — speech-driven tongue, jaw, and lip animation (CVPR 2022, Epic Games)

## Connections
- [[concepts/blendshapes]] — viseme and jaw blendshapes driven by audio features
- [[concepts/digital-human-appearance]] — appearance of inner-mouth (tongue texture, teeth)
- [[papers/choi-2022-animatomy]] — facial rig system that inner-mouth systems animate into

## Notes
Inner-mouth animation (tongue) remains a frontier. The tongue is nearly impossible to capture optically during speech, requiring electromagnetic articulography or ultrasound. Neural models trained on such data can generalize to audio-only inference. The output is typically 3D landmarks or phoneme-correlated blend weights, which then drive a production rig's tongue blendshape set.
