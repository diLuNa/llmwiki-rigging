---
title: "Accurate and Interpretable Solution of the Inverse Rig for Realistic Blendshape Models with Quadratic Corrective Terms"
authors: [Rackovic, Stevo; Soares, Claudia; Jakovetic, Dusan; Desnica, Zoranka]
venue: arXiv 2023 (cs.GR)
year: 2023
tags: [blendshapes, facial-animation, correctives, pose-space, math]
source: https://arxiv.org/abs/2302.04843
---

## Summary
Proposes two solvers for blendshape rig inversion under a quadratic corrective model: an SQP (Sequential Quadratic Programming) solver that maximizes accuracy at the cost of weight interpretability, and an MM (Majorization-Minimization) algorithm that trades a small amount of accuracy for significantly sparser, smoother, more artist-friendly weights. Up to 45% RMSE improvement over prior state-of-the-art in mesh reconstruction.

## Problem
Production facial rigs include quadratic (pairwise) corrective blendshapes that capture non-linear deformations at joint extremes (e.g., cheek bulge when mouth opens). Ignoring these terms introduces systematic residuals in the inverse rig solution. Incorporating them makes the objective non-convex and harder to solve while still maintaining weight sparsity and interpretability required for post-production artist adjustment.

## Method

### Blendshape Model with Quadratic Correctives
The mesh at frame $t$ is:

```
v(w) = v₀ + B w + C(w ⊗ w)
```

where $B \in \mathbb{R}^{3n \times p}$ is the linear blendshape basis, $C$ contains pairwise corrective blend shapes, and $w \in [0,1]^p$. The quadratic $C$ term makes the objective quartic in $w$ (since error is quadratic in $v$).

### Solver 1: SQP
Sequential Quadratic Programming solves the constrained nonlinear program directly:

```
minimize  ‖v(w) - v_target‖²
subject to  0 ≤ w ≤ 1
```

At each SQP iteration, a local quadratic approximation is formed and the resulting QP is solved. The SQP solver achieves the lowest possible mesh error but yields dense, sometimes difficult-to-interpret weight vectors.

### Solver 2: MM (Majorization-Minimization)
The non-convex quartic objective is upper-bounded at each iteration by a simpler (quadratic or linear) majorizing function. Minimizing the majorizer gives the next iterate. The MM formulation is designed so that the majorizer is a convex QP with bound constraints, and adding an L1 regularization term promotes sparsity:

```
minimize  ‖A(wᵏ) w - r(wᵏ)‖² + λ‖w‖₁
subject to  0 ≤ w ≤ 1
```

where $A(wᵏ)$ and $r(wᵏ)$ linearize the corrective interaction at the current estimate $wᵏ$.

The MM updates are ordered by controller influence magnitude — larger-effect controllers are updated first. This implicit ordering naturally suppresses mutually exclusive controllers (same insight as [[papers/rackovic-2023-highfidelity-inverse-rig]]).

## Key Results
- **SQP**: up to 45% relative RMSE improvement vs. state-of-the-art (highest accuracy, densest weights)
- **MM**: comparable sparsity to benchmarks with better mesh accuracy than linear-only inversion; smooth animation trajectories validated by human experts
- Comprehensive evaluation on 4 metrics: mesh RMSE, weight cardinality, animation smoothness, visual appearance ratings

## Limitations
- SQP produces dense, hard-to-edit weight vectors — trades interpretability for accuracy
- MM convergence speed depends on the quality of the linearization; for highly nonlinear rigs, more iterations are required
- Both methods are frame-independent (no temporal coupling); weight discontinuities can occur between frames (addressed in [[papers/an-2024-refined-inverse-rigging]])
- Targets facial rigs specifically — applicability to body rigs with different corrective structures is not evaluated

## Connections
- [[papers/rackovic-2023-highfidelity-inverse-rig]] — companion paper; quartic model, coordinate descent, mutual-exclusivity focus
- [[papers/rackovic-2023-distributed-rig-inversion]] — companion paper; ADMM distributed solving for scalability
- [[papers/an-2024-refined-inverse-rigging]] — follow-up: adds temporal smoothness and sequence-level optimization
- [[concepts/blendshapes]] — blendshape fundamentals
- [[concepts/correctives]] — the corrective blendshape terms being modeled
- [[concepts/rig-inversion]] — problem context
- [[authors/rackovic-stevo]]

## Implementation Notes
- The MM update step is a standard bounded LASSO problem (L2 data term + L1 regularizer + box constraints); solvable via coordinate descent, ADMM, or active-set methods
- SQP implementation can use scipy.optimize.minimize with 'SLSQP' method in Python
- The linearization $A(wᵏ)$ at each MM step captures only first-order interaction effects; second-order interactions are absorbed into the residual $r(wᵏ)$

## Quotes
> "The MM algorithm produces weight vectors that are more interpretable and easier for artists to manipulate." (Paraphrase from abstract)
> "Up to 45% relative improvement in root mean squared error versus state-of-the-art" (Abstract)
