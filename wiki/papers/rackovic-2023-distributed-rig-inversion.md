---
title: "Distributed Solution of the Blendshape Rig Inversion Problem"
authors: [Rackovic, Stevo; Soares, Claudia; Jakovetic, Dusan]
venue: SIGGRAPH Asia 2023 Technical Communications
year: 2023
tags: [blendshapes, facial-animation, correctives, pose-space, math]
source: raw/papers/3610543.3626166.pdf
doi: 10.1145/3610543.3626166
---

## Summary
Proposes a spatially-clustered, distributed method for blendshape rig inversion using the Alternating Direction Method of Multipliers (ADMM). As blendshape models grow to hundreds of corrective shapes, naive inversion becomes impractically slow; this work decomposes the face into overlapping clusters and coordinates their solutions, recovering accuracy that naive clustering sacrifices without the full cost of global solving.

## Problem
Modern production blendshape models for faces include 80+ base shapes and 400+ corrective (pairwise/triple) terms. Full global optimization of all weights simultaneously scales poorly — both in memory and runtime — as model complexity grows. Naive spatial decomposition (solve each cluster independently) introduces boundary artifacts at cluster edges where neighboring regions share blendshape influences.

## Method

### Spatial Clustering
The face mesh is partitioned into $K$ overlapping clusters. Each cluster contains a subset of vertices and the blendshape controllers that primarily influence those vertices. Overlap is deliberate: boundary vertices and shared controllers appear in multiple clusters.

### ADMM Formulation
The global inverse rig problem (fit blendshape weights to minimize mesh error with regularization) is reformulated as a consensus problem:

```
minimize   sum_k f_k(w_k)   [local cluster objectives]
subject to  w_k = z          [global consensus on shared weights]
```

ADMM alternates between:
1. **Local updates**: each cluster independently minimizes its local objective (fast, parallelizable)
2. **Global consensus step**: averages cluster estimates of shared weights
3. **Dual variable update**: Lagrange multipliers enforce consistency between cluster solutions

The shared-weight mechanism — sharing overlapping weight estimates between adjacent clusters — is what distinguishes this from naive clustering and recovers accuracy at cluster boundaries.

### Cluster Count Selection
A data-free method is introduced to determine the optimal number of clusters $K$ based on a trade-off between reconstruction error and density of cluster membership, without requiring ground-truth annotations.

## Key Results
- Clear accuracy advantage over naive spatial clustering on multiple metrics (mesh RMSE, visual quality)
- Parallelizable across clusters → practical speedup vs. full global solve for large models
- Data-free cluster count selection removes a key tuning hyperparameter

## Limitations
- Inter-cluster coupling introduces additional iterations (ADMM convergence is sublinear); full convergence requires more rounds than a single global solve
- Cluster boundary accuracy depends on overlap width — narrow overlaps reintroduce artifacts
- Quantitative comparison against the concurrent Rackovic et al. 2023 quartic methods is not included in this shorter technical communication format
- No public code at publication time

## Connections
- [[papers/rackovic-2023-highfidelity-inverse-rig]] — concurrent paper by same authors; coordinate descent on quartic blendshape model
- [[papers/rackovic-2023-accurate-interpretable-inverse-rig]] — companion paper; SQP and MM algorithms for quadratic correctives
- [[papers/an-2024-refined-inverse-rigging]] — follow-up: full SIGGRAPH Asia 2024 paper; adds temporal smoothness, L1 sparsity, sequence-level optimization
- [[concepts/blendshapes]] — the blendshape model being inverted
- [[concepts/rig-inversion]] — the general problem

## Implementation Notes
- ADMM is well-suited to GPU parallelization: each cluster local update is an independent constrained quadratic program (QP), solvable via a simple projected gradient or active-set method
- The consensus step is a weighted average — trivially parallelizable
- Overlap width is a hyperparameter: typically 1–2 mesh rings around cluster boundaries
- For Houdini: cluster decomposition could be driven by face rig influence maps (which controls affect which vertices)

## Quotes
> "The proposed algorithm applies the Alternating Direction Method of Multipliers, sharing the overlapping weights between the subproblems." (Abstract)
