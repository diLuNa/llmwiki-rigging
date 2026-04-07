---
title: "Skinning: Real-time Shape Deformation"
authors: [Jacobson, Alec; Deng, Zhigang; Kavan, Ladislav; Lewis, J.P.]
venue: SIGGRAPH Course 2014
year: 2014
tags: [skinning, lbs, dqs, correctives, blendshapes, pose-space, math]
source: ~no local pdf~
---

## Summary
Comprehensive survey and tutorial covering the full landscape of skinning techniques for real-time character deformation: LBS, DQS, cage-based skinning, pose-space deformation, neural and data-driven approaches. The standard reference for the field as of 2014.

## Problem
No unified practical reference for skinning methods existed. The field had fragmented across papers spanning 25 years, making it hard to understand tradeoffs and choose the right approach for a given production need.

## Method
Survey organized by technique class:
- **Linear blend skinning (LBS)**: formulation, artifacts, practical tips
- **Dual quaternion skinning (DQS)**: candy-wrapper fix, interpolation issues
- **Shape-aware deformers**: CoR (Center of Rotation), spline-based
- **Pose-space deformation / correctives**: Lewis et al. 2000, radial basis functions
- **Data-driven / example-based**: regression, PCA blendshapes
- **Cage-based skinning**: harmonic coordinates, Green coordinates
- **Physically based**: rig-space physics, elasticity-inspired

Also covers weight computation: automatic skinning weights (BBW, etc.), painting workflows.

## Key Results
- Unified taxonomy of skinning methods with shared notation.
- Practical guidance on choosing among methods by production context.
- Widely cited reference; essentially defines the vocabulary of the skinning field.

## Limitations
- Survey; does not introduce new methods.
- 2014 cutoff; neural skinning developments (e.g., SkinningNet, NBS) postdate it.

## Connections
- [[concepts/linear-blend-skinning]]
- [[concepts/dual-quaternion-skinning]]
- [[concepts/pose-space-deformation]]
- [[concepts/bounded-biharmonic-weights]]
- [[papers/jacobson-2011-bbw]]
- [[papers/kavan-2007-dqs]]
- [[papers/lewis-2000-psd]]
- [[authors/jacobson-alec]]
- [[authors/kavan-ladislav]]

## Implementation Notes
The course notes are freely available online. Start here before any other skinning paper — the shared notation and taxonomy save significant time when reading primary sources.
