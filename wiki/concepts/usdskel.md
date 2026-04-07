---
title: "UsdSkel"
tags: [usd, usdskel, blendshapes, skinning, houdini, solaris]
---

## Definition
UsdSkel is the OpenUSD schema for skeletal animation. It encodes skeletons, joint hierarchies, skinning weights, rest poses, and blendshapes in a USD-native format.

## Key Schema Elements
- `UsdSkelSkeleton` — joint hierarchy with rest pose
- `UsdSkelAnimation` — time-varying joint transforms
- `UsdSkelBindingAPI` — applies skeleton and weights to a mesh
- `UsdSkelBlendShape` — per-shape delta array and optional inbetweens

## Blendshape Weight Convention
UsdSkel uses **non-normalized weights** (unbounded, not clamped to [0,1]). This differs from most DCC defaults. Weights can be negative (subtractive) or > 1 (overshoot). See [[concepts/blendshapes]] for implications.

## Multiple Shape Sets
UsdSkel supports multiple independent blendshape sets (e.g., separate corrective sets for different rigs or LODs) via primvar namespacing.

## Houdini Integration
Houdini 19.5+ has native UsdSkel import/export. In Solaris, blendshapes are authored via LOPs. HDAs can drive blendshape weights via USD attributes.

## Connections
- [[concepts/blendshapes]]
- [[techniques/blendshape-usd]]
