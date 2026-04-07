---
title: "Rig Inversion"
tags: [rig-generation, pose-space, math, neural]
---

## Definition
Rig inversion (or rig retargeting) is the problem of finding rig control parameter values $\mathbf{q}$ such that the rig's output (skeleton pose or mesh shape) matches a target $\mathbf{T}$:

```math
\mathbf{q}^* = \arg\min_\mathbf{q} \| f(\mathbf{q}) - \mathbf{T} \|^2
```

where $f: \text{rig params} \to \text{skeleton/mesh}$ is the rig's forward evaluation function. The challenge is that $f$ is nonlinear, expensive to evaluate, and its Jacobian $\partial f / \partial \mathbf{q}$ is required by gradient-based solvers.

## Variants / Taxonomy
- **Hard-coded heuristics**: artist-specified rules mapping skeleton joint ranges to rig controls. Fast but brittle.
- **Iterative least-squares (Gauss-Newton/Levenberg-Marquardt)**: numerically solves the system using finite-difference Jacobian. Accurate but slow — requires many rig evaluations per frame.
- **Analytic Jacobian learning** [[papers/gustafson-2020-inverse-rig]]: offline-learned polynomial or neural approximation of the rig; enables real-time Jacobian computation.
- **Neural rig inversion**: train a direct $\mathbf{T} \to \mathbf{q}$ regression network.

## Key Papers
- [[papers/gustafson-2020-inverse-rig]] — analytic Jacobian learning for real-time rig inversion

## Connections
- [[papers/radzihovsky-2020-facebaker]] — complementary: approximating rig output (forward direction)
- [[concepts/pose-space-deformation]] — rig inversion is relevant when pose-space sculpts need to be matched

## Notes
Rig inversion is critical for:
- **Crowd systems**: motion synthesis operates in skeleton space; inversion maps back to rig space for hero rig polish.
- **Motion capture retargeting**: mocap gives skeleton angles; character rigs use abstract parameters.
- **Physics-driven animation**: simulation outputs skeleton poses that must be expressed in rig control space.

The computational bottleneck is always the Jacobian. The analytic Jacobian learning approach amortizes this cost offline at the expense of approximation error for out-of-distribution poses.
