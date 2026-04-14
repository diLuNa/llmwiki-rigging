---
title: "AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control"
authors: [Peng, Xue B.; Coumans, Erwin; Zhang, Tingnan; Lee, Tsang-Wei; Tan, Jie; Levine, Sergey]
venue: ACM Transactions on Graphics (SIGGRAPH 2021)
year: 2021
tags: [character-control, physics-based-animation, reinforcement-learning, gans, motion-synthesis]
source: arXiv:2004.04802
doi: 10.1145/3450626.3459670
---

## Summary
Automated method for synthesizing graceful behaviors in physically simulated characters via adversarial imitation learning. Eliminates need to manually design imitation objectives by learning motion style from large, diverse motion datasets. Enables physics-based character control with naturalistic motion quality.

## Problem
Physics-based character control produces physically accurate but often stiff, unnatural motions. Manual imitation objectives and motion selection mechanisms are labor-intensive. Learning from diverse motion datasets requires automated, scalable approaches.

## Method
- **Adversarial imitation learning**: Discriminator distinguishes reference vs. simulated motion
- **Motion dataset learning**: Learns style from large, diverse motion capture collections
- **Generative adversarial network**: GAN-inspired approach for motion synthesis
- **Policy learning**: Reinforcement learning with GAN-based reward signal
- **Style coverage**: Supports diverse motion styles in single learned policy

## Key Results
- Natural-looking physics-based character control
- Successful learning from large motion datasets
- Diverse stylistic variations in motion behavior
- Transfer between different character morphologies

## Limitations
- Computational cost for training physics simulators and learning policies
- Quality depends on training motion dataset coverage
- Generalization to very different morphologies limited
- May require motion preprocessing and cleaning

## Connections
- [[papers/holden-2015-inverse-rig]] — character control fundamentals
- [[papers/pfaff-2021-meshgraphnets]] — neural physics alternatives
- [[papers/gat-2025-anytop]] — related motion synthesis
- [[concepts/motion-synthesis]] — neural motion generation
- [[concepts/secondary-motion]] — physics-based secondary dynamics

## Implementation Notes
- Discriminator design critical for stable adversarial training
- Motion dataset preprocessing (mocap cleanup) important
- Policy can be adapted per-character with transfer learning
- Integration with physics engines (PyBullet, MuJoCo) required

## External References
- Project page: [xbpeng.github.io/projects/AMP](https://xbpeng.github.io/projects/AMP)
- arXiv: [arxiv.org/abs/2004.04802](https://arxiv.org/abs/2004.04802)
- ACM DL: [doi.org/10.1145/3450626.3459670](https://doi.org/10.1145/3450626.3459670)
