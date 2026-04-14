---
title: "Skeleton-Aware Networks for Deep Motion Retargeting"
authors: [Aberman, Kfir; Li, Yijia; Lischinski, Dani; Cohen-Or, Daniel; Zhang, Jing; Hanocka, Rana]
venue: ACM Transactions on Graphics (SIGGRAPH 2020)
year: 2020
tags: [motion-retargeting, neural-networks, skeleton-hierarchy, deep-learning, animation]
source: arXiv:2005.05732
doi: 10.1145/3386569.3392462
---

## Summary
Deep learning framework for motion retargeting between skeletons with different structures. Introduces skeleton-aware convolution, pooling, and unpooling operators that explicitly account for hierarchical structure and joint adjacency. Learns mapping without requiring explicit motion pairing in training set.

## Problem
Neural motion retargeting requires handling variable skeleton topologies and structures. Standard convolution operations don't respect skeletal hierarchy. Learning from unpaired motion collections requires discovering structure-invariant representations.

## Method
- **Skeleton pooling**: Merges edges via hierarchical reduction to common primal skeleton
- **Skeleton-aware convolution**: Operations respect adjacency and hierarchy
- **Skeleton-aware unpooling**: Reconstructs target skeleton structure from compressed representation
- **Differentiable operators**: Enable end-to-end neural network training
- **Unsupervised learning**: No paired motion data required

## Key Results
- Accurate retargeting between diverse skeleton topologies
- Better generalization than topology-specific methods
- Works without paired training data
- Handles variable joint counts and structures

## Limitations
- Assumes roughly homomorphic skeletons (similar articulation types)
- Generalization to very unusual morphologies limited
- Computational overhead from skeleton-aware operations
- Requires motion preprocessing and cleaning

## Connections
- [[papers/zhang-2025-unirig]] — unified topology rigging
- [[papers/xu-2020-rignet]] — neural rigging methods
- [[papers/holden-2015-inverse-rig]] — motion retargeting foundations
- [[concepts/auto-rigging]] — automatic rig generation
- [[papers/loper-2015-smpl]] — parametric body models

## Implementation Notes
- Pooling strategy critical for effective skeleton compression
- Skeleton hierarchy must be extracted before network input
- Compatible with various motion capture systems
- Scalable to diverse character types and morphologies

## External References
- Project page: [deepmotionediting.github.io/retargeting](https://deepmotionediting.github.io/retargeting)
- arXiv: [arxiv.org/abs/2005.05732](https://arxiv.org/abs/2005.05732)
- ACM DL: [doi.org/10.1145/3386569.3392462](https://doi.org/10.1145/3386569.3392462)
