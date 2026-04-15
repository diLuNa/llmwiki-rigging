---
title: "High-fidelity Interpretable Inverse Rig: An Accurate and Sparse Solution Optimizing the Quartic Blendshape Model"
authors: [Rackovic, Stevo; Soares, Claudia; Jakovetic, Dusan; Desnica, Zoranka]
venue: arXiv 2023
year: 2023
tags: [blendshapes, facial-animation, correctives, pose-space, math]
source: https://arxiv.org/abs/2302.04820
---

## Summary
Formulates blendshape rig inversion as regularized least-squares over a quartic blendshape model (up to fourth-order corrective interactions) and solves it via coordinate descent. The key contribution is enforcing mutual exclusivity constraints — controllers that should not fire simultaneously are prevented from doing so by the update ordering — yielding weight vectors that are >20% sparser than state-of-the-art while maintaining comparable or better mesh reconstruction accuracy.

## Problem
Standard blendshape inversion fits a linear (or pairwise) model by minimizing mesh error. For production rigs with quartic (4-way corrective) interactions, the solution space is high-dimensional and naively optimized weight vectors often activate many blendshapes simultaneously, including mutually exclusive ones (e.g., jaw open + jaw closed). This makes the result harder for artists to adjust in post-production.

## Method

### Blendshape Model
The quartic blendshape model expresses a mesh vertex $\mathbf{v}$ as:

```
v(w) = v₀ + Σᵢ wᵢ bᵢ                          (linear)
           + Σᵢ<j wᵢwⱼ bᵢⱼ                       (pairwise correctives)
           + Σᵢ<j<k wᵢwⱼwₖ bᵢⱼₖ                  (triple correctives)
           + Σᵢ<j<k<l wᵢwⱼwₖwₗ bᵢⱼₖₗ             (quartic correctives)
```

where $w \in [0,1]^n$ are blendshape weights. The quartic terms make the mesh a polynomial in $w$ of degree 4.

### Objective
Minimize the regularized fitting error:

```
minimize  ‖M(w) - M_target‖²_F + λ‖w‖₁
subject to  0 ≤ w ≤ 1
```

The L1 penalty promotes sparsity. An additional mutual-exclusivity constraint prevents simultaneous activation of conflicting controllers.

### Coordinate Descent
The objective is decomposed into per-controller scalar problems. Each $w_i$ is updated in isolation (all others fixed), which reduces to a constrained 1D problem with a closed-form solution. The update order is determined by the magnitude of each controller's deformation influence — larger-effect controllers are updated first, consistent with animator intuition and ensuring that dominant shapes are set before fine correctives.

This implicit ordering naturally suppresses activation of mutually exclusive controllers: once a dominant shape (e.g., jaw open) is given a weight, the residual error for its complement (jaw closed) is already small, and L1 regularization pushes that weight to zero.

## Key Results
- >20% reduction in weight vector cardinality (fewer active blendshapes per frame) compared to state-of-the-art
- Mesh error comparable to or lower than competing methods
- Weight vectors easier for artists to interpret and manually adjust in post-production
- Convergence guaranteed: coordinate descent on the (bounded) quartic objective decreases cost monotonically

## Limitations
- Coordinate descent convergence is slow for densely coupled corrective models (many shared vertices)
- Quartic corrective enumeration is memory-intensive for large blendshape sets
- Mutual-exclusivity is handled implicitly via ordering rather than explicit constraint — may not be sufficient for all rig designs
- No temporal smoothness: frame-by-frame solving can produce weight discontinuities (addressed in [[papers/an-2024-refined-inverse-rigging]])

## Connections
- [[papers/an-2024-refined-inverse-rigging]] — extended follow-up by same group; adds temporal smoothness across full sequences
- [[papers/rackovic-2023-distributed-rig-inversion]] — concurrent companion; ADMM distributed approach for scalability
- [[papers/rackovic-2023-accurate-interpretable-inverse-rig]] — companion paper; quadratic corrective terms with SQP and MM solvers
- [[concepts/blendshapes]] — blendshape fundamentals
- [[concepts/rig-inversion]] — problem context
- [[authors/rackovic-stevo]]

## Implementation Notes
- Coordinate descent per-controller update for a quartic blendshape is a bounded polynomial minimization; exact 1D solution exists when coupling terms are included
- L1 regularization with coordinate descent: the proximal update is soft-thresholding, clipped to [0,1]
- For Houdini: the quartic model can be stored as attribute arrays on the geometry; coordinate descent updates iterate over blendshape prim attributes

## Quotes
> "Our method yields solutions with mesh error comparable to or lower than state-of-the-art approaches while significantly reducing the cardinality of the weight vector (over 20 percent)." (Abstract)
