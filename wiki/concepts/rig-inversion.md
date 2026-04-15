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

### Body rig inversion (skeleton → rig parameters)
- **Hard-coded heuristics**: artist-specified rules mapping skeleton joint ranges to rig controls. Fast but brittle.
- **Iterative least-squares (Gauss-Newton/Levenberg-Marquardt)**: numerically solves the system using finite-difference Jacobian. Accurate but slow — requires many rig evaluations per frame.
- **Analytic Jacobian learning** [[papers/gustafson-2020-inverse-rig]]: offline classification of rig parameters into analytic operators (RotationOp, TranslationOp, ForearmTwistOp); enables exact Jacobian at near-zero runtime cost. Best when rig operators are linear-in-angle. ~5000× speedup.
- **Neural direct inverse mapping** [[papers/holden-2015-inverse-rig]] [[papers/holden-2017-inverse-rig-tvcg]]: train MLP or GPR to map joint positions → rig parameters. No Jacobian needed; fast at runtime; requires artist animation data; degrades out-of-distribution.
- **Differentiable rig approximation + mesh loss** [[papers/marquis-bolduc-2022-differentiable-rig]]: train a differentiable MLP to approximate the rig function, then train the inverse model with a vertex-space loss through the frozen rig approximation. Handles non-injective and non-surjective rigs; no artist-posed training data needed; best for large black-box facial rigs.

### Blendshape rig inversion (mesh → blendshape weights)
- **Per-frame least-squares**: minimize ‖B w - (v_target - v₀)‖² s.t. 0 ≤ w ≤ 1. Closed-form for linear blendshapes via NNLS. Baseline for all blendshape inversion work.
- **Quartic model + coordinate descent** [[papers/rackovic-2023-highfidelity-inverse-rig]]: extend to quartic (4-way) corrective models; coordinate descent with controller-influence ordering enforces mutual exclusivity implicitly; >20% sparser weights than SOTA.
- **Quadratic corrective + SQP/MM** [[papers/rackovic-2023-accurate-interpretable-inverse-rig]]: SQP for maximum accuracy; MM algorithm for accuracy/sparsity balance; up to 45% RMSE improvement vs SOTA on quadratic corrective models.
- **Distributed ADMM** [[papers/rackovic-2023-distributed-rig-inversion]]: cluster the face spatially, solve each cluster independently via ADMM with shared overlapping weights; recovers accuracy lost by naive clustering; parallelizable.
- **Temporal + sparsity + quartic (Quartic Smooth)** [[papers/an-2024-refined-inverse-rigging]]: joint optimization over entire animation sequences; L1 sparsity + roughness penalty on second differences; 14× smoother than frame-by-frame quartic solving; evaluated on MetaHuman (80 base + 400+ correctives).

## Key Papers
- [[papers/holden-2015-inverse-rig]] — first data-driven inverse rig mapping; MLP on artist animation data (SCA 2015)
- [[papers/holden-2017-inverse-rig-tvcg]] — extended journal version; adds GPR and super-sampling (TVCG 2017)
- [[papers/gustafson-2020-inverse-rig]] — analytic Jacobian learning; ~5000× speedup for linear-operator rigs (SIGGRAPH Talks 2020)
- [[papers/marquis-bolduc-2022-differentiable-rig]] — differentiable rig approximation + mesh loss; handles non-bijective rigs; 3–4× error reduction over Holden 2015 (SIGGRAPH Asia 2022)
- [[papers/rackovic-2023-highfidelity-inverse-rig]] — quartic blendshape model + coordinate descent; >20% sparsity gain (arXiv 2023)
- [[papers/rackovic-2023-accurate-interpretable-inverse-rig]] — SQP/MM solvers for quadratic correctives; up to 45% RMSE improvement (arXiv 2023)
- [[papers/rackovic-2023-distributed-rig-inversion]] — ADMM clustered distributed inversion (SIGGRAPH Asia 2023 Technical Communications)
- [[papers/an-2024-refined-inverse-rigging]] — Quartic Smooth: joint temporal + sparsity + accuracy optimization (SIGGRAPH Asia 2024)

## See Also
- [[techniques/inverse-rig-mapping]] — implementation guide with Python + VEX; arm/forearm CompoundOp example

## Connections
- [[papers/radzihovsky-2020-facebaker]] — complementary: approximating rig output (forward direction)
- [[concepts/pose-space-deformation]] — rig inversion is relevant when pose-space sculpts need to be matched

## Notes
Rig inversion is critical for:
- **Crowd systems**: motion synthesis operates in skeleton space; inversion maps back to rig space for hero rig polish.
- **Motion capture retargeting**: mocap gives skeleton angles; character rigs use abstract parameters.
- **Physics-driven animation**: simulation outputs skeleton poses that must be expressed in rig control space.

The computational bottleneck is always the Jacobian. The analytic Jacobian learning approach amortizes this cost offline at the expense of approximation error for out-of-distribution poses.
