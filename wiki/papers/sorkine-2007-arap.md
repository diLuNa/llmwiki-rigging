---
title: "As-Rigid-As-Possible Surface Modeling"
authors: [Sorkine, Olga; Alexa, Marc]
venue: Eurographics Symposium on Geometry Processing 2007
year: 2007
tags: [deformation, math, skinning]
source: ~no local pdf~
---

## Summary
Introduces ARAP (As-Rigid-As-Possible) surface deformation — a mesh editing method that minimizes local deviation from rigidity by alternating between local rigid fitting (per-cell SVD) and a global Poisson solve. Produces natural-looking, volume-preserving deformations under large positional constraints.

## Problem
Interactive mesh deformation under user-specified handle constraints should produce natural, shape-preserving results without requiring physics simulation. Laplacian-based methods (LAPLACIAN editing) preserve differential coordinates but not local rigidity, producing shearing under large deformations.

## Method
Minimizes:

```math
E(\mathbf{p}) = \sum_{i} \sum_{j \in \mathcal{N}(i)} w_{ij} \|\, (\mathbf{p}_i - \mathbf{p}_j) - R_i(\mathbf{p}_i^0 - \mathbf{p}_j^0) \|^2
```

where $R_i \in SO(3)$ is the best-fit rotation for cell $i$, $w_{ij}$ are cotangent weights. Solved via alternating optimization:
1. **Local step**: for each cell, find optimal $R_i$ via SVD of the covariance matrix.
2. **Global step**: fix rotations, solve a sparse linear system (Poisson equation) for new vertex positions.

The two steps alternate until convergence (typically 3–10 iterations for interactive use).

## Key Results
- Convincing large-deformation results with no physics simulation.
- Efficient: sparse linear system precomputed; only RHS changes per iteration.
- Widely adopted as a baseline for mesh deformation and as a post-processing step for simulation outputs.

## Limitations
- Volume not strictly preserved (though cell rigidity implies approximate preservation).
- Alternating optimization can converge to local minima under very large deformations.
- Performance degrades with mesh resolution; GPU/multigrid acceleration needed at scale.

## Connections
- [[concepts/laplacian-smoothing]] — ARAP extends Laplacian editing to preserve rigidity
- [[papers/degoes-2018-kelvinlets]] — Kelvinlets cited ARAP as a candidate post-processing step
- [[papers/degoes-2020-sculpt]] — sculpt relaxation is conceptually related (preserve rest-pose shape)
- [[authors/sorkine-olga]]

## Implementation Notes
The sparse system matrix (assembled from cotangent weights) is precomputed once at bind time. Only the RHS is recomputed each iteration, making real-time interaction feasible. In Houdini this can be implemented as a custom SOP iterating local SVD + global Poisson solve. Many open-source implementations exist (e.g., libigl).
