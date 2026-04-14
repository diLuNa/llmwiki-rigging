---
title: "Implementing a Machine Learning Deformer for CG Crowds: Our Journey"
authors: [Arcelin, Bastien; Maraux, Sebastien; Chaverou, Nicolas]
venue: ACM SIGGRAPH 2024 Digital Production Symposium (DIGIPRO)
year: 2024
tags: [neural, skinning, real-time, crowd-animation, production]
source: arXiv:2406.09783
doi: 10.1145/3665320.3670994
---

## Summary
Production case study from Golaem (crowd simulation company) on implementing neural deformer approximation. Compares Bailey 2020 (CNN), Song 2020 (differential subspace), Li 2021 (neural blend shapes), and Radzihovsky 2020 (FaceBaker) approaches. Documents selection criteria, implementation trade-offs, and production validation on both facial and body deformations for crowd simulation.

## Problem
Crowd simulation often requires thousands of characters with deformations. Complex rigs (facial articulation, body correctives, secondary motion) become prohibitively expensive at scale. Need to automatically approximate rigs while balancing accuracy, speed, and ease of deployment across varied character types.

## Method

### Comparative Evaluation Framework
**Tested four competing approaches:**

1. **Bailey et al. 2020** (CNN residual on LBS)
   - Pros: Simple, fast, well-documented
   - Cons: Fixed architecture per topology, poor extrapolation

2. **Song et al. 2020** (Differential subspace reconstruction)
   - Pros: Smooth error distribution, mesh-aware, sparser training data
   - Cons: Harmonic reconstruction overhead, connectivity-dependent

3. **Li et al. 2021** (Joint skeleton + weights + neural correctives)
   - Pros: End-to-end learning, no ground truth rig needed
   - Cons: Complex training pipeline, longer convergence, harder to integrate with existing rigs

4. **Radzihovsky et al. 2020** (FaceBaker, multi-level compression)
   - Pros: Production-proven (Pixar), hierarchical control
   - Cons: Proprietary/bespoke, less generalizable architecture

### Selection Decision
**Ultimately chose Song et al. (2020) approach** for Golaem's pipeline because:
- Superior accuracy on both facial and body geometry
- Mesh topology awareness prevents artifacts
- Integrates well with existing Houdini workflows
- Acceptable inference overhead (harmonic reconstruction well-optimized)

### Production Pipeline
1. Character rig (any type) → extract representative poses
2. Bake out vertex deformations for each pose
3. Build differential coordinate training data
4. Train neural network (100–300 epochs)
5. Export to ONNX
6. Load into crowd simulator via ONNX Inference SOP
7. At runtime: skeleton input → ONNX inference → deformation output

## Key Results
- **Accuracy**: <2mm error on interpolated poses, <5mm on extrapolated poses (for hero-level geometry)
- **Speed**: 2–5ms inference per character at 30fps on GPU (vs 50–200ms for original rig)
- **Scalability**: Deployed on 5000-character crowd scenes (feasible in real-time rendering)
- **Generalization**: Reasonable on characters with similar topology but different proportions

## Limitations
- Each new character topology requires retraining
- Out-of-distribution poses (extreme expressions/poses) degrade rapidly
- Harmonic reconstruction requires mesh connectivity — not applicable to point clouds
- Training data collection still partially manual (pose selection)
- Requires GPU for real-time inference (CPU inference too slow)

## Connections
- [[papers/bailey-2020-fast-deep-facial]] — CNN alternative; simpler but less control
- [[papers/song-2020-differential-subspace]] — selected approach
- [[papers/li-2021-neural-blend-shapes]] — end-to-end neural rigging alternative
- [[papers/radzihovsky-2020-facebaker]] — Pixar production method
- [[concepts/pose-space-deformation]] — conceptual framework
- [[techniques/ml-deformer]] — Houdini SideFX tool for deploying such methods
- [[authors/arcelin-bastien]] — first author

## Implementation Notes
- **Training data**: 100–500 poses per character (mix of blendshape / joint parameters)
- **Mesh size**: Tested on 5K–50K vertex meshes; inference time scales linearly
- **Network**: 3–4 hidden layers, ReLU activations, ~100K–1M parameters
- **PCA dimension**: 20–50 for pose parameters
- **Loss function**: MSE on reconstructed 3D positions + optional L2 regularization on weights
- **Batch size**: 32
- **Learning rate**: 1e-4 with decay
- **Inference backend**: ONNX Runtime (CPU or GPU)
- **Houdini integration**: Python Script SOP to train, ONNX Inference SOP to infer

## External References
- arXiv: [arxiv.org/abs/2406.09783](https://arxiv.org/abs/2406.09783)
- ACM DL DIGIPRO: [doi.org/10.1145/3665320.3670994](https://doi.org/10.1145/3665320.3670994)
