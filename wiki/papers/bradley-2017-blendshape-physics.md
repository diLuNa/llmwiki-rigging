---
title: "Enriching Facial Blendshape Rigs with Physical Simulation"
authors: [Bradley, Derek; Bächer, Moritz; Thomaszewski, Bernhard; Beeler, Thabo; Gross, Markus]
venue: Eurographics 2017
year: 2017
tags: [simulation, blendshapes, muscles, digital-human, correctives]
source: ~no local PDF~
---

## Summary
Augments a standard facial blendshape rig with physically-based soft tissue simulation. The blendshape rig defines a *kinematic target* (the intended shape); FEM elastic simulation then drives the actual mesh toward that target while respecting physical constraints (volume preservation, inertia, damping). The result is physically plausible soft tissue jiggle and secondary motion on top of existing facial rigs.

## Problem
Facial blendshapes produce perfectly crisp, frame-accurate deformation but lack physical plausibility — no jiggle, no volume preservation, no soft tissue dynamics. Full facial FEM simulation is too expensive and hard to art-direct. A method that enriches existing blendshape rigs with physics, without replacing them, is needed.

## Method
**Architecture:** Blendshape rig evaluates a *target shape* $\mathbf{x}_\text{rig}(t)$ each frame. The physical simulation layer maintains a mesh $\mathbf{x}(t)$ with elastic energy:
```math
E(\mathbf{x}) = E_\text{elastic}(\mathbf{x}) + E_\text{attachment}(\mathbf{x}, \mathbf{x}_\text{rig})
```
where $E_\text{elastic}$ is a neo-Hookean or corotated linear FEM energy and $E_\text{attachment}$ penalizes deviation from the rig target.

**Attachment energy:** Acts as a spring pulling the simulation toward the rig shape, with spatially-varying stiffness (stiffer near bone contact, softer in fatty regions).

**Time integration:** Implicit integration for stability; the attachment energy provides a stabilizing force. Real-time via subspace acceleration or reduced-order model.

**Material properties:** Spatially varying stiffness and damping tuned per anatomical region (bone-supported vs. fatty cheek tissue).

## Key Results
- Physically plausible soft tissue jiggle and secondary motion on production facial rigs.
- Art-directability preserved: rig target always respected asymptotically.
- Demonstrated on realistic human face models.
- Compatible with existing blendshape rig pipelines as a post-process.

## Limitations
- Additional simulation layer adds runtime cost.
- Material property tuning requires TD effort.
- Linearized FEM may not capture extreme deformations.
- Not real-time without subspace reduction.

## Connections
- [[papers/choi-2022-animatomy]] — complementary anatomy-based approach to facial rigging
- [[papers/zhu-2024-fabrig]] — cloth-simulation-based facial parameterization
- [[papers/hahn-2013-rig-space-secondary]] — rig-space secondary dynamics (body)
- [[papers/smith-2018-neo-hookean]] — neo-Hookean elastic model used for FEM layer
- [[concepts/blendshapes]] — the rig this enriches
- [[authors/beeler-thabo]] — co-author

