---
title: "An Empirical Rig for Jaw Animation"
authors: [Zoss, Gaspard; Bradley, Derek; Bérard, Pascal; Beeler, Thabo]
venue: ACM Transactions on Graphics (SIGGRAPH 2018)
year: 2018
tags: [rig-generation, correctives, muscles, neural]
source: raw/papers/An-Empirical-Rig-for-Jaw-Animation-Paper.pdf
---

## Summary
A data-driven jaw rig built from accurate motion capture of jaw anatomy. The rig models the true 6-DOF manifold of mandibular motion (jaw-open, lateral deviation, protrusion) compressed to an intuitive 3-DOF control space based on Posselt's Envelope of Motion, preventing physiologically infeasible poses while retaining expressive range. Retargetable to new human and fantasy characters.

## Problem
Standard jaw rigs approximate motion as a rotation around a fixed pivot plus translation, missing the complex sliding behavior of the temporo-mandibular joint (TMJ). This produces incorrect jaw positioning and allows anatomically impossible poses. More-DOF rigs improve accuracy but are even more susceptible to infeasible poses without explicit constraint modeling.

## Method
**Anatomy-informed capture:**
- The TMJ involves both rotation and translation: for small openings the condyle rotates in socket; for large openings the condyle slides over the temporal bone, translating the effective pivot.
- Capture: fiducial markers placed on the skull and mandible of subjects; tracked with multiple cameras to reconstruct 6-DOF jaw motion accurately.

**Manifold analysis:**
- The 6-DOF jaw motion space is analyzed to find the low-dimensional structure (Posselt's Envelope of Motion — a well-known anatomical concept describing the outer boundary of all jaw positions).
- The manifold is parameterized with 3 intuitive DOFs: open/close, left/right, forward/backward.
- The parameterization places automatic limits on motion (joint stops, ligament limits) preventing infeasible poses.

**Rig construction:**
- A piecewise parametric map from the 3-DOF control space to rigid jaw pose (6-DOF transformation) fitted to the captured data.
- At runtime: animator moves 3 sliders → jaw pose computed via the empirical map.

**Retargeting:**
- The rig structure (envelope shape, pivot curve) is transferred to new characters by fitting the captured manifold parameterization to the target character's anatomy using a simple anatomical landmark alignment.

## Key Results
- Jaw motion is anatomically correct, matching the TMJ sliding behavior.
- 3-DOF control is as intuitive as existing simple rigs, but with correct biomechanics.
- Successfully retargeted to human and fantasy creature characters.
- Used in production (referenced by Animatomy for Avatar: The Way of Water).

## Limitations
- Requires capture data from real subjects to define the empirical manifold.
- Retargeting requires anatomical landmark identification on the target character.
- Covers jaw rigid body only; skin deformation around the jaw is a separate system.

## Connections
- [[papers/choi-2022-animatomy]] — uses this jaw rig as sub-component for Avatar production
- [[papers/lewis-2000-psd]] — pose-space deformation for skin driven by jaw poses
- [[concepts/rig-inversion]] — related: inverse mapping from jaw pose to rig controls
- [[authors/beeler-thabo]]

## Implementation Notes
The key implementation insight: the effective pivot of the jaw is not fixed but traces a curve in 3D space as the mouth opens. Model this as a polynomial or spline fit to the captured condyle trajectory, then parameterize open/close as arc-length along this curve. Lateral and protrusion DOFs are then offsets from this spine.

For Houdini: the jaw rig can be implemented as a Chops/Python SOP that maps the 3 user parameters through the empirical table (a 3D lookup grid fitted to the capture data) to output a rigid transform for the jaw bone.
