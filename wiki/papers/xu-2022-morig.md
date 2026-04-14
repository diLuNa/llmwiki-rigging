---
title: "MoRig: Motion-Aware Rigging of Character Meshes from Point Clouds"
authors: [Xu, Zhan; Yang, Zhou; Yang, Zeng; Kang, Hao; Lovegrove, Steven; Vedaldi, Andrew; Cremers, Daniel; Novotny, David]
venue: SIGGRAPH Asia 2022 Conference Papers
year: 2022
tags: [neural, auto-rigging, skeleton-extraction, point-cloud-input, motion-capture]
source: arXiv:2210.09463
doi: 10.1145/3550469.3555390
---

## Summary
Method for automatic rigging of 3D character meshes from single-view point cloud motion sequences. Uses neural network encoding motion cues to guide skeleton inference for diverse character types (humanoids, quadrupeds, toys). Handles occlusion and part proportion mismatches between mesh and captured motion.

## Problem
Existing auto-rigging methods focus on static mesh input or require complete geometry. Motion capture point clouds are inherently partial and dynamic. Leveraging motion information can improve rig quality by disambiguating skeletal structure from incomplete geometry.

## Method
- **Point cloud encoder**: Neural network processing partial/occluded point clouds
- **Motion context**: Temporal sequences encode movement patterns and articulation
- **Skeleton prediction**: Multi-stage refinement of joint positions and hierarchy
- **Weight computation**: Automatic skinning weight solving from encoded features
- **Occlusion handling**: Implicit geometric reasoning from motion cues

## Key Results
- Accurate skeleton prediction from point cloud motion sequences
- Handles diverse character morphologies (humanoids, quadrupeds, toys)
- Robustness to occlusion and geometric mismatches
- Produces animation-ready rigs suitable for motion retargeting

## Limitations
- Requires continuous motion sequences (single frames insufficient)
- Skeletal complexity limited to typical character articulation
- Generalization to unusual morphologies requires additional training
- Point cloud quality affects skeleton accuracy

## Connections
- [[papers/xu-2020-rignet]] — RigNet neural rigging (mesh-based)
- [[papers/zhang-2025-unirig]] — unified diverse topology rigging
- [[papers/ma-2025-riganyface]] — character-specific neural rigging
- [[concepts/auto-rigging]] — automatic skeleton extraction
- [[papers/loper-2015-smpl]] — parametric body models

## Implementation Notes
- Motion encoding critical for disambiguation of skeletal structure
- Multi-view or monocular point clouds both supported
- Handles occluded regions through learned implicit geometry
- Compatible with standard DCC rigging workflows

## External References
- GitHub: [github.com/zhan-xu/MoRig](https://github.com/zhan-xu/MoRig)
- Project page: [zhan-xu.github.io/motion-rig](https://zhan-xu.github.io/motion-rig/)
- arXiv: [arxiv.org/abs/2210.09463](https://arxiv.org/abs/2210.09463)
- ACM DL: [doi.org/10.1145/3550469.3555390](https://doi.org/10.1145/3550469.3555390)
