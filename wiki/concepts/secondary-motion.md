---
title: "Secondary Motion"
tags: [simulation, correctives, hair, skinning, secondary-motion]
---

## Definition
Secondary motion refers to the physically plausible but non-primary deformations of a character — skin jiggle, soft tissue lag, hair settling, clothing follow-through — that are driven by but not directly controlled by the animator. It enriches primary (animated) motion without requiring full physical simulation of every asset.

## Variants / Taxonomy

- **Rig-space secondary motion**: dynamics computed in the space of rig parameters (joint angles, blendshape weights), then mapped back to geometry. Avoids full FEM. See [[papers/hahn-2013-rig-space-secondary]], [[papers/hahn-2012-rig-space-physics]].
- **Simulation-based secondary motion**: FEM or mass-spring systems layered on top of kinematic deformation. More accurate but expensive. See [[papers/mcadams-2011-elasticity-skinning]].
- **Data-driven secondary motion**: statistical models learned from reference video or simulation. Generalize cheaply to new animations. See [[papers/jain-2010-hand-secondary]].
- **Hair / cloth secondary motion**: strand or cloth simulation driven by skeleton, with shape-restore forces to maintain styled look. See [[papers/iben-2019-hair-shape]], [[papers/hahn-2014-subspace-cloth]].

## Key Papers
- [[papers/hahn-2013-rig-space-secondary]] — rig-space stiffness matrix K_q = J^T K_x J; real-time secondary dynamics
- [[papers/hahn-2012-rig-space-physics]] — physics in rig parameter space; blends with animator control
- [[papers/iben-2019-hair-shape]] — centroid and force constraints to hold hair shape during simulation
- [[papers/jain-2010-hand-secondary]] — data-driven secondary motion for hand animation
- [[papers/mcadams-2011-elasticity-skinning]] — efficient elasticity for character skin secondary deformation
- [[papers/hahn-2014-subspace-cloth]] — subspace cloth for secondary clothing motion

## Connections
- [[concepts/pose-space-deformation]] — static correctives that approximate secondary motion at specific poses
- [[concepts/neo-hookean-simulation]] — physics model underlying high-quality secondary motion
- [[concepts/blendshapes]] — secondary motion sometimes baked into blendshapes for performance

## Notes
Secondary motion sits at the intersection of simulation and animation: riggers want predictable, art-directable results; simulation provides physical plausibility. The key production challenge is making secondary motion responsive to animator overrides without breaking physical coherence.

Rig-space formulations (Hahn et al.) are the most production-friendly: they inherit the rig's existing parameter space, respect rig constraints, and can be real-time on commodity hardware.
