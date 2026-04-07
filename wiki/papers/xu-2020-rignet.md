---
title: "RigNet: Neural Rigging for Articulated Characters"
authors: [Xu, Zhan; Zhou, Yang; Kalogerakis, Evangelos; Landreth, Chris; Singh, Karan]
venue: ACM Transactions on Graphics (SIGGRAPH 2020)
year: 2020
tags: [rig-generation, skinning, neural, weights, lbs, auto-rigging]
source: raw/papers/2005.00559v2.pdf
---

## Summary
RigNet is an end-to-end deep learning system that predicts both a skeleton and skinning weights from a bare 3D character mesh, requiring no pre-defined template. Trained on 2,703 rigged characters spanning humanoids, quadrupeds, and creatures, it uses graph neural networks to localize joints, predict bone connectivity, and compute skinning weight distributions. The result is an animation-ready rig matching animator intuitions across diverse character morphologies.

## Problem
Traditional rigging is manual and expert-intensive. Template-fitting methods (e.g., Pinocchio) fail when character topology deviates from the template. Prior learning-based work either loses surface detail via voxelization, handles only fixed shape classes, or solves skeleton and skinning separately without a unified framework.

## Method
Three-stage modular architecture, each trained with supervision from the dataset:

**Stage 1 — Joint Prediction:**
GMEdgeNet combines mesh-topology neighbours $N_m(v)$ and geodesic-ball neighbours $N_d(v)$ (radius 0.06 of bounding box diagonal):
```math
x'_v = \text{MLP}\!\left(\text{concat}\!\left(\max_{u\in N_m}\ \text{MLP}(x_v,\, x_u-x_v),\;\; \max_{u\in N_d}\ \text{MLP}(x_v,\, x_u-x_v)\right)\right)
```
Each vertex votes toward a candidate joint via a learned displacement $q_v = v + f_d(v)$, modulated by attention $a_v = f_a(v) \in [0,1]$. Joints are extracted via attention-weighted mean-shift clustering with a learnable bandwidth $h$.

**Stage 2 — Bone Connectivity:**
BoneNet predicts pairwise bone probability $p_{i,j} = \sigma(\text{MLP}(f_{i,j}, g_s, g_t))$ for each joint pair, using joint positions, shape features, and geometric heuristics (e.g., fraction of the bone exterior to the mesh). A Minimum Spanning Tree on $-\log p_{i,j}$ gives the final skeleton topology. A separate RootNet selects the root joint.

**Stage 3 — Skinning Weights:**
Per-vertex features are augmented with volumetric geodesic distances $D_{r,v}$ to the $K=5$ closest bones. A GMEdgeNet predicts raw weights, normalized via softmax to guarantee non-negativity and partition-of-unity.

**Training losses:**
- Joints: symmetric Chamfer distance + binary attention supervision
- Connectivity: binary cross-entropy with hard example mining
- Skinning: cross-entropy against reference weight distributions

## Key Results
On a 270-character test set:
- Joint IoU 61.6% vs Pinocchio 36.5% and Xu et al. 2019 53.7%
- Skinning precision/recall 82.3%/80.8%, avg L1 0.39 — outperforms BBW and NeuroSkinning
- Generalizes qualitatively to fish, robots, toys, non-humanoid creatures

## Limitations
- Per-stage training prevents end-to-end gradient flow
- One rig per training character — misses secondary/helper joints (clothing, accessories)
- Ambiguous skeleton topologies; model learns one mode
- No guarantee of resolution/tessellation invariance

## Connections
- [[papers/jacobson-2011-bbw]] — BBW is the baseline skinning method RigNet replaces/outperforms
- [[papers/le-2012-ssdr]] — SSDR extracts LBS rigs from animation data (different direction of auto-rigging)
- [[papers/pfaff-2021-meshgraphnets]] — both use GNN/message-passing on mesh graphs for character simulation
- [[papers/holden-2015-inverse-rig]] — inverse rig mapping: the complementary problem
- [[concepts/auto-rigging]] — RigNet is the canonical reference for end-to-end neural auto-rigging
- [[concepts/linear-blend-skinning]] — predicted skinning weights drive LBS at runtime
- [[authors/kalogerakis-evangelos]]
- [[authors/singh-karan]]

## Implementation Notes
The joint prediction bandwidth $h$ doubles as a level-of-detail parameter — increasing $h$ merges nearby candidate joints into coarser rig. The dataset (ModelsResource-RigNet) is publicly available. Inference on a single mesh takes a few seconds on GPU.
