---
title: "UniRig: One Model to Rig Them All: Diverse Skeleton Rigging with UniRig"
authors: [Zhang, Jia-Peng; Pu, Cheng-Feng; Guo, Meng-Hao; Cao, Yan-Pei; Hu, Shi-Min]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [neural, rig-generation, skeleton, auto-rigging, skinning]
source: arXiv:2504.12451
doi: 10.1145/3730930
---

## Summary
Large autoregressive transformer model (UniRig) for automatic skeletal rigging of diverse character types (humans, creatures, mechanical). Trained on 14K diverse rigged characters and can predict joint hierarchy, positions, and skinning weights end-to-end from static meshes. Achieves state-of-the-art generalization across topology-agnostic rigging.

## Problem
Existing neural rigging methods focus on specific character categories (human bodies, faces). A unified model that handles humans, creatures, quadrupeds, mechanical rigs, and extreme morphologies requires diverse training data and architecture capable of capturing universal rigging patterns.

## Method
- **Data**: 14K diverse rigged characters spanning multiple categories
- **Architecture**: Autoregressive transformer predicting joint positions, hierarchy, and weights sequentially
- **Input**: Mesh vertices and faces (topology-independent)
- **Output**: Skeletal structure (joint positions, hierarchy) + skinning weights

## Key Results
- Generalizes across human, creature, quadruped, and mechanical rigs
- Outperforms prior topology-specific methods (RigNet, RigAnyFace)
- Produces valid, usable rigs directly from static geometry

## Limitations
- Requires large diverse dataset (not ideal for specialized morphologies)
- Autoregressive decoding slower than feed-forward alternatives
- Joint hierarchy prediction may require post-correction for complex branching

## Connections
- [[papers/xu-2020-rignet]] — prior neural rigging (human-focused)
- [[papers/qin-2023-nfr]] — neural face rigging (topology-agnostic)
- [[papers/ma-2025-riganyface]] — RigAnyFace (prior SOTA)
- [[papers/hou-2024-neutral-facial-rigging]] — neutral rigging from limited data
- [[concepts/auto-rigging]] — automated rig generation
- [[techniques/ml-deformer]] — downstream application (learned deformation)

## External References
- arXiv: [arxiv.org/abs/2504.12451](https://arxiv.org/abs/2504.12451)
- ACM DL: [doi.org/10.1145/3730930](https://doi.org/10.1145/3730930)
