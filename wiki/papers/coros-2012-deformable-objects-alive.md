---
title: "Deformable Objects Alive"
authors: [Coros, Stelian; Martin, Sebastian; Thomaszewski, Bernhard; Schumacher, Christian; Sumner, Bob; Gross, Markus]
venue: ACM SIGGRAPH 2012
year: 2012
tags: [simulation, rig-generation, muscles, volumes]
source: ~no local PDF~
---

## Summary
A framework for creating physically-simulated, art-directable deformable characters. Controllers specified in a rig-like parameter space drive target shapes for FEM simulation; the simulation adds physical dynamics (inertia, collisions, soft tissue response) while respecting animator intent. Bridges rig-based animation and physics simulation in a unified pipeline.

## Problem
Art-directed character animation and physically-based simulation are typically separate pipelines. Rig-driven animation lacks physical dynamics; full simulation is hard to control. A system that allows artists to work with familiar rig-like controls while getting physical behavior automatically is needed.

## Method
**Rig control layer:** Artists specify motion using control parameters (positions, orientations, blend weights) — similar to a traditional rig.

**Target shape:** Control parameters define a kinematic target shape $\mathbf{x}_\text{target}(t)$ via forward kinematics or blendshapes.

**Physical simulation:** An FEM elastic body is attached to the target shape via spatially-varying spring forces (attachment energy). The simulation tracks the rig target while satisfying physical constraints.

**Contacts and collisions:** Full rigid/deformable contact handling via penalty or constraint methods.

**Material model:** Corotated linear elasticity for efficiency; spatially-varying stiffness (stiff near skeleton, soft at surface).

## Key Results
- Physically plausible deformable characters with rig-style art direction.
- Secondary dynamics, contact response, and volume preservation emerge from physics.
- Demonstrated on varied characters (creatures, abstract shapes).
- Interactive rates via GPU acceleration.

## Limitations
- FEM cost limits resolution; coarse proxy meshes needed for real-time.
- Attachment energy formulation can over-constrain vs. true anatomical behavior.
- Material parameter tuning is non-trivial.

## Connections
- [[papers/hahn-2012-rig-space-physics]] — companion paper on rig-space physics from same group
- [[papers/hahn-2013-rig-space-secondary]] — follows up with rig-space secondary motion
- [[papers/bradley-2017-blendshape-physics]] — similar approach applied to facial rigs
- [[papers/smith-2018-neo-hookean]] — improved elastic model applicable here
- [[concepts/neo-hookean-simulation]] — physics model class

