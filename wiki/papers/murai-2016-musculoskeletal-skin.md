---
title: "Dynamic Skin Deformation Simulation Using Musculoskeletal Model and Soft Tissue Dynamics"
authors: [Murai, Akihiko; Hong, Q. Youn; Yamane, Katsu; Hodgins, Jessica]
venue: Computational Visual Media / Pacific Graphics 2016
year: 2016
tags: [simulation, muscles, skinning, digital-human]
source: ~no local PDF~
---

## Summary
Simulates realistic dynamic skin deformation by combining a musculoskeletal model (bones, muscles, tendons) with a layered soft tissue simulation (fat, skin). Muscles drive skeletal motion; the soft tissue layer responds with physically correct jiggling, stretching, and compression. Validated against real motion capture + high-speed video of human subjects.

## Problem
LBS and blendshape rigs produce skin deformation with no physical dynamics — no jiggle, no tissue sliding, no subcutaneous fat behavior. Full FEM simulation of skin+muscle is expensive. A method grounded in anatomy that produces dynamic skin deformation at practical cost is needed.

## Method
**Musculoskeletal skeleton:** Bones connected by joints; muscles represented as active force-generating elements between attachment points. Muscle activations drive joint torques and skeletal motion.

**Layered tissue model:**
- *Deep tissue / fat:* volumetric elements (FEM) loosely coupled to skeleton with damped springs.
- *Skin surface:* thin shell or surface mesh coupled to fat layer.

**Dynamics:** Tissue layers respond to skeletal motion with inertia, damping, and elastic forces. Jiggle and secondary motion emerge naturally.

**Validation:** Compared against motion capture markers and synchronized high-speed video of human subjects performing various motions.

## Key Results
- Physically plausible skin dynamics (jiggle, tissue sliding) from musculoskeletal input.
- Quantitative validation against real human subjects.
- Demonstrated on arm and leg regions with complex muscle activation patterns.

## Limitations
- Musculoskeletal model setup is expensive (requires per-subject anatomy data).
- FEM tissue simulation not real-time.
- Muscle activation inference from motion is underdetermined (many solutions).

## Connections
- [[papers/mcadams-2011-elasticity-skinning]] — efficient elasticity for character skinning
- [[papers/choi-2022-animatomy]] — anatomy-inspired approach for facial muscles
- [[papers/bradley-2017-blendshape-physics]] — soft tissue dynamics for facial rigs
- [[papers/kim-2022-dynamic-deformables]] — dynamic deformables course
- [[concepts/neo-hookean-simulation]] — elastic model class for soft tissue

