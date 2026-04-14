---
title: "LayGA: Layered Gaussian Avatars for Animatable Clothing Transfer"
authors: [Lin, Siyou; Li, Zhe; Su, Zhaoqi; Zheng, Zerong; Zhang, Hongwen; Liu, Yebin]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [neural, gaussian-splatting, avatars, clothing, virtual-try-on]
source: arXiv:2405.07319
doi: 10.1145/3641519.3657501
---

## Summary
Representation separating body and clothing layers for photorealistic animatable clothing transfer from multi-view video. Builds on Gaussian map-based avatars with two-stage training for smooth surface reconstruction and body-clothing segmentation. Enables virtual try-on and clothing retargeting across identities.

## Problem
Traditional avatar methods entangle body and clothing geometry, preventing accurate garment tracking, sliding motion representation, and clothing transfer. Separation enables precise deformation modeling and cross-identity virtual try-on applications.

## Method
- **Layered Gaussian representation**: Separate body and clothing Gaussian distributions
- **Two-stage training**: Single-layer reconstruction followed by multi-layer fitting
- **Geometric constraints**: Smooth surface reconstruction with body-clothing collision handling
- **Segmentation learning**: Automatic detection of clothing-body boundaries from video

## Key Results
- Photorealistic animations with separated body and clothing layers
- Accurate garment deformation and sliding motion
- Successful virtual try-on across identities and poses
- Outperforms single-layer baseline methods in garment fidelity

## Limitations
- Requires multi-view video input for high quality
- Segmentation accuracy depends on clothing-body contrast
- Complex multi-layer garments may require manual supervision
- Limited to seen clothing-body combinations

## Connections
- [[papers/pfaff-2021-meshgraphnets]] — related neural geometry learning
- [[papers/li-2017-flame]] — body model foundation
- [[papers/giebenhain-2024-npga]] — neural appearance modeling
- [[concepts/blendshapes]] — body deformation controls
- [[techniques/ml-deformer]] — learned deformation networks

## Implementation Notes
- Gaussian map representation avoids explicit surface reconstruction
- Collision detection between layers critical for stable simulation
- Training stability improved through phased optimization
- Compatible with physics-based cloth simulation tools

## External References
- Project page: [jsnln.github.io/layga](https://jsnln.github.io/layga)
- arXiv: [arxiv.org/abs/2405.07319](https://arxiv.org/abs/2405.07319)
- ACM DL: [doi.org/10.1145/3641519.3657501](https://doi.org/10.1145/3641519.3657501)
