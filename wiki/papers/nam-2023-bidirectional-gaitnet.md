---
title: "Bidirectional GaitNet: A Bidirectional Prediction Model of Human Gait and Anatomical Conditions"
authors: [Nam, Hyunwoo; Lee, Seyoung; Lee, Jungnam]
venue: ACM SIGGRAPH 2023 Conference Proceedings
year: 2023
tags: [gait-animation, musculoskeletal-models, variational-autoencoder, biomechanics, synthesis]
source: TBA
doi: 10.1145/3588432.3591492
---

## Summary
Generative model learning bidirectional relationship between human anatomy and gait patterns. Forward model predicts gait given anatomical conditions; backward model estimates anatomy from observed gait. Built on comprehensive 304-unit musculoskeletal model with distilled simulation data and VAE architecture.

## Problem
Human gait is highly individualized, varying with body morphology, muscle physiology, and neuromuscular control. Understanding and predicting gait from anatomy (or vice versa) enables personalized animation and gait analysis applications. Requires integration of biomechanical simulation with generative modeling.

## Method
- **Musculoskeletal model**: 304 Hill-type musculotendon units for realistic muscle dynamics
- **Simulation-based training**: Distill data from state-of-the-art predictive gait simulator
- **Forward model**: Maps anatomical parameters to gait cycles
- **VAE architecture**: Bidirectional inference via encoder-decoder with latent space
- **Backward model**: Inverse mapping from observed gaits to anatomy parameters

## Key Results
- Accurate gait prediction from anatomical parameters
- Successful anatomy inference from gait observations
- Enables personalization and gait analysis applications
- Demonstrates biomechanical validity of learned models

## Limitations
- Training data generation expensive (simulation-based)
- Limited to healthy adult gait patterns
- Anatomical parameters must fit musculoskeletal model
- Generalization to pathological gaits limited

## Connections
- [[papers/loper-2015-smpl]] — parametric human body model
- [[papers/choi-2022-animatomy]] — anatomy-aware deformation
- [[concepts/muscles]] — musculoskeletal modeling for animation
- [[papers/cao-2024-multimodal-grasp]] — grasp synthesis from anatomy
- [[concepts/simulation]] — physics-based character animation

## Implementation Notes
- Distillation from simulation reduces training data cost
- Latent space regularization critical for smooth interpolation
- Compatible with SMPL and similar body models for appearance
- Useful for motion retargeting and personalized animation

## External References
- GitHub: [github.com/namjohn10/BidirectionalGaitNet](https://github.com/namjohn10/BidirectionalGaitNet)
- ACM DL: [doi.org/10.1145/3588432.3591492](https://doi.org/10.1145/3588432.3591492)
