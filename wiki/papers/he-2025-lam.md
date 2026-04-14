---
title: "LAM: Large Avatar Model for One-shot Animatable Gaussian Head"
authors: [He, Yisheng; Gu, Xiaodong; Ye, Xiaodan; Xu, Chao; Zhao, Zhengyi; Dong, Yuan; Yuan, Weihao; Dong, Zilong; Bo, Liefeng]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [neural, avatars, gaussian-splatting, facial-animation, head-generation]
source: arXiv:2502.17796
doi: 10.1145/3721238.3730706
---

## Summary
Large avatar model (LAM) for generating animatable Gaussian head avatars in a single forward pass from minimal input. Uses canonical Gaussian attributes generator leveraging FLAME canonical points as queries with multi-scale image features. Enables real-time reenactment and rendering without additional networks or post-processing.

## Problem
Generating high-quality, animatable 3D head avatars efficiently requires either expensive per-subject optimization or complex post-processing pipelines. Existing methods struggle with one-shot generation while maintaining animation quality and real-time performance.

## Method
- **Canonical Gaussian generator**: Transformer-based network predicting Gaussian attributes in canonical space using FLAME landmarks
- **Linear blend skinning**: Standard LBS with corrective blendshapes for animation control
- **Multi-scale feature fusion**: Hierarchical extraction and combination of image features at multiple scales
- **Real-time rendering**: Direct Gaussian splatting without additional post-processing

## Key Results
- One-shot generation in seconds without per-subject optimization
- Real-time animation via standard LBS pipeline
- Outperforms state-of-the-art methods on existing benchmarks
- Directly animatable with FLAME-compatible rigging

## Limitations
- Quality depends on input image resolution and lighting conditions
- Limited to head region (not full-body avatars)
- Animation quality bounded by FLAME model expressiveness

## Connections
- [[papers/li-2017-flame]] — morphable face model foundation
- [[papers/pfaff-2021-meshgraphnets]] — related neural geometry learning
- [[papers/giebenhain-2024-npga]] — neural appearance Gaussian heads
- [[concepts/blendshapes]] — corrective animation controls
- [[concepts/nonlinear-face-models]] — neural face modeling

## Implementation Notes
- FLAME canonical points enable structured, skeleton-aware Gaussian prediction
- Compatible with standard DCC animation pipelines (Houdini, Maya, Blender)
- Multi-scale feature extraction crucial for detail preservation
- Real-time inference enables interactive character control

## External References
- GitHub: [github.com/aigc3d/LAM](https://github.com/aigc3d/LAM)
- ACM DL: [doi.org/10.1145/3721238.3730706](https://doi.org/10.1145/3721238.3730706)
- arXiv: [arxiv.org/abs/2502.17796](https://arxiv.org/abs/2502.17796)
