---
title: "Robust and Accurate Skeletal Rigging from Mesh Sequences"
authors: [Le, Binh Huy; Deng, Zhigang]
venue: ACM Transactions on Graphics (SIGGRAPH 2014)
year: 2014
tags: [skinning, lbs, rig-generation, weights, math, auto-rigging]
source: ~no local PDF~
doi: 10.1145/2601097.2601161
---

## Summary
Extends SSDR to automatically generate a **complete skeletal rig** — joints, positions, bone hierarchy, and skinning weights — directly from example mesh poses, with no user-provided skeleton. Incorporates joint constraints and weight smoothness regularization into the alternating optimization, and automatically prunes redundant bones. Produces rigs suitable for direct use in animation software and game engines.

## Problem
SSDR recovers bone transforms and weights but requires a bone count to be specified and gives no joint positions — just rigid transforms per frame. For full rig extraction (e.g., from a scan sequence), you also need the skeleton topology, joint locations, and a rest-pose hierarchy. Prior methods are either error-prone or require symmetric input.

## Method

### SSDR Foundation
Inherits the SSDR objective (minimize per-vertex LBS reconstruction error over all frames) from [[papers/le-2012-ssdr]]:
```math
\min_{W, \{R_k^f, T_k^f\}} \sum_{f,i} \left\| v_i^f - \sum_k w_{ik}(R_k^f v_i^0 + T_k^f) \right\|^2
```
with non-negativity, partition-of-unity, and sparsity constraints on $W$.

### Extensions for Skeletal Rigging

**Joint position estimation:** Each bone transform $\{R_k^f, T_k^f\}$ is parameterized around a joint position $j_k$ in rest pose. The per-frame bone rotation $R_k^f$ is estimated around $j_k$, and the translation $T_k^f$ is derived from it. Joint positions are solved jointly with rotations via least-squares.

**Joint constraints:** Pairs of adjacent bones share a joint — this imposes a constraint that the relative motion between them corresponds to a rotation about their shared joint. The optimization alternates:
1. **Weight update**: given joint positions + transforms, update $W$ (NNLS + sparsity).
2. **Transform update**: given $W$, update per-frame $\{R_k^f\}$ per bone (SVD on weighted point sets around $j_k$).
3. **Joint update**: given $W$ + $\{R_k^f\}$, update joint positions $j_k$ (closed-form least-squares).

**Bone pruning:** Start with an over-complete set (e.g., $K = 2 \times \text{target}$ bones). After convergence, remove bones whose influence weight across all vertices falls below a threshold. Re-run until bone count stabilizes.

**Weight smoothness regularization:** Adds a Laplacian smoothness term $\lambda \sum_{i,j \in \text{edges}} \|w_i - w_j\|^2$ to the weight objective, producing spatially coherent weight maps that generalize better.

### Result
Produces a complete rig: rest-pose joint positions, per-frame bone rotations (interpretable as joint angles), and smooth sparse skinning weights — all from example poses alone. No symmetry assumption; handles quadrupeds, humans, highly deformable and facial models.

## Key Results
- 28-bone cat skeleton from 9 example poses (SSDR alone gives transforms only, no topology)
- Handles diverse model types: humans, quadrupeds, highly deformable clothing, facial shapes
- Outperforms prior skeleton extraction methods (Pinocchio, SSD-based) in reconstruction error
- Weights generalize to unseen poses better than pure SSDR due to smoothness regularization
- Runtime: minutes for typical character (100 frames, 10K vertices, 20 bones)

## Limitations
- Still requires user to specify approximate bone count $K$ (or over-specify and prune)
- Joint hierarchy (parent-child topology) is inferred heuristically — may need manual correction for complex branching structures (hands, fingers)
- Assumes rigid bones; cannot model stretch/twist along a bone
- Like SSDR, generalizes only within the span of training poses

## Connections
- [[papers/le-2012-ssdr]] — direct predecessor; this paper adds joint positions, smoothness, and pruning
- [[papers/le-2016-cor-skinning]] — same first author; CoR skinning improves runtime quality of LBS
- [[papers/le-2019-direct-delta-mush]] — same first author; later closed-form deformation analysis
- [[papers/xu-2020-rignet]] — neural approach to same problem (skeleton + weights from geometry)
- [[concepts/linear-blend-skinning]] — output format
- [[concepts/auto-rigging]] — this is the key automation paper for data-driven rig extraction
- [[authors/le-binh]] — first author

## Implementation Notes
- The EA **Dem Bones** library implements both SSDR and the skeletal rigging extension; see [[techniques/dem-bones]]
- Houdini's **Dem Bones Skinning Converter SOP** (Labs) wraps the EA library directly
- Joint pruning threshold: typically $\sum_i w_{ik} < \epsilon \cdot N$ where $\epsilon \approx 0.01$
- For production use: run with over-estimated $K$ (e.g., 1.5–2× target), let pruning reduce it naturally
- Smoothness $\lambda \in [0.01, 0.1]$ — higher values give more uniform weights at cost of accuracy

## External References
- Project page: [binh.graphics/papers/2014s-ske](https://binh.graphics/papers/2014s-ske/)
- ACM DL: [doi.org/10.1145/2601097.2601161](https://doi.org/10.1145/2601097.2601161)
