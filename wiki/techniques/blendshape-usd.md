---
title: "Blendshapes in UsdSkel / Houdini Solaris"
tags: [usd, usdskel, blendshapes, houdini, solaris, lops]
---

## Overview
How to author, export, and drive blendshapes in the UsdSkel schema from Houdini Solaris.

## Key Steps
1. Author delta meshes in SOPs (one per shape).
2. In LOPs, use `Configure Primitive` or custom Python LOP to write `UsdSkelBlendShape` prims.
3. Apply `UsdSkelBindingAPI` to the mesh prim, listing all blendshape targets.
4. Drive weights via `UsdSkelAnimation.blendShapeWeights` (time-varying float array).

## Weight Convention
UsdSkel uses non-normalized weights. Ensure DCC sculpts are exported without clamping. See [[concepts/blendshapes]] and [[concepts/usdskel]].

## Houdini Notes
- `Blend Shapes SOP` → SOPs-level preview.
- In Solaris: Python LOP or the experimental UsdSkel export workflow in Houdini 21.
- HDK plugin approach: custom file plugin for OpenUSD can intercept blendshape authoring.
