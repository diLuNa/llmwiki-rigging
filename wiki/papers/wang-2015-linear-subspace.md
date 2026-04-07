---
title: "Linear Subspace Design for Real-Time Shape Deformation"
authors: [Wang, Yu; Shi, Alec; Pons-Moll, Gerard; Ye, Youyi; Tong, Xin]
venue: ACM Transactions on Graphics (SIGGRAPH 2015)
year: 2015
tags: [deformation, skinning, rig-generation, math, neural]
source: ~no local PDF~
---

## Summary
Proposes a framework for automatically computing a compact linear subspace basis that best approximates the deformation space of a given rig or simulation. The basis is optimized jointly for reconstruction accuracy and real-time performance constraints (fixed vertex count, limited bases). Bridges the gap between full-DOF production rigs and real-time LBS approximations.

## Problem
Production rigs and physics simulations produce rich nonlinear deformations that don't compress well into simple LBS or small blendshape sets. PCA on pose samples gives a global basis that is dense (every basis vector affects every vertex), making real-time evaluation expensive and making it difficult to apply localized artist edits. A spatially localized, optimized linear basis is needed.

## Method
Given a set of sample deformations $\{d^s\}_{s=1}^{S}$ (vertex displacements from rest pose), the goal is to find $K$ basis vectors $\{b_k\} \subset \mathbb{R}^{3N}$ and per-sample weights $\{c^s\} \subset \mathbb{R}^K$ minimizing:
```math
\min_{\{b_k\},\{c^s\}} \sum_s \left\| d^s - \sum_k c^s_k b_k \right\|^2 + \lambda \sum_k \|b_k\|_{\text{spatial}}
```
**Key contributions over plain PCA:**
- **Spatial locality**: each basis $b_k$ is constrained to be spatially compact (non-zero over a local mesh region) via an $\ell_1$ regularizer or support constraint.
- **Joint weight/basis optimization**: alternating between solving for coefficients $c^s$ (regression) and basis $b_k$ (sparse recovery), similar to Dictionary Learning / K-SVD.
- **Real-time structure**: the resulting $K$ localized bases map to $K$ scalar parameters per frame; basis evaluation is a dense BLAS operation but with compact support.

**Applications demonstrated:**
- Approximating complex cage deformations with a small basis.
- Reducing a 300-blendshape rig to 30 localized components with similar fidelity.
- Real-time subspace simulation (precompute reduced stiffness matrices in the learned basis).

## Key Results
- Localized bases are more interpretable than global PCA and more compatible with artist workflows.
- Reconstruction error comparable to PCA at the same $K$, better at smaller $K$ for localized effects.
- Real-time evaluation on GPU demonstrated for 10k-vertex meshes.

## Limitations
- Requires a representative sample set; rare pose combinations may not be approximated well.
- Basis count $K$ is a hyperparameter; underfitting (too few bases) causes visible artifacts.
- Spatial locality constraint complicates the optimization (non-convex alternating scheme).

## Connections
- [[papers/bailey-2018-deep-deformation]] — neural alternative: nonlinear approximation of the same deformation space
- [[papers/le-2012-ssdr]] — SSDR also learns a compact LBS basis from examples, but from motion sequences
- [[papers/loper-2015-smpl]] — SMPL's shape + pose PCA components are a learned linear subspace of similar flavor
- [[papers/bouaziz-2014-projective-dynamics]] — subspace simulation in the learned basis reduces real-time FEM cost
- [[concepts/blendshapes]] — result is effectively a learned localized blendshape palette
- [[concepts/linear-blend-skinning]] — the compact evaluation model at runtime is equivalent to LBS

## Implementation Notes
The framework is implemented in Python (scipy sparse + alternating NNLS). In Houdini:
- **Precompute**: sample rig deformations at random poses → stack into matrix $D \in \mathbb{R}^{3N \times S}$.
- **Learn basis**: run K-SVD or sparse PCA to get $B \in \mathbb{R}^{3N \times K}$.
- **Export**: store each column of $B$ as a blendshape delta on the mesh.
- **Runtime**: K scalar parameters drive the K blendshapes — standard Houdini blendshape SOP workflow.
