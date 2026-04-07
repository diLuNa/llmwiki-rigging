---
title: "Efficient Simulation of Secondary Motion in Rig-Space"
authors: [Hahn, Fabian; Thomaszewski, Bernhard; Coros, Stelian; Sumner, Bob; Gross, Markus]
venue: ACM/Eurographics Symposium on Computer Animation (SCA) 2013
year: 2013
tags: [simulation, rig-generation, secondary-motion, correctives]
source: ~no local PDF~
---

## Summary
Adds physically plausible secondary jiggle/dynamics to rig-driven characters by simulating elastic motion directly in the low-dimensional **rig parameter space** rather than in full mesh space. A linearized elastic model is projected into rig space; the result is a compact system of ODEs that can be solved in real-time, adding dynamics to arbitrary rig DOFs (blend weights, joint angles, etc.).

## Problem
Full FEM simulation of secondary dynamics is too slow for character animation pipelines. Existing secondary motion approaches either require manual spring setups (per-shot tuning) or expensive subspace methods that don't integrate naturally with the production rig.

## Method
**Rig parameterization:** Character deformation is written as $\mathbf{x}(\mathbf{q})$ where $\mathbf{q}$ are rig parameters (joint angles, blendshape weights, etc.) and $\mathbf{x}$ is the mesh.

**Linearized elastic energy in rig space:**
The elastic potential energy $E(\mathbf{q})$ is approximated as quadratic in rig-space displacements $\delta\mathbf{q}$ around the animated pose $\mathbf{q}_0(t)$:
```math
E \approx \frac{1}{2} \delta\mathbf{q}^\top \mathbf{K}_q \, \delta\mathbf{q}
```
where $\mathbf{K}_q = \mathbf{J}^\top \mathbf{K}_x \mathbf{J}$ is the mesh stiffness $\mathbf{K}_x$ projected through the rig Jacobian $\mathbf{J} = \partial\mathbf{x}/\partial\mathbf{q}$.

**Dynamic simulation:** Solving $\mathbf{M}_q \ddot{\delta\mathbf{q}} + \mathbf{D}_q \dot{\delta\mathbf{q}} + \mathbf{K}_q \delta\mathbf{q} = \mathbf{f}_q$ — a low-dimensional (n_rig DOF) system updated each frame.

The actual rig parameters fed to the character are $\mathbf{q}(t) = \mathbf{q}_\text{anim}(t) + \delta\mathbf{q}(t)$.

**Rig Jacobian:** Computed by differentiating the rig's deformation map w.r.t. its parameters.

## Key Results
- Real-time secondary dynamics on production rigs with no mesh-level simulation.
- Physically tunable (stiffness, damping) without per-joint spring authoring.
- Demonstrated on face, body, and clothing rigs.
- Seamless integration: operates as a post-process on top of any existing rig.

## Limitations
- Linearization breaks for large secondary oscillations (small perturbation assumption).
- Rig Jacobian computation requires differentiable rig; complex procedural rigs may not be straightforward.
- Projection loses accuracy when mesh stiffness distribution doesn't align with rig DOFs.

## Connections
- [[papers/hahn-2012-rig-space-physics]] — same group, SIGGRAPH 2012 predecessor on rig-space physics
- [[papers/hahn-2014-subspace-cloth]] — companion paper on subspace cloth simulation
- [[papers/kim-2022-dynamic-deformables]] — broader survey of dynamics methods
- [[concepts/rig-inversion]] — related: mapping dynamics back to rig space

