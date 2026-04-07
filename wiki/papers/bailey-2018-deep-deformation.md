---
title: "Fast and Deep Deformation Approximations"
authors: [Bailey, Stephen W.; Otte, Dave; Dilorenzo, Paul; O'Brien, James F.]
venue: SIGGRAPH 2018
year: 2018
tags: [neural, deformation, skinning, rig-generation, blendshapes]
source: ~no local pdf~
---

## Summary
Approximates complex character deformation rigs using a compact neural network that maps rig control parameters (joint rotations, blendshape weights) to per-vertex displacements, enabling real-time playback of high-quality deformations on any platform.

## Problem
Production rigs with many corrective sculpts and procedural deformers are too slow for real-time applications (games, real-time previews, crowd systems). Existing linear approximations (PCA/blendshapes) can't capture nonlinear rig behavior such as muscle bulging and skin contact.

## Method
Trains a neural network $f: \mathbf{q} \to \Delta\mathbf{p}$ where $\mathbf{q}$ is the rig control vector and $\Delta\mathbf{p}$ is per-vertex displacement from a linear baseline (LBS). The residual formulation means the network only needs to learn nonlinear corrections — simpler to train and more accurate than learning the full displacement.

Key design choices:
- **Linear baseline**: use LBS as the base; network predicts residual.
- **Sparse connectivity**: network connections reflect bone influence regions to limit parameter count.
- **Training data**: densely sampled rig evaluations at random pose combinations.

## Key Results
- Real-time deformation matching production rig quality.
- Outperforms PCA/blendshape baselines on nonlinear effects.
- Compact enough for game-engine deployment.
- Cited by [[papers/radzihovsky-2020-facebaker]] as prior state of the art to beat.

## Limitations
- Per-character training required.
- Accuracy degrades at unusual pose combinations not in the training set.
- Residual approach still relies on LBS being a good baseline.

## Connections
- [[papers/radzihovsky-2020-facebaker]] — FaceBaker claims to outperform this for facial rigs
- [[concepts/blendshapes]] — linear baseline and baked output are blendshape-adjacent
- [[concepts/linear-blend-skinning]]
- James F. O'Brien (UC Berkeley) — senior author; no author page yet
