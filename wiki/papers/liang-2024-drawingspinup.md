---
title: "DrawingSpinUp: 3D Animation from Single Character Drawings"
authors: [Liang, Yulong; Deng, Chaoyi; Zhang, Peizhuo; Cai, Runyi; Wang, Junshu; Zhang, Xiaodan; Chen, Yifan; Yang, Anan]
venue: SIGGRAPH Asia 2024 Conference Papers
year: 2024
tags: [neural, 3d-generation, image-to-3d, character-animation, stylization]
source: arXiv:2409.08615
doi: 10.1145/3680528.3687593
---

## Summary
First 3D-aware animation system generating non-planar 3D animations from single 2D character drawings with target 3D motions. Preserves consistent artistic style while synthesizing 3D geometry and deformation. Enables bringing amateur character drawings to life with complex 3D movements.

## Problem
Existing animation methods limited to flat 2D motion synthesis from drawings. Image-to-3D methods fail on amateur-quality character drawings due to appearance and geometry reconstruction challenges. Gap between 2D drawings and 3D animation rigging makes style transfer difficult.

## Method
- **3D-aware diffusion**: Image-conditioned generation of 3D geometry and appearance
- **Style preservation**: Maintains artistic characteristics of source drawing
- **Motion-driven deformation**: Applies target 3D motion to generated mesh
- **Temporal coherence**: Ensures smooth animation across keyframes
- **Style transfer network**: Maps 2D drawing style to 3D geometry texture

## Key Results
- Successfully generates plausible 3D animations from diverse character drawings
- Maintains drawing style in synthesized 3D models
- Supports complex 3D motions (jumping, dancing, spinning)
- Handles stylized and semi-abstract character designs

## Limitations
- Quality depends on drawing clarity and style consistency
- Complex articulated characters may require simplification
- Automatic rigging may need manual adjustment
- Handles torso/limbs better than intricate details (hands, face)

## Connections
- [[papers/zhou-2017-mesh-vae]] — mesh-based neural shape learning
- [[papers/gat-2025-anytop]] — motion synthesis across topologies
- [[papers/xu-2020-rignet]] — automatic rigging
- [[concepts/auto-rigging]] — skeleton and weight generation
- [[techniques/ml-deformer]] — learned deformation networks

## Implementation Notes
- Foreground segmentation and joint keypoint detection critical preprocessing
- Style consistency requires multi-scale feature matching
- Compatible with standard DCC tools for animation refinement
- PyTorch implementation enables easy integration

## External References
- GitHub: [github.com/LordLiang/DrawingSpinUp](https://github.com/LordLiang/DrawingSpinUp)
- Project page: [lordliang.github.io/DrawingSpinUp](https://lordliang.github.io/DrawingSpinUp/)
- arXiv: [arxiv.org/abs/2409.08615](https://arxiv.org/abs/2409.08615)
- ACM DL: [doi.org/10.1145/3680528.3687593](https://doi.org/10.1145/3680528.3687593)
