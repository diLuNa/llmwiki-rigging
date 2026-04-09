---
title: "FaceFormer: Speech-Driven 3D Facial Animation with Transformers"
authors: [Fan, Yingruo; Lin, Zhaojiang; Saito, Jun; Wang, Wenping; Komura, Taku]
venue: CVPR 2022
year: 2022
tags: [speech-driven-animation, neural, blendshapes, digital-human]
source: raw/papers/2112.05329.pdf
---

## Summary
FaceFormer is an end-to-end Transformer that encodes long-term raw audio context using pre-trained self-supervised speech representations (wav2vec 2.0) and autoregressively predicts sequences of 3D face mesh vertex displacements. Novel biased cross-modal attention and biased causal self-attention with periodic positional encoding align audio to facial motion over long sequences. FaceFormer is the canonical baseline for 3D mesh-output speech animation — every subsequent paper (CodeTalker, EmoTalk, DiffPoseTalk) benchmarks against it.

## Problem
Existing speech-driven 3D facial animation methods process short audio windows, missing long-range phonetic context. Autoregressive generation accumulates error without proper temporal attention. A Transformer architecture that encodes long-term audio while generating temporally coherent 3D face vertex sequences is missing.

## Method
**Audio encoder:** wav2vec 2.0 pre-trained speech model encodes raw waveform into rich feature representations with phonetic and prosodic content.

**Biased cross-modal attention:** When attending audio features, attention is biased toward the audio window temporally aligned to the current output frame — preventing the model from attending to future audio.

**Biased causal self-attention:** Attention over the autoregressive output sequence is biased toward recent frames, encouraging smooth motion continuity.

**Periodic positional encoding:** Captures the cyclical nature of phoneme production (jaw open-close cycles).

**Output:** Per-frame 3D vertex displacement sequence on a fixed mesh topology (VOCASET mesh, 5023 vertices). Trained on the VOCASET corpus (12 subjects, 40 sentences each).

## Key Results
- State-of-the-art on VOCASET lip vertex error.
- Better temporal coherence than single-frame regression baselines.
- Canonical baseline for all subsequent 3D speech animation methods.
- CVPR 2022.

## Limitations
- Fixed mesh topology (VOCASET) — not directly applicable to arbitrary character meshes without retargeting.
- Trained on English speech with limited speaker diversity.
- No emotion control — generates neutral facial motion regardless of speech affect.
- Output is vertex displacements, not FACS weights — requires retargeting for production blendshape rigs.

## Connections
- [[concepts/speech-driven-animation]] — foundational Transformer baseline for 3D mesh speech animation
- [[concepts/blendshapes]] — output vertex displacements can be retargeted to blendshape rigs
- [[papers/xing-2023-codetalker]] — CodeTalker extends FaceFormer with discrete motion codebook
- [[papers/peng-2023-emotalk]] — EmoTalk adds emotion disentanglement
- [[papers/sun-2024-diffposetalk]] — DiffPoseTalk adds diffusion-based style control and head pose
- [[papers/taylor-2017-speech-animation]] — prior deep learning baseline (LSTM-based, no long-term context)
- [[authors/saito-jun]]
