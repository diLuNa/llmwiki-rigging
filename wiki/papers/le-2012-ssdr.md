---
title: "Smooth Skinning Decomposition with Rigid Bones"
authors: [Le, Binh Huy; Deng, Zhigang]
venue: ACM Transactions on Graphics (SIGGRAPH Asia 2012)
year: 2012
tags: [skinning, lbs, rig-generation, weights, math]
source: ~no local PDF~
---

## Summary
SSDR (Smooth Skinning Decomposition with Rigid Bones) is an algorithm that automatically extracts an LBS rig — bone transformations and skinning weights — from an input mesh animation sequence. Given only vertex trajectories, SSDR recovers a compact set of rigid bone transformations and smooth skinning weights that best approximate the input motion. It enables rig recovery from scan sequences and approximation of complex simulated or captured deformations.

## Problem
Artists manually skinning a character to a skeleton is expensive. Simulation data, performance capture, and non-linear rigs produce vertex animations with no explicit bone structure. An automatic method to extract a compact, game-engine–compatible LBS approximation from any mesh animation sequence is needed.

## Method
SSDR minimizes the reconstruction error over an animation of $F$ frames:
```math
\min_{W, \{R_k^f, T_k^f\}} \sum_{f=1}^{F} \sum_{i=1}^{N}
\left\| v_i^f - \sum_{k=1}^{K} w_{ik}\bigl(R_k^f v_i^0 + T_k^f\bigr) \right\|^2
```
subject to: $w_{ik} \ge 0$, $\sum_k w_{ik} = 1$, $\|w_i\|_0 \le p$ (at most $p$ non-zero weights per vertex).

**Algorithm (alternating optimization):**
1. **Bone update**: given weights $W$, solve for rigid transforms $\{R_k^f, T_k^f\}$ per bone per frame via SVD (Procrustes on weighted vertex sets).
2. **Weight update**: given transforms, solve per-vertex QP: minimize reconstruction error subject to non-negativity, sum-to-one, and sparsity constraints. SSDR uses an NNLS solver with a greedy sparsity step.
3. **Bone initialization**: k-means clustering of per-vertex best-fit transforms to initialize bone set.
4. **Iterate** until convergence.

Sparsity ($p \le 4$) is enforced by iteratively removing the smallest weight and re-solving — analogous to the sparse NMF trick.

## Key Results
- Recovers meaningful, artist-intuitive bone transformations from cloth, muscle, and captured skin animations.
- Approximation error competitive with previous methods using far fewer bones.
- Weights are smooth across the mesh surface (inherit from NNLS solution structure).
- Applied to: LBS-approximation of FEM simulations, rig extraction from scanned sequences, game-engine baking of complex rigs.

## Limitations
- Purely data-driven: requires a representative pose sequence; generalizes poorly to unseen poses outside the training set.
- Bone count $K$ must be chosen manually; too few → high error, too many → over-fitting.
- Assumes rigid bones; cannot recover twist/stretch bones naturally.
- Runtime is $O(FNK)$ per iteration; slow for very dense meshes or long sequences.

## Connections
- [[papers/le-2019-direct-delta-mush]] — same first author; Direct Delta Mush is a later, closed-form alternative
- [[papers/jacobson-2011-bbw]] — BBW computes LBS weights from rest pose; SSDR learns them from motion
- [[papers/loper-2015-smpl]] — SMPL learns LBS weights from a scan database; same spirit as SSDR but statistical
- [[papers/bailey-2018-deep-deformation]] — neural alternative to SSDR: neural net approximates full rig
- [[concepts/linear-blend-skinning]] — SSDR produces an LBS rig
- [[concepts/bounded-biharmonic-weights]] — alternative weight computation method (geometry-based vs data-driven)
- [[authors/le-binh]] — first author

## Implementation Notes
SSDR is most useful in Houdini as a **rig baking** tool:
1. Feed a DOP/FEM simulation or complex Python rig as a mesh sequence.
2. Run SSDR (Python; use the `ssdr` pip package or reimplement the alternating opt).
3. Import extracted weights as point attributes `bbw_0..K-1`; bone xforms as per-frame matrices.
4. At runtime: use `bbw-lbs-apply.vex` with the extracted weights.

Key hyperparameter: sparsity $p$. For skin: $p=4$; for cloth: $p=2$ often sufficient.
