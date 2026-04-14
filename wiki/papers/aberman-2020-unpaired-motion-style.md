---
title: "Unpaired Motion Style Transfer from Video to Animation"
authors: [Aberman, Kfir; Weng, Yiming; Lischinski, Dani; Cohen-Or, Daniel; Chen, Baoquan]
venue: ACM Transactions on Graphics (SIGGRAPH 2020)
year: 2020
tags: [motion-retargeting, style-transfer, video-input, unsupervised-learning, animation]
source: arXiv:2005.05732
doi: 10.1145/3386569.3392469
---

## Summary
Data-driven framework for motion style transfer learning from unpaired motion collections with style labels. Extracts motion styles from either 3D joint positions or 2D video, enabling transfer of observed styles to reference animations. Supports style transfer across motion types not seen during training.

## Problem
Paired motion data for style transfer is expensive to collect. Unpaired learning requires discovering shared representations between 3D and video domains and learning style-invariant motion features for generalization.

## Method
- **Common embedding space**: Learns unified representation from 3D and 2D styles
- **Unsupervised learning**: No paired motion correspondences required
- **Style extraction**: Encodes style from video or 3D motion capture
- **Style application**: Combines content motion with extracted style
- **Domain alignment**: Bridges gap between 3D animation and 2D video spaces

## Key Results
- Successful style transfer from videos to 3D animations
- Works with unpaired, diverse motion collections
- Generalizes to motion types not in training set
- Maintains content motion structure with style variation

## Limitations
- Quality depends on motion style distinctness
- Video preprocessing (pose estimation) affects accuracy
- Generalization to very different motion types limited
- May require motion cleaning and preprocessing

## Connections
- [[papers/aberman-2017-style-transfer]] — related motion style research
- [[papers/holden-2015-inverse-rig]] — motion retargeting foundations
- [[papers/gat-2025-anytop]] — topology-agnostic motion synthesis
- [[concepts/motion-synthesis]] — neural motion generation
- [[papers/zhou-2017-mesh-vae]] — VAE-based shape/motion learning

## Implementation Notes
- Style loss design critical for effective transfer
- Video pose estimation quality impacts style extraction
- Encoder sharing between 3D and 2D domains enables domain bridging
- Compatible with motion capture preprocessing pipelines

## External References
- Project page: [deepmotionediting.github.io/style_transfer](https://deepmotionediting.github.io/style_transfer)
- arXiv: [arxiv.org/abs/2005.05732](https://arxiv.org/abs/2005.05732)
- ACM DL: [doi.org/10.1145/3386569.3392469](https://doi.org/10.1145/3386569.3392469)
