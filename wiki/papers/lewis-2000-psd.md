---
title: "Pose Space Deformation"
authors: [Lewis, J.P.; Cordner, Matt; Fong, Nickson]
venue: SIGGRAPH 2000
year: 2000
tags: [correctives, pose-space, blendshapes, rbf]
source: raw/papers/lewis-2000-psd.pdf
---

## Summary
Unifies skinning and corrective shapes by treating correctives as functions of pose parameters, interpolated via RBFs across pose space.

## Problem
Prior correctives were binary or hand-interpolated curves. No smooth, general mechanism for blending across arbitrary pose combinations.

## Method
Represent corrective deltas at scattered pose-space samples. Interpolate via RBFs keyed on joint rotation parameters.

## Limitations
- Unpredictable behavior far from sample points.
- Doesn't address corrective authoring, only interpolation.
- Scales poorly with DOF count.

## Connections
- [[concepts/pose-space-deformation]]
- [[concepts/blendshapes]]
- [[papers/degoes-2020-sculpt]] — tooling for authoring the correctives PSD interpolates
