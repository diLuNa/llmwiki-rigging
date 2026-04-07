---
title: "Holding the Shape in Hair Simulation"
authors: [Iben, Hayley; Brooks, Jacob; Bolwyn, Christopher]
venue: SIGGRAPH Talks 2019
year: 2019
tags: [simulation, hair, correctives, secondary-motion]
source: raw/papers/2019.SiggraphTalks.IBB.pdf
---

## Summary
Presents a collection of force- and constraint-based techniques for guiding hair simulation back toward a groomed (artist-specified) rest shape, developed and refined across multiple Pixar features (Brave, Inside Out, The Good Dinosaur, Coco, Incredibles 2, Toy Story 4).

## Problem
Hair simulation is physics-based, but purely physical simulation often drifts far from the styled/groomed look. Hard kinematic constraints on scalp points don't provide enough shape control, especially for complex hairstyles that must recover their designed silhouette after dynamic perturbation.

## Method
Multiple complementary techniques:
- **Centroid-based shape constraints**: constrain the centroid of selected hair point groups to a target position, pulling hair toward a desired shape region rather than a specific point.
- **Force-based shape restoration**: apply soft spring forces toward groomed positions.
- **Layered kinematic constraints**: authored during setup, not per-shot, to reduce artist burden.
- No single universal approach; different character hair types require different combinations.

## Key Results
- Achieved predictable style recovery for diverse hair types across six Pixar features.
- Setup-time authoring reduces per-shot iteration.
- Demonstrated on Helen (Incredibles 2) hair simulation.

## Limitations
- Requires careful per-character tuning; no single parameter set works universally.
- Constraint forces can conflict with physical behavior under strong dynamics.

## Connections
- [[concepts/secondary-motion]] — hair simulation as secondary motion
- [[authors/iben-hayley]]

## Implementation Notes
Centroid constraints are straightforward to implement: compute the mean position of a selected vertex group each frame and apply a spring force toward the target centroid. Works better than per-vertex springs because it doesn't over-constrain individual strand degrees of freedom.
