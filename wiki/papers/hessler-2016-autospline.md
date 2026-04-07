---
title: "AutoSpline: Animation Controls Only When and Where You Need Them"
authors: [Hessler, Mark; Talbot, Jeremie]
venue: SIGGRAPH Talks 2016
year: 2016
tags: [rig-generation, skinning, deformation]
source: ~no local pdf~
---

## Summary
AutoSpline is a spline-based rigging tool developed at Pixar that automatically generates animation controls along chains (tails, tentacles, spines) and places them adaptively based on where control is needed — reducing setup time while giving animators direct curve-based handles.

## Problem
Rigging long, flexible appendages (tails, tentacles, hair, spines) requires many joints and controls. Manual setup is tedious, and control placement is non-obvious. Artists want intuitive curve-based control without manually placing every joint.

## Method
AutoSpline:
- Defines a smooth spline along the appendage chain.
- Auto-generates rig controls (handles) at user-specified positions or adaptively based on curvature.
- Drives joint rotations from spline tangent frames.
- Allows adding/removing controls interactively.

The "only when and where you need them" philosophy means controls are created on demand rather than at every joint.

## Key Results
- Used at Pixar for tails, tentacles, spines across multiple films.
- Cited as a component of the alien character rigging on *Elio* [[papers/singleton-2025-alien-rigs]].
- Reduced rig setup time for appendage characters.

## Limitations
- Primarily suited for chain-like structures; doesn't generalize to volume deformation.
- Less expressive than curvenet rigging for surface-level detail.

## Connections
- [[papers/nguyen-2023-curvenet-elemental]] — curvenet rigging as a more general successor
- [[papers/singleton-2025-alien-rigs]] — AutoSplines used alongside curvenets on Elio aliens
- [[concepts/curvenet-rigging]]
- [[authors/hessler-mark]]
- [[authors/talbot-jeremie]]
