---
title: "Learning Inverse Rig Mappings by Nonlinear Regression"
authors: [Holden, Daniel; Saito, Jun; Komura, Taku]
venue: IEEE Transactions on Visualization and Computer Graphics (TVCG), vol. 23 no. 3
year: 2017
tags: [rig-generation, neural, pose-space, math]
source: raw/papers/rigfunction.pdf
---

## Summary
Extended journal version of Holden et al. SCA 2015. Adds Gaussian Process Regression (GPR) with active subsampling as a second inverse rig method alongside the neural network approach, and substantially expands evaluation. For rigs where enough training data can be collected, the MLP is faster; for small-data regimes, GPR generalizes better. Both map joint positions or surface geometry to high-level rig control parameters in real time.

## Problem
Same as [[papers/holden-2015-inverse-rig]]: animators work in rig parameter space; motion synthesis (IK, motion capture retargeting, motion editing) works in skeleton joint space. The gap between the two representations prevents direct application of state-of-the-art animation techniques to production-rigged characters.

Key challenge: the rig function $f: \mathbf{y} \to \mathbf{x}$ (rig params → skeleton) is nonlinear, high-dimensional, and often not analytically invertible. The journal version frames this more carefully than the conference version and adds a second solution path.

## Method

### Input Representation
Skeleton configuration $\mathbf{x} \in \mathbb{R}^{3j}$ is the vector of global joint positions relative to the character's center of gravity ($j$ joints). Local joint angles are also supported.

### Method 1: Neural Network Regression
A multilayer perceptron trained to approximate $f^{-1}: \mathbf{x} \to \mathbf{y}$. The network is trained on example animation sequences produced by artists. Super-sampling (augmenting training data by interpolating between poses in rig space) is introduced in this version to improve generalization, particularly in regions of rig space not well-covered by artist animations.

### Method 2: Gaussian Process Regression (new in journal version)
Models each dimension of the rig output independently as a Gaussian process over the skeleton input space, using an RBF kernel:

$$k(\mathbf{x}_i, \mathbf{x}_j) = \exp\left(-\frac{\|\mathbf{x}_i - \mathbf{x}_j\|^2}{2\ell^2}\right)$$

Prediction for a new input $\mathbf{x}^*$:
$$y_i^* = K_*\,(K + \theta_1 I)^{-1} Y_i$$

where $K \in \mathbb{R}^{n \times n}$ is the Gram matrix, $K_* = [k(\mathbf{x}^*, \mathbf{x}_1) \ldots k(\mathbf{x}^*, \mathbf{x}_n)]$, and $\theta_1 = 10^{-5}$ (Tikhonov regularization for noiseless data).

Memory scales quadratically with $n$, so **active subsampling** is used: greedily build a reduced dataset $\hat{X}$ by iteratively selecting the data point furthest from all already-included points, then moving the highest-error remaining point. Terminates after a fixed budget.

### Method Selection Guide (from paper)
- **GPR**: better for small rigs, sparse data, smooth parameter spaces, or rigs where artist animations thoroughly cover the parameter space.
- **MLP**: better for large rigs, dense data, or when training time is acceptable. Scales better to high-dimensional outputs.
- **Super-sampling** (MLP only): apply when rig parameter space is covered unevenly by artist animations; interpolates in rig space then evaluates forward to add in-distribution skeleton positions.

### Refinement Step
Both methods can be followed by a Newton refinement step using the Jacobian of the rig function (estimated via finite differences or analytically). This iteratively adjusts the predicted rig parameters to minimize the residual in joint position space, recovering the exact inverse when the rig function is injective in a neighborhood of the prediction.

## Key Results
- Rig inversion for quadruped, biped, deformable mesh, and facial rigs.
- GPR with subsampling achieves competitive accuracy using far less data than MLP.
- Super-sampling MLP outperforms both plain MLP and GPR on large rigs.
- Newton refinement with analytic Jacobian reduces residual to near-zero for smooth rigs.
- Real-time performance (< 1 ms per frame) for all methods after training.

## Limitations
- MLP training requires large artist-animated datasets; GPR training requires smaller but still curated datasets. Both depend on having example poses.
- GPR memory scales as $O(n^2)$; impractical for very large rigs without aggressive subsampling.
- Neural method has known generalization failures far from training distribution (explicitly motivates [[papers/gustafson-2020-inverse-rig]] and [[papers/marquis-bolduc-2022-differentiable-rig]]).
- No explicit handling of non-injectivity — multiple rig parameters mapping to the same skeleton pose cause conflicting gradients.

## Connections
- [[papers/holden-2015-inverse-rig]] — conference version (SCA 2015); this is the extended journal release
- [[papers/gustafson-2020-inverse-rig]] — Pixar's analytic Jacobian approach; addresses the Jacobian cost this paper defers to finite differences
- [[papers/marquis-bolduc-2022-differentiable-rig]] — SIGGRAPH Asia 2022; directly motivated by limitations of this work; uses mesh loss to handle non-injectivity
- [[papers/an-2024-refined-inverse-rigging]] — more recent neural inverse rigging work
- [[concepts/rig-inversion]]
- [[authors/holden-daniel]]
- [[authors/komura-taku]]

## Implementation Notes
- The GPR subsampling strategy (farthest-point selection + highest-error promotion) is directly applicable to any dataset curation problem where coverage matters more than density.
- Super-sampling: interpolate two rig parameter vectors in rig space ($\mathbf{y} = \alpha \mathbf{y}_a + (1-\alpha) \mathbf{y}_b$), evaluate the forward rig function to get a valid skeleton position, add the pair to the training set. This is cheap (only requires rig evaluations, no artist time).
- For Houdini KineFX: the Newton refinement step maps directly to the Gauss-Newton loop in [[vex/inverse-rig-mapping.vex]] Snippet B.
