---
title: "Subspace Clothing Simulation Using Adaptive Bases"
authors: [Hahn, Fabian; Thomaszewski, Bernhard; Coros, Stelian; Sumner, Bob; Cole, Forrester; Meyer, Mark; DeRose, Tony; Gross, Markus]
venue: ACM SIGGRAPH 2014
year: 2014
tags: [simulation, correctives, neural]
source: ~no local PDF~
---

## Summary
A subspace simulation method for character clothing that adapts its reduced basis dynamically based on the current pose. A library of local bases is precomputed offline from pose-space training simulations; at runtime, the relevant bases are blended and the simulation is solved in the resulting low-dimensional subspace. Achieves orders-of-magnitude speedup over full cloth simulation while preserving pose-dependent wrinkling.

## Problem
Full cloth simulation is too expensive for real-time or interactive use. Static subspace methods (fixed basis) fail to capture pose-dependent wrinkling — the optimal subspace changes dramatically with character pose. Blend shapes for cloth require extensive artist authoring per pose.

## Method
**Training:** Run full cloth simulation for a set of representative poses $\{\mathbf{q}_k\}$. For each, compute local PCA basis $\mathbf{U}_k$ capturing the cloth deformation modes.

**Basis blending:** At runtime for pose $\mathbf{q}$, blend local bases using pose-space weights $w_k(\mathbf{q})$:
```math
\mathbf{U}(\mathbf{q}) = \sum_k w_k(\mathbf{q}) \mathbf{U}_k
```
Bases are orthogonalized after blending.

**Subspace simulation:** Project elastic forces, mass, and damping into the current subspace; solve the low-dimensional ODE system each frame.

**Adaptive DOFs:** Number of retained modes per basis adapts to local detail level — more modes near complex wrinkle regions.

## Key Results
- 10–100× speedup over full cloth simulation.
- Pose-dependent wrinkling quality matches full simulation.
- Real-time performance on GPU-accelerated subspace solve.
- Demonstrated on dressed character bodies.

## Limitations
- Training simulations required for each garment + character combination.
- Basis interpolation can introduce artifacts at large pose extrapolations.
- Topology changes (e.g., sliding garments) not handled.

## Connections
- [[papers/hahn-2013-rig-space-secondary]] — same group, rig-space secondary motion
- [[papers/hahn-2012-rig-space-physics]] — same group, SIGGRAPH 2012 predecessor
- [[papers/waggoner-2022-cloth-tailoring]] — Pixar cloth pipeline context
- [[papers/olmos-2025-cloth-draping]] — more recent blended-UV cloth approach
- [[concepts/pose-space-deformation]] — related idea: pose-indexed correctives

