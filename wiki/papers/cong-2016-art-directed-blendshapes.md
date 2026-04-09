---
title: "Art-Directed Muscle Simulation for Film Characters"
authors: [Cong, Matthew; Bao, Michael R.; Fedkiw, Ronald]
venue: SIGGRAPH 2016 (ACM Transactions on Graphics 35(4))
year: 2016
tags: [muscles, simulation, blendshapes, digital-human, rig-generation]
source: knowledge
---

## Summary
Bridges the gap between physics-based muscle simulation and production blendshape rigs by generating a **blendshape basis from the anatomy simulation model**. Each FACS action unit is simulated via FEM muscle activation, and the resulting surface mesh deformation is stored as a blendshape delta. At runtime, the blendshape rig runs at interactive rates; the simulation only runs offline during character rigging. Crucially, the blendshapes capture muscle-driven nonlinear deformation including tissue interaction (bulging, sliding), not just linear displacements. SIGGRAPH 2016.

## Problem
Direct FEM muscle simulation (Cong et al. 2015) produces high-quality facial deformation but is too slow for interactive animation workflows (hours per frame). Production pipelines require blendshape rigs that run at interactive rates. A method was needed to bake physics quality into a fast blendshape representation with art-directable controls.

## Method
**Blendshape generation from simulation:**
1. Start from anatomy model (Cong et al. 2015): volumetric tet mesh + muscle fibers
2. For each FACS AU $k$, activate the corresponding muscles to full activation ($a_k = 1$, all others $= 0$)
3. Run quasistatic FEM simulation to equilibrium
4. Extract surface mesh deformation: blendshape delta $\mathbf{d}_k = \mathbf{x}_{sim}(\mathbf{a} = \mathbf{e}_k) - \mathbf{x}_{neutral}$
5. Result: set of blendshape deltas $\{\mathbf{d}_k\}$ encoding muscle-physics quality deformation

**Art direction:** artists can sculpt corrections on top of simulation blendshapes. Correctives from sculpture are combined additively. Simulation blendshapes provide the physically-correct base; sculpt provides the art direction.

**Combination blendshapes:** generate interaction shapes for AU pairs that have synergistic muscle interactions (e.g., brow raise + brow squeeze). These cannot be approximated by linear combination of individual AU shapes due to tissue contact and sliding.

**Runtime:** standard blendshape evaluation at interactive rates. No simulation at runtime.

## Key Results
Demonstrated that simulation-derived blendshapes preserve tissue sliding and bulging behavior not achievable with manually sculpted shapes. Artists reported requiring significantly less sculpt correction on simulation blendshapes vs. hand-sculpted. Deployed on film characters (Kong, see Cong 2017). SIGGRAPH 2016.

## Limitations
Blendshape approximation loses dynamic effects (no temporal filtering, no secondary dynamics). Linear combination of blendshapes cannot capture all nonlinear interactions — requires explicit combination shapes. AUs must be pre-defined; novel muscle activation combinations not in the basis require re-simulation.

## Connections
- [[papers/cong-2015-anatomy-pipeline]] — anatomy model source for the simulation blendshapes
- [[papers/cong-2017-kong-muscle-talk]] — production deployment (Kong)
- [[papers/teran-2005-quasistatic-flesh]] — FEM engine for generating each blendshape via simulation
- [[papers/lewis-2014-blendshape-star]] — blendshape rig framework this integrates into
- [[papers/bradley-2017-blendshape-physics]] — alternative: add physics on top of existing blendshapes (vs. generating blendshapes from physics)
- [[concepts/muscles]] — key application: muscle simulation → blendshape basis generation
- [[concepts/blendshapes]] — simulation-derived blendshapes as production rig targets
- [[authors/cong-matthew]]
- [[authors/fedkiw-ronald]]

## Implementation Notes
The blendshape generation process is embarrassingly parallel: each FACS AU simulation is independent. In practice, combination shapes for $N$ AUs requires $O(N^2)$ simulations — expensive but one-time. At 51 AUs (FACS core set) this is ~2,600 pair simulations. ILM in practice generates only the combinations that have significant physical interaction (tissue contact or crossing muscle pairs).
