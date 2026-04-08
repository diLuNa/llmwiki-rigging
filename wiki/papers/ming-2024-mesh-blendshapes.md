---
title: "High-Quality Mesh Blendshape Generation from Face Videos via Neural Inverse Rendering"
authors: [Ming, Xin; Li, Jiawei; Ling, Jingwang; Zhang, Libo; Xu, Feng]
venue: ECCV 2024
year: 2024
tags: [neural, blendshapes, rig-generation, facial-capture, digital-human]
source: raw/papers/2401.08398.pdf
---

## Summary
Reconstructs a FACS-compatible mesh-based blendshape rig from single or sparse multi-view consumer video using neural inverse rendering. Differential coordinates with tetrahedral connections enable high-quality vertex deformation; semantic regulations jointly optimize blendshape bases and per-frame expression coefficients. Output blendshapes are geometrically and semantically accurate and directly importable into production animation pipelines (Maya, Houdini) — a practical alternative to studio scan-based rig creation.

## Problem
Creating high-quality personalized blendshape rigs currently requires expensive multi-view scan capture, manual shape sculpting, and rigging expertise. Existing video-based face reconstruction methods produce FLAME parameters or low-detail meshes, not editable production-ready blendshape rigs. A method that reconstructs artist-grade FACS-compatible delta meshes from consumer video would democratize character rigging.

## Method
**Parameterization:** Face geometry is represented with differential coordinates (edge vectors and face normals in a local frame) in a tetrahedral mesh embedding — more expressive than direct vertex positions for encoding complex surface deformations while preserving local rigidity.

**Blendshape optimization:**
- Neutral mesh $M_0$ and blendshape bases $\{\Delta_i\}$ are jointly optimized alongside per-frame expression coefficients $\alpha^t$.
- Semantic regulation: a prior forces each blendshape to correspond to a specific FACS AU region, preventing bleedthrough between semantically unrelated shapes.
- Neural regressor: handles temporally unsynchronized multi-camera footage by predicting expression coefficients from appearance features.

**Inverse rendering:** Differentiable rasterizer renders the current mesh estimate; photometric + silhouette + landmark losses drive optimization.

## Key Results
- FACS-compatible, production-importable blendshapes from consumer video.
- Better geometric accuracy than FLAME-fitting-based alternatives.
- Handles single-view and sparse multi-view input.
- Code and data publicly available.

## Limitations
- Optimization-based — slow to run per-subject (not real-time).
- Quality degrades with insufficient input video coverage (occlusion, limited expression range in captured footage).
- Semantic regulation provides FACS alignment only loosely — finer FACS correspondence requires manual cleanup.

## Connections
- [[concepts/facial-blendshape-rigs]] — directly produces production-format blendshape rigs from video
- [[concepts/nonlinear-face-models]] — neural inverse rendering for rig generation
- [[concepts/rig-inversion]] — the optimization solves for both rig and expression weights simultaneously
- [[papers/qin-2023-nfr]] — NFR is also topology-agnostic auto-rigging; ECCV 2024 is more focused on production mesh format
- [[papers/ma-2025-riganyface]] — RigAnyFace is also automatic blendshape rig generation but from mesh, not video

## Implementation Notes
The tetrahedral differential coordinates are the key technical choice: they allow smooth, volume-preserving deformations similar to what a skilled rigger produces manually, which is why the output is directly importable into DCC tools without topology conversion. The semantic regulation term is essentially a spatial mask per FACS AU — similar in spirit to the influence region concept in blendshape rigs.
