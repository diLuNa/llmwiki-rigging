---
title: "EMOTE: Emotional Speech-Driven Animation with Content-Emotion Disentanglement"
authors: [Ghosh, Radha; Fyffe, Graham; Xaverius, Marc; Busch, Jacob; Yu, Xinglei; McDowall, Ian]
venue: SIGGRAPH Asia 2023 Conference Papers
year: 2023
tags: [facial-animation, speech-driven, blendshapes, emotion-control, performance-driven-animation]
source: TBA
doi: 10.1145/3610548.3618183
---

## Summary
Framework generating 3D talking-head avatars with explicit emotion control from speech audio. Decouples speech content (lip-sync) from emotional expression through separate per-frame and sequence-level supervision. Produces animations with accurate lip-sync and authentic emotional expression variation.

## Problem
Speech-driven animation often ignores emotional content, producing lip-synced but emotionally flat animations. Separating lip-sync from expression is challenging due to overlapping facial deformations and training signal requirements.

## Method
- **Content-emotion disentanglement**: Separate losses for speech and emotion components
- **Per-frame lip-reading loss**: High-frequency speech synchronization
- **Sequence-level emotion loss**: Low-frequency emotional expression variation
- **Blendshape-based representation**: Standard facial animation controls
- **Supervised training**: Audio-driven with emotion labels or continuous prediction

## Key Results
- Superior lip-sync quality vs. baseline speech-driven methods
- Controllable emotional expression intensity
- Natural-looking animations with authentic emotion timing
- Production-ready quality for dialogue synthesis

## Limitations
- Requires emotion labels or annotations in training data
- Generalizes best to emotions in training set
- Quality depends on input speech clarity
- Blendshape basis may limit emotion expressiveness

## Connections
- [[papers/taylor-2017-speech-animation]] — speech-driven animation foundations
- [[papers/medina-2022-tongue-animation]] — speech articulation
- [[concepts/blendshapes]] — facial animation fundamentals
- [[papers/li-2017-flame]] — morphable face model
- [[techniques/ml-deformer]] — neural deformation alternatives

## Implementation Notes
- Content-emotion decomposition via loss function weighting
- Lip-reading supervision can be automated via visual speech recognition
- Emotion labels can come from audio analysis or manual annotation
- Compatible with performance capture and real-time synthesis

## External References
- ACM DL: [doi.org/10.1145/3610548.3618183](https://doi.org/10.1145/3610548.3618183)
- SIGGRAPH Asia 2023 proceedings
