---
title: "Muscles & Soft Tissue Simulation"
tags: [muscles, simulation, volumes, skinning, rig-generation, digital-human]
---

## Definition
Muscle and soft tissue systems in character rigging encompass two related but distinct problems:

1. **Muscle as rig control** — anatomically-inspired virtual muscles whose contraction drives skin deformation, providing a physiologically meaningful parameterization of facial or body animation controls.
2. **Soft tissue as simulation** — volumetric FEM (or proxy) simulation of flesh, fat, and skin responding to skeletal motion, producing physically plausible secondary deformation (jiggle, compression, stretch).

The two can coexist in a pipeline: muscles drive the skeleton; soft tissue simulation responds to skeletal+muscular motion to produce the final surface deformation.

## Variants / Taxonomy

### Facial Muscle Systems
Anatomy-inspired virtual muscles as rig controls for facial animation. Replaces or underlies FACS blendshapes with muscle fiber activations, reducing corrective shape counts and enabling physiologically consistent expression transfer.

- [[papers/pdi-1998-facial-antz]] — first major production deployment; 300+ virtual muscles (muscles, bone movements, eye rotations) layered into high-level controls; soft/hard area deformation per muscle; PDI/DreamWorks ANTZ (1998)
- [[papers/modesto-2014-dwa-face-system]] — DWA face system evolution ANTZ→Shrek→Mr Peabody; shows how muscle-based parameterization scaled over 16 years of production
- [[papers/choi-2022-animatomy]] — Weta FX / Avatar: The Way of Water; replaces FACS AUs with contractile fiber curves; strain $\gamma = (s - \bar{s})/\bar{s}$ per fiber → blendshape weights $B_E = E\gamma$; FLAME-style pose correctives $B_P$ for jaw/neck; fully transferable across identity
- [[papers/zoss-2018-jaw-rig]] — data-driven jaw anatomy rig; 6-DOF mandibular motion compressed to 3-DOF Posselt's Envelope; prevents physiologically infeasible poses; retargetable to new characters
- [[papers/zhu-2024-fabrig]] — anatomy-inspired muscle and fat patches deformed by cloth simulation; fully transferable across characters without per-character blendshape authoring

### Full Musculoskeletal Simulation
Physics-based simulation of the complete anatomical stack: bones → muscles/tendons → fat → skin. Highest fidelity, highest cost.

- [[papers/murai-2016-musculoskeletal-skin]] — complete layered stack validated against real subjects; muscles drive skeletal motion; layered soft tissue (fat, skin) responds with physically correct jiggling and compression

### Soft Tissue / Flesh FEM
Volumetric elastic simulation of flesh treated as a continuous material, without explicitly modeling individual muscle fibers. Used for body and face secondary deformation.

- [[papers/smith-2018-neo-hookean]] — stable Neo-Hookean hyperelastic model; robust volume preservation at Poisson's ratio ≈ 0.5; used in Pixar's Fizz simulator for flesh and cloth
- [[papers/mcadams-2011-elasticity-skinning]] — efficient corotational FEM for character skin with contact and self-collision at production scale; multigrid solver for interactive rates on tet meshes
- [[papers/kim-2022-dynamic-deformables]] — production course (Pixar Fizz); Neo-Hookean formulation, Hessian construction, collision handling, two-way coupling; includes open-source implementations
- [[papers/bouaziz-2014-projective-dynamics]] — Projective Dynamics: local constraint projections + global sparse solve; stable, fast, suitable for soft bodies and cloth at interactive rates

### Physics-Enriched Rigs (Rig ↔ Physics Coupling)
Bridges the rig and simulation layers — either projecting physics into rig space or using the rig as a target for simulation.

- [[papers/coros-2012-deformable-objects-alive]] — rig parameter space defines target shapes; FEM simulation adds physical dynamics while respecting animator intent; unified rig + physics pipeline
- [[papers/hahn-2012-rig-space-physics]] — simulates physics in the *reduced space* of rig parameters; forces projected through rig Jacobian; secondary motion, soft-tissue dynamics emerge within rig DOFs
- [[papers/bradley-2017-blendshape-physics]] — blendshape rig defines kinematic target; co-rotational FEM drives actual mesh toward it with volume preservation, inertia, damping; physically plausible jiggle on facial rigs

### Neural / Learned Muscle Surrogates
GNN or data-driven models that learn to approximate soft tissue dynamics without iterative solvers.

- [[papers/pfaff-2021-meshgraphnets]] — MeshGraphNets; learns physics simulation on production meshes including soft body (flesh/muscle proxy) dynamics; inference orders of magnitude faster than FEM

## Key Concepts

**Muscle as parametric control vs simulation object:**
Production pipelines almost never simulate anatomically correct muscle fibers at runtime — it's too expensive. Instead they use muscles in one of two ways:
- *As rig controls*: a "muscle" is a curve/vector whose contraction length drives a weight or corrective blend. No physics computed — just a better parameterization than FACS.
- *As simulation proxy*: a volumetric region whose elastic response is simulated. Typically collapsed into a layered approach: muscle activations → skeletal poses → FEM soft tissue.

**Flesh simulation material models:**
| Model | Volume preservation | Cost | Stability |
|-------|-------------------|------|-----------|
| Co-rotational linear FEM | Poor (large deformation) | Medium | Good |
| Neo-Hookean | Strong | Medium-High | Good (Smith 2018) |
| Projective Dynamics | Constraint-based | Low-Medium | Excellent |
| Position-Based Dynamics | Approximate | Low | Good |

**Rig-space physics (Hahn 2012):** Rather than simulating in $\mathbb{R}^{3N}$ (one vector per vertex), project everything into rig parameter space $\mathbb{R}^k$ where $k \ll 3N$. The rig Jacobian $J = \partial M / \partial q$ maps forces from vertex to rig space. Fast but limited to motion expressible in rig DOFs.

**Animatomy strain parameterization:**
```math
\gamma_m = \frac{s_m - \bar{s}_m}{\bar{s}_m}, \quad B_E = E \cdot \gamma
```
where $s_m$ is the contracted length of fiber $m$, $\bar{s}_m$ is rest length, and $E$ maps strain to skin displacement. This is the production-validated anatomy-to-deformation bridge in Animatomy.

## Connections
- [[concepts/neo-hookean-simulation]] — the hyperelastic material model underlying most production flesh simulations
- [[concepts/facial-blendshape-rigs]] — muscle systems underlie or replace FACS blendshapes in production facial rigs
- [[concepts/pose-space-deformation]] — muscle activations often drive PSD correctives as an intermediate step
- [[concepts/secondary-motion]] — soft tissue jiggle and dynamic skin response are a primary source of secondary motion
- [[concepts/mesh-graph-nets]] — MeshGraphNets as a neural surrogate for soft tissue FEM
- [[concepts/rig-inversion]] — mapping surface observations back to muscle activation parameters

## Notes

**Production hierarchy:** Most studios don't go below the muscle-as-control abstraction at runtime. Full musculoskeletal simulation (Murai 2016) is used for film VFX reference, not real-time.

**The "muscles" tag in this wiki** covers both uses: facial muscle control systems (PDI, Animatomy, DWA) and volumetric flesh simulation (Smith, McAdams, Coros, Bouaziz, Hahn). The connection is that both model the same underlying anatomical truth at different levels of abstraction and cost.
