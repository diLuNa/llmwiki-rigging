---
title: "Pose Space Deformation (PSD)"
tags: [correctives, pose-space, blendshapes, rbf]
---

## Definition
A framework for defining corrective shapes as continuous functions of pose parameters. Instead of discrete switch-on/off correctives, PSD interpolates between artist-sculpted deltas across the full pose space.

## How it works
1. Artist sculpts corrective deltas at key poses.
2. Poses are parameterized (joint rotations as vectors/quaternion components).
3. Deltas are interpolated at runtime via RBFs (or other scattered data interpolants) keyed on current pose parameters.

## Key Papers
- [[papers/lewis-2000-psd]] — foundational formulation

## Connections
- [[concepts/blendshapes]] — correctives are blendshape deltas
- [[papers/degoes-2020-sculpt]] — tooling for authoring the correctives PSD interpolates

## Notes
Modern pipelines sometimes replace RBF interpolation with learned models (neural PSD). Houdini's Pose-Space Deform SOP implements a production variant.
