---
title: "Hierarchical Neural Skinning Deformation with Self-supervised Training for Character Animation"
authors: [Gao, Xingyi; Zeng, Lingfeng; Chen, Tongtong; Wu, Junjie; Hao, Aimin; Qin, Hong]
venue: ACM Transactions on Graphics
year: 2024
tags: [neural, deformation, secondary-motion, self-supervised, character-animation, muscles]
source: TBA
doi: 10.1145/3728300
---

## Summary
Self-supervised hierarchical framework for soft-body character animation via graph-based neural networks. Decomposes deformation into musculoskeletal and adipose tissue layers powered by Multi-Scale Edge Aggregation Mesh Graph Networks. Formulates secondary motion as energy optimization problem without requiring ground-truth data.

## Problem
Real-time character animation requires efficient soft-body deformation modeling accounting for muscles, fat, and skin. Obtaining ground-truth data for training neural deformation models is expensive. Balancing biomechanical accuracy with computational efficiency is critical.

## Method
- **Hierarchical decomposition**: Separate neural emulators for musculoskeletal and soft-tissue layers
- **MSEA-MGN architecture**: Multi-scale edge aggregation mesh graph networks for arbitrary topologies
- **Energy formulation**: Constrained secondary motion as potential energy minimization
- **Self-supervised training**: Biomechanical material models as implicit supervision

## Key Results
- High-quality soft-body deformations without ground-truth training data
- Generalization across arbitrary mesh topologies
- Significant speedups over full physics simulation
- Improved anatomical plausibility over standard LBS

## Limitations
- Energy formulation complexity limits very stiff materials
- Graph network scalability for very large meshes
- Material parameter selection affects convergence
- Limited to smooth secondary motions

## Connections
- [[papers/mcadams-2011-elasticity-skinning]] — elasticity for skinning
- [[papers/kavan-2007-dqs]] — dual quaternion skinning
- [[papers/pfaff-2021-meshgraphnets]] — mesh graph networks
- [[concepts/muscles]] — musculoskeletal modeling
- [[techniques/ml-deformer]] — neural deformation learning

## Implementation Notes
- Graph network design critical for topological generalization
- Energy minimization provides interpretable supervision signal
- Compatible with Houdini geometry for deformable characters
- Training cost reduced through self-supervised approach

## External References
- ACM DL: [doi.org/10.1145/3728300](https://doi.org/10.1145/3728300)
- SIGGRAPH 2024 proceedings
