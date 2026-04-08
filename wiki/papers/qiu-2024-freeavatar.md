---
title: "FreeAvatar: Robust 3D Facial Animation Transfer by Learning an Expression Foundation Model"
authors: [Qiu, Feng; Zhang, Wei; Liu, Chen; An, Rudong; Li, Lincheng; Ding, Yu; Fan, Changjie; Hu, Zhipeng; Yu, Xin]
venue: SIGGRAPH Asia 2024
year: 2024
tags: [neural, digital-human, blendshapes, facial-capture, rig-generation]
source: raw/papers/2409.13180.pdf
---

## Summary
FreeAvatar learns a topology-agnostic expression foundation model via reconstruction + contrastive expression similarity training on unlabeled facial images, then uses it to drive diverse 3D avatars without geometric landmark constraints. An Expression-driven Multi-avatar Animator decodes expression semantics to avatar control parameters, trained across multiple topologies via dynamic identity injection. Outperforms landmark-constrained retargeting baselines for subtle and complex emotions.

## Problem
Most facial animation transfer methods rely on geometric landmarks or FLAME parameters as intermediate representation — both are sparse (only ~68 landmarks) and topology-specific. This causes landmark-constrained methods to fail on complex or subtle expressions where landmark motion is ambiguous. A richer, topology-agnostic expression representation would enable more faithful transfer across arbitrary avatar pairs.

## Method
**Expression foundation model:**
- Trains a facial encoder via reconstruction (predicts expression embedding from image) and contrastive objectives (similar expressions have similar embeddings, different expressions are separated).
- Trained on unlabeled images + a re-collected expression comparison dataset.
- Output: a dense expression feature vector $\mathbf{e}$ capturing semantic expression independently of identity and topology.

**Expression-driven Multi-avatar Animator (EMA):**
- Maps $\mathbf{e}$ → avatar control parameters (blendshape weights, joint angles, etc.) for a target avatar.
- Dynamic identity injection: a single network handles multiple avatar topologies by conditioning on an identity embedding — enabling joint training across diverse avatar types.
- Neural renderer ensures differentiable supervision via perceptual consistency losses.

## Key Results
- Better expression fidelity on subtle/complex expressions vs landmark-constrained baselines.
- Single model drives multiple avatar topologies simultaneously.
- Animates from video without explicit 3D reconstruction or rig inversion.

## Limitations
- Expression foundation model trained on 2D images — depth/3D expression ambiguity may affect quality for non-frontal input.
- EMA requires per-avatar-topology training data; generalization to truly novel avatar formats is limited.

## Connections
- [[concepts/nonlinear-face-models]] — expression foundation model as a topology-agnostic expression space
- [[concepts/facial-blendshape-rigs]] — blendshape weights are the output control parameters
- [[concepts/rig-inversion]] — EMA is a form of rig inversion from expression features to avatar controls
- [[papers/sol-2025-blendshape-retargeting]] — similar retargeting goal via VAE latent space
- [[papers/danecek-2022-emoca]] — EMOCA provides expression-aware features as alternative intermediate
