---
title: "Neutral Facial Rigging from Limited Spatiotemporal Meshes"
authors: [Hou, Jing; Weng, Dongdong; Zhao, Zhihe; Li, Ying; Zhou, Jixiang]
venue: Electronics (MDPI) 2024
year: 2024
tags: [rig-generation, blendshapes, neural, digital-human, auto-rigging]
source: raw/papers/Neutral_Facial_Rigging_from_Limited_Spatiotemporal.pdf
---

## Summary
An automatic facial rigging method that generates a large expression dataset from a limited set of spatiotemporal face meshes, then trains two networks: RigGenNet (MLP mapping semantic parameters → joint positions) and RigRecogNet (GAN-like network for inverse mapping joint positions → semantic parameters). Local vertex constraints on eyes and lips improve recognition accuracy. Achieves 14.78 ms generation, 92.92% expression recognition accuracy.

## Problem
Manual facial rigging requires expert labour. Existing learning-based methods either lack semantic interpretability (PCA blendshapes) or require large labeled 3D datasets that are expensive to produce.

## Method
**Dataset expansion:** A projection-searching algorithm selects optimal 3D masks for eyes/lips and generates a large training set from a small number of input spatiotemporal meshes by interpolating semantic parameters and joint positions.

**RigGenNet:** MLP with local vertex constraints:
- Input: semantic expression parameters
- Output: joint positions
- Vertex constraints enforce geometric consistency between semantic codes and joint locations

**RigRecogNet:** GAN-like bidirectional network:
- Input: joint positions
- Output: semantic expression parameters
- Adversarial training improves parameter recovery quality

**Local constraints:** 3D masks for eye and lip regions, computed via projection-searching, focus network attention on high-deformation facial sub-regions.

## Key Results
- Generation time: 14.78 ms (real-time)
- Vertex RMSE: 1.57×10⁻³ (best among comparisons)
- Recognition accuracy: 92.92%
- Local constraints improve recognition by 3.02%; projection-searching adds 1.03%

## Limitations
- Relies heavily on Metahuman topology; limited cross-topology evaluation
- Journal paper (Electronics MDPI) — lower bar than conference venues; limited qualitative comparison with concurrent SIGGRAPH-tier work
- Dataset expansion via interpolation may not capture full expression diversity

## Connections
- [[papers/qin-2023-nfr]] — NFR is the more technically rigorous approach to the same problem
- [[papers/ma-2025-riganyface]] — RigAnyFace is the more scalable successor
- [[papers/li-2017-flame]] — references FLAME as a face model foundation
- [[concepts/auto-rigging]] — bidirectional rig generation and inversion
- [[concepts/rig-inversion]] — RigRecogNet is a rig inversion network
