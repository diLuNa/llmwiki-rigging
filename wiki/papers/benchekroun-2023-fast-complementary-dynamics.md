---
title: "Fast Complementary Dynamics via Skinning Eigenmodes"
authors: [Benchekroun, Otman; Zhang, Jiayi; Chaudhuri, Siddhartha; Grinspun, Eitan; Zhou, Yi; Wang, Huamin; Jiang, Chenfanfu; Yang, Yin]
venue: ACM Transactions on Graphics (SIGGRAPH 2023)
year: 2023
tags: [simulation, secondary-motion, reduced-space, eigenmode-decomposition, character-animation]
source: TBA
doi: 10.1145/3592431
---

## Summary
Method computing secondary motion via reduced-space physics simulation using novel material-sensitive, rig-aware skinning subspace. Guarantees rotation invariance while capturing joint-dependent deformations. Enables efficient, physically-plausible secondary motion generation for character animation.

## Problem
Secondary motion (muscle jiggle, clothing sway, hair bounce) is essential for animation realism but computationally expensive to simulate. Reduced-space methods require carefully designed basis; naive approaches lack physical accuracy or deformation fidelity.

## Method
- **Skinning eigenmode basis**: Material-sensitive modes capturing joint-dependent deformations
- **Rotation-invariant formulation**: Ensures correctness under skeletal rotations
- **Rig-aware design**: Modes respect skeletal hierarchy and joint constraints
- **Reduced-space solver**: Efficient physics in low-dimensional subspace
- **Material models**: Handle skin, fat, muscle, and clothing with different properties

## Key Results
- Realistic secondary motion with minimal computational overhead
- Material-specific behavior for different body tissues
- Stability and physical plausibility over heuristic methods
- Production-ready efficiency for real-time character animation

## Limitations
- Basis must be computed per-character
- Limited to small-deformation regime
- Material parameter selection affects quality
- Doesn't handle large-scale contact interactions

## Connections
- [[papers/mcadams-2011-elasticity-skinning]] — elasticity in character animation
- [[concepts/muscles]] — musculoskeletal secondary motion
- [[papers/kavan-2007-dqs]] — dual quaternion skinning
- [[papers/pfaff-2021-meshgraphnets]] — neural physics alternatives
- [[concepts/secondary-motion]] — technical foundations

## Implementation Notes
- Eigenmode computation can be done offline per character
- Skinning weights directly influence eigenmode computation
- Rotation invariance critical for non-Manhattan skeleton orientations
- Compatible with standard DCC character pipelines

## External References
- ACM DL: [doi.org/10.1145/3592431](https://doi.org/10.1145/3592431)
- SIGGRAPH 2023 proceedings
