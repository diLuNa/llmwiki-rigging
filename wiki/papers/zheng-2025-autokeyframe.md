---
title: "AutoKeyframe: Autoregressive Keyframe Generation for Human Motion Synthesis and Editing"
authors: [Zheng, Bowen; Chen, Ke; Yao, Yuxin; Zeng, Zijiao; Jiang, Xinwei; Wang, He; Lasenby, Joan; Jin, Xiaogang]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [neural, motion-synthesis, keyframing, character-animation, diffusion]
source: arXiv:TBA
doi: 10.1145/3721238.3730664
---

## Summary
Autoregressive framework for automatic keyframe generation balancing dense and sparse motion controls. Directly generates key postures at critical timings from both overall motion trajectories (dense) and explicit pose constraints (sparse). Enables labor-efficient animation generation while maintaining fine-grained control.

## Problem
Keyframing has been the cornerstone of character animation, offering precise pose control but requiring intensive manual labor. Automating keyframe selection and generation while balancing control inputs (trajectory, sparse pose targets) is a central research challenge.

## Method
- **Autoregressive generation**: Sequential keyframe prediction conditioned on motion context and control signals
- **Dual control signals**: Dense trajectory control and sparse pose constraints simultaneously
- **Transformer architecture**: Sequence-to-sequence modeling of control-to-keyframe mapping
- **Motion quality optimization**: Per-keyframe loss ensuring naturalness and temporal coherence

## Key Results
- Generates high-quality keyframe sequences from mixed dense/sparse controls
- Reduces manual animation labor while preserving artistic intent
- Handles diverse motion types (walk, dance, gestures, interactions)
- Quantitative improvements over baseline keyframe selection methods

## Limitations
- Output quality depends on input control signal density and accuracy
- Generalization to highly specialized motions requires additional training
- Requires paired training data (trajectories + keyframes) which is costly
- Temporal artifacts possible at keyframe boundaries

## Connections
- [[papers/holden-2015-inverse-rig]] — inverse kinematics for pose specification
- [[papers/gat-2025-anytop]] — related motion synthesis across topologies
- [[concepts/motion-synthesis]] — neural motion generation
- [[techniques/ml-deformer]] — learned deformation approximation
- [[concepts/secondary-motion]] — enriching skeletal motion

## Implementation Notes
- Works with any skeleton topology via embedding-based representation
- Compatible with standard motion capture preprocessing
- Can be integrated with existing animation pipelines via keyframe export
- Batch generation enables rapid iteration

## External References
- GitHub: [github.com/Cr7st/AutoKeyframe](https://github.com/Cr7st/AutoKeyframe)
- ACM DL: [doi.org/10.1145/3721238.3730664](https://doi.org/10.1145/3721238.3730664)
