---
title: "AnimPortrait3D: Text-based Animatable 3D Avatars with Morphable Model Alignment"
authors: [Wu, Yue; Li, Junxuan; Kirschstein, Tobias; Sevastopolskiy, Artem; Saito, Shunsuke; Tan, Qingyang; Romero, Javier; Cao, Chen; Rushmeier, Holly; Nam, Giljoo]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [neural, text-to-3d, avatar-generation, facial-rigging, morphable-models]
source: GitHub
doi: 10.1145/3721238.3730827
---

## Summary
Text-based framework for generating animatable 3D portrait avatars with accurate morphable model alignment. Addresses appearance-geometry ambiguity and rigging misalignment by leveraging pre-trained text-to-3D priors and ControlNet-based refinement. Produces high-fidelity, rigged avatars suitable for facial animation from text descriptions.

## Problem
Text-to-3D generation with parametric face models (FLAME) often suffers from misalignment between generated appearance and rigging, poor geometry reconstruction, and limited facial expression capability. Score distillation sampling approaches struggle with detail synthesis while maintaining model coherence.

## Method
- **Prior-guided initialization**: Use pretrained text-to-3D models to initialize 3D geometry and appearance with robust rigging relationships
- **ControlNet refinement**: Condition generation on semantic and normal maps from morphable model to ensure alignment
- **Morphable model supervision**: Optimize for consistency with FLAME parameters and blendshape controls
- **Expression synthesis**: Enable dynamic facial expressions through learned deformation offsets

## Key Results
- Generates high-quality 3D head avatars from text descriptions
- Maintains accurate alignment between appearance and FLAME rigging
- Supports diverse facial expressions and animations
- Outperforms baseline text-to-3D approaches in synthesis quality and animation fidelity

## Limitations
- Text description quality directly affects output fidelity
- Limited to head region (not full-body characters)
- Morphable model constraint may limit extreme morphologies
- Requires careful ControlNet conditioning for best results

## Connections
- [[papers/li-2017-flame]] — morphable face model foundation
- [[papers/feng-2021-deca]] — face reconstruction and animation
- [[papers/he-2025-lam]] — related neural avatar generation
- [[concepts/blendshapes]] — facial animation controls
- [[concepts/nonlinear-face-models]] — morphable model extensions

## Implementation Notes
- Prior-guided initialization critical for avoiding geometry-appearance misalignment
- Dual-path optimization balancing appearance synthesis and rigging accuracy
- Compatible with standard facial animation pipelines via FLAME export
- Text prompts should include style, appearance, and expression details

## External References
- GitHub: [github.com/oneThousand1000/AnimPortrait3D](https://github.com/oneThousand1000/AnimPortrait3D)
- ACM DL: [doi.org/10.1145/3721238.3730827](https://doi.org/10.1145/3721238.3730827)
