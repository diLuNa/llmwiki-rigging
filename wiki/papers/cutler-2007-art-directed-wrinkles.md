---
title: "An art-directed wrinkle system for CG character clothing and skin"
authors: [Cutler, Lawrence D.; Gershbein, Reid; Wang, Xiaohuan Corina; Curtis, Cassidy; Maigret, Erwan; Prasso, Luca; Farson, Peter]
venue: Computers & Graphics 2007
year: 2007
tags: [correctives, pose-space, blendshapes, skinning, houdini]
source: raw/papers/ArtDirectedWrinkles.pdf
---

## Summary
A kinematic, art-directable wrinkle system for CG character clothing and skin used in production at PDI/DreamWorks. Artists sculpt wrinkle patterns on a small set of reference poses using a curve-based tool; at runtime the system measures local surface stress to blend between reference wrinkle deformations. Used successfully on multiple DreamWorks feature films.

## Problem
Cloth simulation is too slow, hard to art-direct, and collision-prone for production at scale. Existing fast kinematic approaches lacked artist control, smooth blending between multiple wrinkle states, or scale to full feature film pipelines.

## Method
Two-phase pipeline:

**Wrinkle Creation (offline):** Artist selects 10–12 reference poses (arm raise, elbow bend, torso twist, etc.). In an interactive tool, they draw wrinkle curves on the reference mesh surface. The system extrudes a displacement field from these curves using a Gaussian profile, creating per-vertex displacement offsets relative to the un-deformed pose. Each reference pose stores: curve positions, displacement vectors, and a *stress map* (per-vertex surface stress measurement).

**Wrinkle Evaluation (runtime, per frame):**
1. Compute the current frame's stress map by measuring local surface deformation (strain tensor or surface metric change).
2. Compare the animation stress map to each reference pose stress map to derive *proximity weights*: how close the current pose is to each reference.
3. Smooth-filter weights to avoid discontinuities between reference poses.
4. Sum the weighted displacement fields and apply as a final geometry deformation pass.

Stress is measured as a local surface metric — the change in edge lengths / angles around each vertex between the animated pose and the bind pose, capturing both compression and stretch.

**Extensions:**
- *Age wrinkles*: model-space wrinkles for skin that persist and change slowly across poses.
- *Retargeting*: wrinkle curve patterns can be transferred between costumes or characters sharing similar topology.

## Key Results
- Fast, history-independent; runs at interactive rates.
- Clean smooth blending as characters move between reference poses.
- Art-directable at the curve level: artist controls wrinkle profile, orientation, amplitude.
- Deployed on multiple PDI/DreamWorks feature-length animated films.

## Limitations
- Requires upfront artist work to define reference poses and sculpt wrinkle curves per pose.
- Quality bounded by the density and quality of reference poses; wrinkles not seen in any reference pose may not appear.
- Purely kinematic — no physical accuracy or dynamic secondary motion.
- Wrinkles applied as geometry displacement (not render-time displacement maps) which affects memory and pipeline integration.

## Connections
- [[concepts/pose-space-deformation]] — same spirit of pose-space interpolation applied to wrinkles
- [[papers/lewis-2000-psd]] — foundational pose-space deformation reference
- [[papers/mancewicz-2014-delta-mush]] — complementary post-process smoothing layer
- [[papers/degoes-2020-sculpt]] — sculpt processing as a later generalization

## Implementation Notes
The stress map is the key signal for pose-proximity weighting. A simple approximation: for each vertex, compute the ratio of current edge lengths to rest edge lengths, then combine into a scalar stress via an RMS or max over incident edges. For more fidelity, use the Cauchy–Green strain tensor (FᵀF − I) projected to a scalar.

Curve-to-displacement: the paper uses a Gaussian cross-section profile perpendicular to the wrinkle curve, decaying to zero at a user-specified radius. The displacement is applied in surface-normal direction, optionally with a tangential component to create folds.

## Quotes
> "Our goal was to create a viable alternative to clothing simulations that could be used for tighter garments on any human characters."

> "The wrinkles should animate smoothly into different patterns as the motion changes. The wrinkles should also be large enough to affect the silhouette edge."
