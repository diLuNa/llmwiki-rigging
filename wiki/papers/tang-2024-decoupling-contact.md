---
title: "Decoupling Contact for Fine-Grained Motion Style Transfer"
authors: [Tang, Xin; Cai, Shuqi; Liang, Liang; Zhang, Feng; Han, Xiaogang; Zhou, Kun; Bao, Hujun]
venue: SIGGRAPH Asia 2024 Conference Papers
year: 2024
tags: [motion-retargeting, style-transfer, contact-modeling, motion-synthesis]
source: arXiv:2409.05387
doi: 10.1145/3680528.3687609
---

## Summary
Motion style transfer method enabling fine-grained control over contact while maintaining motion naturalness. Decouples hip velocity into trajectory and contact timing components, allowing independent manipulation of each aspect. Produces natural motions with explicit style expression and enhanced quality.

## Problem
Contact dynamics are essential for motion style expression but difficult to control independently. Existing style transfer methods don't explicitly account for contact timing and distribution, limiting style fidelity and naturalness of retargeted animations.

## Method
- **Hip velocity decomposition**: Trajectory and contact timing components
- **Contact timing model**: Explicit learning of when/where contacts occur
- **Style-trajectory-contact coupling**: Separate models for each component
- **Recombination**: Flexible mixing of style with target trajectory/contact
- **Naturalness preservation**: Physics-informed constraints on contact feasibility

## Key Results
- Fine-grained control over motion contacts and style
- High-quality style transfer with naturalness preservation
- Flexible style expression across diverse motion types
- Improved results over baseline style transfer methods

## Limitations
- Requires accurate contact detection/labeling in training data
- Method assumes bipedal locomotion-like contact patterns
- Generalization to non-locomotion motions limited
- Contact timing model may overfit to training data characteristics

## Connections
- [[papers/aberman-2020-unpaired-motion-style]] — unpaired motion style transfer
- [[papers/holden-2015-inverse-rig]] — motion retargeting foundations
- [[concepts/secondary-motion]] — contact-driven secondary dynamics
- [[concepts/motion-synthesis]] — neural motion generation
- [[papers/gat-2025-anytop]] — topology-agnostic motion synthesis

## Implementation Notes
- Contact labeling automation critical for scaling
- Hip velocity decomposition generalizes to various characters
- Compatible with motion capture post-processing pipelines
- Particularly effective for walking, running, and interaction motions

## External References
- arXiv: [arxiv.org/abs/2409.05387](https://arxiv.org/abs/2409.05387)
- Project page: [xjtang.com](https://xjtang.com)
- ACM DL: [doi.org/10.1145/3680528.3687609](https://doi.org/10.1145/3680528.3687609)
