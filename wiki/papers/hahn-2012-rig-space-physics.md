---
title: "Rig-Space Physics"
authors: [Hahn, Fabian; Martin, Sebastian; Thomaszewski, Bernhard; Sumner, Robert; Coros, Stelian; Gross, Markus]
venue: SIGGRAPH 2012
year: 2012
tags: [simulation, rig-generation, pose-space, math, muscles]
source: ~no local pdf~
---

## Summary
Reformulates physical simulation in the reduced space of rig parameters rather than in full vertex space. Physical forces are projected through the rig Jacobian into rig-control space, enabling physics-driven character animation that respects rig structure — secondary motion, soft-tissue dynamics, and physical plausibility emerge automatically within the rig's degrees of freedom.

## Problem
Full FEM simulation ignores the rig structure; conversely, rig-only animation ignores physics. Coupling them naively (simulate → feed back into rig) is ill-defined because the rig maps rig-params → vertex positions but not vice versa. A principled coupling requires projecting physics into the space the rig already controls.

## Method
Given rig mapping $\mathbf{x} = f(\mathbf{q})$ where $\mathbf{q}$ are rig parameters and $\mathbf{x}$ are vertex positions, the rig Jacobian is $J = \partial f / \partial \mathbf{q}$. Physical forces $\mathbf{f}$ in vertex space are projected into rig space:

```math
\mathbf{f}_\text{rig} = J^T \mathbf{f}
```

The reduced equation of motion is then:

```math
J^T M J\, \ddot{\mathbf{q}} = J^T \mathbf{f}_\text{elastic} + J^T \mathbf{f}_\text{external}
```

This yields a small system (rig DOF count, not mesh vertex count) that can be time-integrated efficiently. Secondary dynamics and physically-driven follow-through emerge within the rig's subspace.

## Key Results
- Physics-driven secondary motion that respects the rig's structure.
- System size equals the number of rig parameters — far cheaper than full FEM.
- Natural secondary dynamics (jiggle, follow-through) without hand-tuning.
- Demonstrated on characters with bone + blendshape rigs.

## Limitations
- Rig subspace limits the expressiveness of physical deformation — effects outside the rig's span cannot emerge.
- Requires computing the rig Jacobian $J$, which is expensive for complex procedural rigs.
- Linearization of the rig (constant $J$) can limit accuracy under large deformations.

## Connections
- [[concepts/pose-space-deformation]] — rig parameters often include PSD corrective weights
- [[concepts/rig-inversion]] — related problem: projecting back from vertex space to rig space
- [[papers/gustafson-2020-inverse-rig]] — efficient Jacobian approximation relevant here
- [[papers/smith-2018-neo-hookean]] — physical forces could use this stable model
- [[authors/sorkine-olga]] (Sorkine in group at ETH at the time)

## Quotes
> Physical forces are reduced to the rig's degrees of freedom, producing physics-driven secondary motion that is guaranteed to respect the character's rig structure.

## Implementation Notes
The bottleneck is computing $J$ per frame. For rigs with analytic Jacobians (joint chains, blend weights) this is feasible; for complex procedural rigs it requires finite differencing or the analytic learning approach of [[papers/gustafson-2020-inverse-rig]]. The reduced mass matrix $J^T M J$ can be precomputed if $J$ changes slowly.
