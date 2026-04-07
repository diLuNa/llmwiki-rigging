---
title: "Speech Driven Tongue Animation"
authors: [Medina, Salvador; Tome, Denis; Stoll, Carsten; Tiede, Mark; Munhall, Kevin; Hauptmann, Alex; Matthews, Iain]
venue: CVPR 2022
year: 2022
tags: [speech-driven-animation, neural, facial-capture, digital-human]
source: raw/papers/Medina_Speech_Driven_Tongue_Animation_CVPR_2022_paper.pdf
---

## Summary
A deep-learning system that generates realistic tongue, jaw, and lip animation for virtual characters directly from audio input. Introduces a large-scale speech + mocap dataset capturing inner-mouth articulators, and evaluates encoder-decoder architectures with self-supervised audio features (wav2vec-style) for speech-to-animation mapping.

## Problem
Optical performance capture of the tongue is infeasible — the inner mouth is only partially observable. Existing speech-driven animation focuses on lips/face, leaving tongue animation unrealistic ("uncanny valley" for close-up face shots). No large-scale dataset of speech-synchronized tongue motion existed.

## Method
**Dataset:** Large-scale mocap dataset capturing tongue, jaw, and lip landmark trajectories synchronized with audio. Subjects speak varied content; captures include inner-mouth markers.

**Architecture:** Encoder-decoder networks mapping audio features → landmark trajectories. Multiple architectures evaluated (RNN, Transformer variants).

**Audio features:** Self-supervised deep audio encoders (wav2vec-style) found most robust — generalize to unseen speakers and content without speaker-specific fine-tuning.

**Output:** 3D landmarks driving a high-quality parametric 3D face model (likely FLAME or similar). Tongue mesh deforms via landmark-driven blend/rig system.

## Key Results
- Self-supervised audio encoders outperform mel-spectrogram baselines.
- Generalizes to unseen speakers without retraining.
- Convincing tongue + jaw animation on parametric face models from audio alone.

## Limitations
- Landmark-based — depends on downstream rig/blend system for final deformation quality.
- Does not model tongue-teeth or tongue-palate contact dynamics.
- Trained on limited capture hardware; generalization to diverse accents/languages untested.

## Connections
- [[concepts/speech-driven-animation]] — parent concept
- [[concepts/blendshapes]] — parametric face model driven by landmarks
- [[papers/gruber-2024-gantlitz]] — complementary face appearance; this paper drives geometry

