---
title: "Skinning with Dual Quaternions"
authors: [Kavan, Ladislav; Collins, Steven; Žára, Jiří; O'Sullivan, Carol]
venue: I3D 2007
year: 2007
tags: [skinning, dqs, lbs, dual-quaternion, artifacts]
source: raw/papers/kavan-2007-dqs.pdf
---

## Summary
Replaces matrix blending in LBS with dual quaternion blending. Eliminates the candy-wrapper artifact while remaining GPU-friendly. Introduces bulging at certain joint configurations as a trade-off.

## Problem
LBS interpolates transformation matrices linearly. The average of two rotations is not a valid rotation — it collapses volume (candy-wrapper artifact) at twisted joints.

## Method
Represent each bone transform as a dual quaternion. Blend linearly, then normalize. Because dual quaternions encode rigid transforms, the blend stays on the rigid transform manifold.

## Key Results
No candy-wrapper. GPU shader compatible. Widely adopted in game engines and DCCs.

## Limitations
- Bulging artifact at certain configurations.
- Shortest-path ambiguity for rotations > 180°.
- Doesn't help with non-rigid (muscle/fascia) deformation.

## Connections
- [[concepts/linear-blend-skinning]]
- [[concepts/dual-quaternion-skinning]]
- [[authors/kavan-ladislav]]

## Implementation Notes
Handle sign flipping: flip dual quaternion if dot product with reference < 0. Available as deform mode in Houdini Bone Deform SOP.
