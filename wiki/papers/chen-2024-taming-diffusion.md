---
title: "Taming Diffusion Probabilistic Models for Character Control"
authors: [Chen, Rui; Shi, Mingyi; Huang, Shaoli; Tan, Ping; Komura, Taku; Chen, Xuelin]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [neural, diffusion, character-animation, motion-synthesis, real-time-control]
source: arXiv:TBA
doi: 10.1145/3641519.3657440
---

## Summary
Character control framework utilizing motion diffusion models for real-time, diverse animation generation. Transformer-based Conditional Autoregressive Motion Diffusion Model (CAMDM) generates future motions conditioned on historical movement and high-level user controls. Addresses motion diffusion challenges through classifier-free guidance and heuristic trajectory extension.

## Problem
Motion diffusion models generate high-quality, diverse animations but are challenging to control in real-time for character animation. Balancing diversity, quality, and responsiveness to dynamic user inputs requires novel algorithmic designs.

## Method
- **CAMDM architecture**: Transformer-based conditional autoregressive diffusion
- **Separate condition tokenization**: Independent encoding of past motion, trajectory, and control
- **Classifier-free guidance**: Adaptive weight balancing between conditioned and unconditioned generation
- **Trajectory heuristics**: Future motion extension enabling flexible trajectory specification

## Key Results
- Real-time character control from diverse input signals (keyboard, gamepad, sketch)
- High-quality, natural motion generation compared to baseline methods
- Effective handling of rapid control changes and transitions
- Supports complex interaction scenarios

## Limitations
- Diversity-quality tradeoff with classifier-free guidance strength
- Computational cost remains challenging for very long sequences
- Generalization to unseen motion types limited by training data
- Trajectory heuristics may produce artifacts at boundaries

## Connections
- [[papers/gat-2025-anytop]] — topology-agnostic motion synthesis
- [[concepts/motion-synthesis]] — neural motion generation fundamentals
- [[concepts/secondary-motion]] — enriching primary skeletal motion
- [[papers/holden-2015-inverse-rig]] — character control and IK
- [[techniques/ml-deformer]] — learned deformation

## Implementation Notes
- Separate condition encoding critical for stable training
- Classifier-free guidance requires careful hyperparameter tuning
- Compatible with real-time animation engines (Unity, Unreal)
- Works with arbitrary skeleton topologies via standardized representations

## External References
- GitHub: [github.com/AIGAnimation/CAMDM](https://github.com/AIGAnimation/CAMDM)
- Project page: [aiganimation.github.io/CAMDM](https://aiganimation.github.io/CAMDM/)
- ACM DL: [doi.org/10.1145/3641519.3657440](https://doi.org/10.1145/3641519.3657440)
