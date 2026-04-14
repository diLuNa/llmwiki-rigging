---
title: "AniPortraitGAN: Animatable 3D Portrait Generation from 2D Image Collections"
authors: [Wu, Yue; Xu, Sicheng; Xiang, Jianfeng; Wei, Fangyun; Chen, Qifeng; Yang, Jiaolong; Tong, Xin]
venue: SIGGRAPH Asia 2023 Conference Papers
year: 2023
tags: [neural, 3d-generation, gans, facial-animation, portrait-modeling]
source: arXiv:2309.02186
doi: 10.1145/3610548.3618164
---

## Summary
Animatable 3D-aware GAN generating photorealistic portrait animations from 2D image collections. Uses generative radiance manifold representation with learnable facial expression and head-shoulder deformations. Dual-camera rendering with adversarial learning improves portrait quality including shoulders.

## Problem
Existing animatable 3D-aware GANs for human generation focus on either full body (low facial quality) or head-only (uncommon in videos). Portrait-style avatars with shoulders and full head animation control are underexplored but valuable for video synthesis and telepresence applications.

## Method
- **Generative radiance manifold**: 3D representation balancing rendering quality and animation flexibility
- **Facial and shoulder deformations**: Learnable transform networks for expression and pose control
- **Dual-camera rendering**: Different views for improved quality
- **Adversarial training**: Multi-scale discriminators for portrait-specific cues
- **Unstructured image collection**: Requires no correspondence between training images

## Key Results
- High-quality portrait animations with head and shoulder movements
- Facial expression control via latent code manipulation
- Head pose variations supported
- Outperforms single-region generation in portrait quality

## Limitations
- Limited to portrait composition (head + shoulders)
- Extreme poses may produce artifacts
- Requires collection of similar portrait images for training
- Generalization to different ethnicities/ages depends on training diversity

## Connections
- [[papers/li-2017-flame]] — morphable face model foundation
- [[papers/he-2025-lam]] — related avatar generation approach
- [[papers/tan-2024-soap]] — related 3D portrait generation
- [[concepts/blendshapes]] — facial animation controls
- [[concepts/nonlinear-face-models]] — neural face modeling

## Implementation Notes
- Dual-camera rendering adds computational cost but improves quality
- Adversarial training requires careful balancing of loss terms
- Image collection preprocessing (alignment) helpful for convergence
- Compatible with standard DCC tools for animation export

## External References
- GitHub: [github.com/kathrinawu/AniPortraitGAN](https://github.com/kathrinawu/AniPortraitGAN)
- arXiv: [arxiv.org/abs/2309.02186](https://arxiv.org/abs/2309.02186)
- ACM DL: [doi.org/10.1145/3610548.3618164](https://doi.org/10.1145/3610548.3618164)
