---
title: "ImFace++: A Sophisticated Nonlinear 3D Morphable Face Model"
authors: [Zheng, Mingwu; Yang, Hongyu; Huang, Di; Chen, Liming]
venue: IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI 2024)
year: 2023
tags: [neural, digital-human, blendshapes, rig-generation]
source: raw/papers/2312.04028v3.pdf
---

## Summary
ImFace++ extends ImFace with a richer deformation model, improved disentanglement of identity/expression/pose, and additional applications including face editing, expression transfer, and ear-to-ear reconstruction. It introduces an RDF (Radial Deformation Field) space model and a two-stage architecture with sub-networks for coarse and fine deformation components.

## Problem
ImFace demonstrates the power of implicit neural face models but has limited expressiveness for fine-scale deformation and limited application range (no editing, no cross-subject expression transfer). A more sophisticated version that supports the full pipeline of digital human workflows is needed.

## Method
**Extensions over ImFace:**

- **RDF space model**: introduces a Radial Deformation Field that separates global pose (large-scale rigid motion) from local expression deformation (small-scale non-rigid). Allows better generalization to unseen head poses.

- **Two-stage deformation**: 
  - Stage 1 (coarse): global shape + expression morphing in a coarse SDF space.
  - Stage 2 (fine): high-frequency detail refinement using localized implicit functions over the coarse result.

- **Sub-network structure**: separate MLPs for identity, expression, and pose sub-components — each a function of its own latent code — combined additively in deformation space.

- **Meaningful latent space**: latent codes are individual-independent (shared across subjects for expression), enabling expression transfer and editing without per-subject finetuning.

**Applications demonstrated:**
- Face reconstruction from images
- Expression transfer across identities
- Ear-to-ear 3D face completion
- Semantic face editing (change expression/identity independently)

## Key Results
- Outperforms ImFace and FLAME on reconstruction accuracy and expression disentanglement.
- High-quality expression transfer across diverse identities.
- Successfully handles full 360° head reconstruction (ear-to-ear).

## Limitations
- Higher model complexity than ImFace; slower training and inference.
- Still requires marching cubes for mesh extraction.
- Limited to face region; does not handle hair, ears, or neck in the deformation model.

## Connections
- [[papers/zheng-2022-imface]] — direct predecessor; ImFace++ is the journal extension
- [[papers/li-2017-flame]] — FLAME is the baseline being outperformed
- [[papers/ranjan-2018-coma]] — CoMA represents a different (mesh-based) approach to the same problem
- [[concepts/digital-human-appearance]] — high-fidelity face geometry for digital human pipelines
- [[concepts/blendshapes]] — expression latent codes replace explicit blendshape weights
