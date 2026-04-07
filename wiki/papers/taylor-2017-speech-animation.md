---
title: "A Deep Learning Approach for Generalized Speech Animation"
authors: [Taylor, Sarah; Kim, Taehwan; Yue, Yisong; Mahler, Moshe; Krahe, Jimmy; Rodriguez, Anastasio Garcia; Hodgins, Jessica; Matthews, Iain]
venue: ACM SIGGRAPH 2017
year: 2017
tags: [speech-driven-animation, neural, blendshapes, digital-human]
source: ~no local PDF~
---

## Summary
An LSTM-based deep learning system that maps audio features directly to facial blendshape weights for real-time lip sync animation, without phoneme transcription. Trained on synchronized audio + blendshape capture data; generalizes across speakers and languages. Influential early example of end-to-end neural speech-to-animation.

## Problem
Traditional lip sync relies on explicit phoneme alignment, which is slow and language-specific. Speaker-specific training restricts generalization. A single neural model that maps audio → blendshape weights across speakers and without transcription would be a production breakthrough.

## Method
**Input:** Raw audio waveform → mel-frequency cepstral coefficients (MFCCs) or similar audio features over a sliding window.

**Network:** Bidirectional LSTM encoder mapping audio features to a sequence of blendshape weight vectors. Trained with L2 loss against captured ground truth blendshape weights.

**Output:** Per-frame blendshape weights for a standardized facial blendshape set (lip corner, jaw open, lip pucker, etc.). Drives a production facial rig.

**Training data:** Paired audio + facial performance capture from multiple speakers. Blendshape weights extracted via performance capture pipeline.

**Generalization:** Network architecture and training strategy allow cross-speaker inference without fine-tuning.

## Key Results
- Convincing real-time lip sync from audio alone, without phoneme transcription.
- Generalizes to unseen speakers.
- Reduces lip sync authoring time significantly.
- Demonstrated on Disney character rigs.

## Limitations
- Blendshape output quality bounded by the blendshape rig's expressiveness.
- Audio-only input: cannot handle text/intent-driven emphasis or emotion.
- MFCC features less robust than modern self-supervised encoders (wav2vec, HuBERT).
- Does not model tongue or inner-mouth motion (cf. Medina 2022).

## Connections
- [[papers/medina-2022-tongue-animation]] — extends to inner-mouth (tongue) animation
- [[concepts/speech-driven-animation]] — parent concept
- [[concepts/blendshapes]] — the rig interface this system drives

