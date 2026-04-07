---
title: "RigAnyFace: Scaling Neural Facial Mesh Auto-Rigging with Unlabeled Data"
authors: [Ma, Wenchao; Kneubuehler, Dario; Chu, Maurice; Sachs, Ian; Jiang, Haomiao; Huang, Sharon X.]
venue: NeurIPS 2025
year: 2025
tags: [rig-generation, blendshapes, neural, digital-human, auto-rigging]
source: raw/papers/2511.18601v1.pdf
---

## Summary
RigAnyFace (RAF) is a scalable neural facial auto-rigging system that generates industry-standard FACS blendshape rigs for arbitrary facial meshes including those with multiple disconnected components (eyeballs, teeth). The core contributions are: (1) a modified DiffusionNet with a global encoder to handle disconnected parts without inter-component vertex penetration, (2) 2D displacement supervision using optical flow on rendered images to leverage large amounts of unlabeled (un-rigged) meshes for training. RAF achieves 25% lower error than NFR on matched test sets and uniquely generalises to non-humanoid stylised faces.

## Problem
Existing methods (NFR, template transfer) fail on disconnected component meshes and require expensive manually-rigged assets for all 3D supervision. The scarcity of ground-truth rigged data bottlenecks scalability.

## Method
**Architecture (modified DiffusionNet):**

*Global encoder*: A small 2-layer DiffusionNet processes the full neutral mesh $M_0$ including all disconnected components → global pooled feature $G_0 \in \mathbb{R}^{d}$.

*FACS conditioning*: FACS pose vector $A_i$ concatenated with $G_0$, replicated across vertices, and fused into each DiffusionNet diffusion block.

Network input: neutral mesh $M_0$ + FACS pose $A_i$; output: per-vertex displacement $\hat{d}_i$:
```math
\hat{M}_i = (V_0 + \hat{d}_i,\; F)
```
This directly produces the FACS target shape (one forward pass per FACS pose = one blendshape).

**2D displacement supervision (key innovation):**
For unlabeled meshes, ground-truth 2D displacement is derived by:
1. Render neutral from mesh → $I_0$
2. Apply a pre-trained 2D face animation model to generate $I_i$ (posed image)
3. Estimate optical flow $d^{2d}_i$ between $I_0$ and $I_i$ using RAFT

Training loss Stage 1 (coarse, unlabeled + labeled, 2D only):
```math
\mathcal{L}_{s1} = \alpha_1 \mathcal{L}_{img} + \alpha_2 \mathcal{L}_{mask} + \alpha_3 \mathcal{L}_{dis\text{-}2d} + \alpha_4 \mathcal{L}_{reg}
```

Training loss Stage 2 (fine, labeled only, full 3D supervision):
```math
\mathcal{L}_{s2} = \alpha_1 \mathcal{L}_{img} + \alpha_2 \mathcal{L}_{mask} + \alpha_3 \mathcal{L}_{mse\text{-}3d} + \alpha_4 \mathcal{L}_{lmk} + \alpha_5 \mathcal{L}_{ec}
```

## Key Results
- vs NFR on humanoid subset: MAE 1.82 vs 2.41 mm (25% lower), Q95 5.47 vs 7.12 mm (23% lower)
- Global encoder reduces inter-component penetration rate from 0.377 to 0.173 (54%)
- Ablation: unlabeled data adds 5%, 2D displacement loss adds 4.6% on Q95
- Generalises to Objaverse/CGTrader assets and non-humanoid faces where NFR largely fails
- Applications: FACS rig editing, video-to-mesh retargeting, text-to-3D animation
- 5.4M parameters; 3.1s inference on Nvidia T4 GPU

## Limitations
- Shell-like meshes with insufficient geometric detail show degraded performance
- Meshes with unintended disconnections (bad triangulation) lose spatial coherence
- 2D supervision generation requires a pre-trained face animation model fine-tuned on a small seed set

## Connections
- [[papers/qin-2023-nfr]] — NFR is the direct predecessor; RAF extends it with disconnected components and 2D scaling
- [[papers/pfaff-2021-meshgraphnets]] — both use mesh-aware GNNs; DiffusionNet generalises where MeshGraphNets require fixed topology
- [[papers/choi-2022-animatomy]] — Animatomy rig could be a target for RAF retargeting
- [[papers/canrig-2026-neural-face-rigging]] — concurrent neural facial rigging approach
- [[concepts/auto-rigging]] — RAF and NFR are the main neural facial auto-rigging references
- [[concepts/blendshapes]] — output is a FACS linear blendshape rig
