---
title: "Physical Simulation for Character Deformation"
tags: [simulation, fem, elasticity, muscles, fascia, volumes, secondary-motion]
---

## Definition
Physical simulation computes the deformation of elastic or rigid bodies under external forces, contacts, and constraints by numerically integrating equations of motion or solving quasi-static equilibrium. In character animation, simulation is used for secondary motion (jiggle, soft tissue), cloth, muscles, fascia, and physics-driven corrective deformation on top of a skinned rig.

## Variants / Taxonomy

### Finite Element Method (FEM)
Discretizes a volume into elements; each element's deformation is governed by a constitutive model (Neo-Hookean, co-rotational, etc.). Most accurate but most expensive.
- [[papers/teran-2005-quasistatic-flesh]] — quasistatic FEM for flesh
- [[papers/sifakis-2005-anatomy-muscles]] — full anatomical FEM simulation
- [[papers/smith-2018-neo-hookean]] — stable Neo-Hookean model

### Projective Dynamics
Reformulates implicit integration as alternating local/global steps (ADMM-like). Fast convergence, amenable to GPU.
- [[papers/bouaziz-2014-projective-dynamics]] — foundational projective dynamics paper

### Rig-Space Physics
Projects simulation forces onto the rig's low-dimensional subspace (defined by the rig's Jacobian). Orders of magnitude cheaper than full simulation; trades accuracy for real-time performance.
- [[papers/hahn-2012-rig-space-physics]] — rig-space physics projection
- [[papers/hahn-2013-rig-space-secondary]] — secondary motion in rig space

### Machine Learning Surrogates for Simulation
Train a neural network to approximate expensive simulation outputs, enabling real-time inference.
- [[papers/benchekroun-2023-fast-complementary-dynamics]] — fast complementary dynamics via neural surrogate
- [[papers/benchekroun-2024-stiffgipc]] — stiff IPC simulation acceleration
- [[papers/pfaff-2021-meshgraphnets]] — MeshGraphNets for mesh-based simulation
- [[papers/fortunato-2022-multiscale-mgn]] — multiscale MeshGraphNets

### Cloth Simulation
- [[papers/hahn-2014-subspace-cloth]] — subspace cloth with adaptive bases
- [[papers/li-2022-ncloth]] — neural cloth
- [[papers/grigorev-2023-hood]] — neural cloth on body
- [[papers/waggoner-2022-cloth-tailoring]] — cloth tailoring workflow

### Facial Simulation
Physics-based facial deformation, often layered on top of blendshape rigs.
- [[papers/terzopoulos-1990-physically-based-face]] — early physically-based face model
- [[papers/sifakis-2006-speech-muscle]] — speech muscle simulation
- [[papers/bao-2019-face-capture-muscles]] — face capture with muscles
- [[papers/park-2024-realtime-face-sim-superres]] — real-time facial sim via super-resolution
- [[papers/yang-2024-generalized-physical-face]] — generalized physical face model
- [[papers/bradley-2017-blendshape-physics]] — blendshape enrichment with physics

### Rigid Body Resting
- [[papers/baktash-2025-resting-rigid-bodies]] — resting probability analysis for rigid bodies

## Key Papers
- [[papers/teran-2005-quasistatic-flesh]] — FEM flesh baseline
- [[papers/bouaziz-2014-projective-dynamics]] — projective dynamics
- [[papers/hahn-2012-rig-space-physics]] — rig-space physics (most relevant to rigging pipeline)
- [[papers/benchekroun-2023-fast-complementary-dynamics]] — neural surrogate for complementary dynamics
- [[papers/pfaff-2021-meshgraphnets]] — graph-network mesh simulation
- [[papers/lan-2025-jgs2]] — recent simulation work

## Connections
- [[concepts/skinning]] — simulation is often layered on top of a skinned character
- [[concepts/correctives]] — simulation-driven corrective shapes (complementary dynamics)
- [[concepts/rig-inversion]] — simulation outputs skeleton poses; rig inversion maps back to rig space
- [[concepts/muscles]] — anatomical muscle models drive simulation

## Notes
In production, full simulation is rarely run at final frame rate. The common pattern is: LBS/DQS skinning → pose-space correctives → rig-space physics or neural surrogate → final cloth/hair sim. Each layer adds fidelity while the earlier layers carry most of the motion.
