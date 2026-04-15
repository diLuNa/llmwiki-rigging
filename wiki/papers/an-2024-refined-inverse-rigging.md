---
title: "Refined Inverse Rigging: A Balanced Approach to High-fidelity Blendshape Animation"
authors: [Rackovic, Stevo; Soares, Claudia; Jakovetic, Dusan]
venue: SIGGRAPH Asia 2024 Conference Papers
year: 2024
tags: [blendshapes, facial-animation, correctives, pose-space, math]
source: raw/papers/3680528.3687670.pdf
doi: 10.1145/3680528.3687670
---

## Summary
"Quartic Smooth" — a blendshape rig inversion method that jointly optimizes mesh fidelity, weight sparsity, and temporal smoothness across an entire animation sequence. Key innovation: temporal decoupling of blendshape controllers allows frame-wise parallelism while still enforcing cross-frame roughness penalties. Evaluated on MetaHuman Jesse (80 base + 400+ corrective blendshapes), achieves the best smoothness in the benchmark while maintaining competitive accuracy and 2.16s per-sequence solve time.

## Problem
Prior blendshape inversion methods (including the authors' earlier work in [[papers/rackovic-2023-highfidelity-inverse-rig]] and [[papers/rackovic-2023-accurate-interpretable-inverse-rig]]) solve frames independently. This produces weight discontinuities — jitter — that is visually unacceptable in animated sequences, especially in close-up facial shots. Simultaneously enforcing accuracy, sparsity, and smoothness within a tractable formulation is the core challenge.

## Method

### Joint Objective
Optimization is formulated over the entire animation sequence of $T$ frames simultaneously:

```math
\min_W \; E_\text{df}(W) + \alpha \cdot E_\text{sr}(W) + \beta \cdot E_\text{tsr}(W)
\quad \text{s.t.} \; 0 \leq W \leq 1
```

where $W \in [0,1]^{p \times T}$ is the matrix of blendshape weights across all frames.

**Data fidelity** $E_\text{df}$: Frobenius norm between estimated and target mesh sequences:
```
E_df = ‖M(W) - M_target‖²_F
```

**Sparsity regularization** $E_\text{sr}$: L1 norm promoting few active blendshapes per frame:
```
E_sr = (1/pT) ‖W‖₁
```

**Temporal smoothness** $E_\text{tsr}$: roughness penalty via second differences across consecutive frames:
```
E_tsr = ‖F W‖²_F
```
where $F$ is a pentadiagonal finite-difference matrix that computes $w_t - 2w_{t-1} + w_{t-2}$ (second discrete derivative). This penalizes abrupt weight changes more heavily than first-difference approaches.

### Blendshape Model
Supports the full quartic hierarchy (linear, pairwise, triple, quartic correctives), same model as [[papers/rackovic-2023-highfidelity-inverse-rig]].

### Coordinate Descent with Temporal Decoupling
The joint objective is decomposed per-controller (column-wise in $W$). Each controller's weight trajectory $\{w_{i,t}\}_t$ is updated independently with others fixed, yielding a temporally-coupled but controller-decoupled subproblem. Temporal decoupling means: the cross-frame coupling within one controller is handled in its scalar trajectory optimization, while controller interactions are resolved across coordinate descent passes.

Update order: controllers sorted by total deformation magnitude across the sequence.

### Clustering for Parallelism
Optional spatial clustering (RSJD and RSJD_A variants from [[papers/rackovic-2023-distributed-rig-inversion]]) decomposes the face into $K$ clusters. Cluster counts $K=29$ (RSJD) and $K=13$ (RSJD_A) were determined data-free. Clustering trades mesh accuracy for speed and parallelism.

## Key Results
Evaluated on MetaHuman Jesse, 80 training / 100 test frames:

| Method | Max Error | Mean Error | Cardinality | Roughness | Time (s) |
|--------|-----------|------------|-------------|-----------|----------|
| **Quartic Smooth** (this paper) | 0.101 | 0.019 | 56.3 | **7.2e-5** | 2.16 |
| Linear Smooth | 0.257 | 0.051 | 68.6 | 4.2e-4 | 0.02 |
| Quartic (no smoothing) | 0.086 | **0.016** | 49.7 | 1.1e-3 | 14.4 |

Quartic Smooth achieves the **lowest roughness penalty** (14× smoother than Quartic, 6× smoother than Linear Smooth) while keeping mean error within 19% of the best-accuracy Quartic-only variant, at 6× lower cost.

## Limitations
- Clustering (RSJD variants) introduces higher mesh errors at cluster boundaries — accuracy-speed tradeoff
- Hyperparameters $\alpha$, $\beta$ require cross-validation per character
- Evaluated on a single MetaHuman character; generalization to other rig topologies not demonstrated
- Temporal decoupling does not guarantee global optimality over the sequence
- No public code released at time of publication

## Connections
- [[papers/rackovic-2023-highfidelity-inverse-rig]] — prior work by same authors; quartic model, coordinate descent, sparsity focus
- [[papers/rackovic-2023-accurate-interpretable-inverse-rig]] — prior work; SQP and MM algorithms with quadratic correctives
- [[papers/rackovic-2023-distributed-rig-inversion]] — prior work; ADMM clustering approach reused here
- [[papers/holden-2015-inverse-rig]] — foundational neural inverse rig mapping
- [[concepts/blendshapes]] — blendshape fundamentals
- [[concepts/correctives]] — corrective blendshapes being modeled
- [[concepts/rig-inversion]] — problem context
- [[authors/rackovic-stevo]]

## Implementation Notes
- The roughness penalty matrix $F$ is pentadiagonal and sparse; $F^T F$ can be precomputed as a banded matrix and applied efficiently per-controller trajectory
- Second-difference penalty is preferable to first-difference because it controls acceleration (not just velocity), suppressing high-frequency oscillations better
- Coordinate descent on the scalar trajectory subproblem per controller reduces to a 1D bounded convex QP with a banded structure — solvable in $O(T)$ via the Thomas algorithm
- For Python: `scipy.sparse.diags` can construct $F$; `scipy.optimize.minimize(method='L-BFGS-B')` handles per-trajectory optimization
- Integration with ARKit (52 weights) or MetaHuman (80 base + 400+ correctives): the quartic model naturally extends to production-scale rig definitions

## Quotes
> "Quartic Smooth achieves superior smoothness (lowest roughness penalty) with balanced accuracy and computational efficiency compared to benchmarks that either lack smoothness regularization or ignore temporal coherence." (Results section)
