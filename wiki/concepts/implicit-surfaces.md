---
title: "Implicit Surfaces"
tags: [deformation, simulation, rig-generation]
---

## Definition
An implicit surface is defined as the zero-level set of a scalar field $f: \mathbb{R}^3 \to \mathbb{R}$:

```math
S = \{ \mathbf{x} \in \mathbb{R}^3 \mid f(\mathbf{x}) = 0 \}
```

Interior is $f < 0$, exterior is $f > 0$. The surface is not represented as an explicit mesh but as a continuous field.

## Variants / Taxonomy
- **Metaballs / Blobby surfaces**: $f(\mathbf{x}) = \sum_i w_i(\|\mathbf{x}-\mathbf{c}_i\|) - \text{threshold}$; classic for organic, blobby shapes.
- **Signed Distance Fields (SDF)**: $f(\mathbf{x})$ = signed distance to nearest surface; well-behaved for many operations.
- **Level sets**: evolving implicit surfaces, often governed by PDEs (useful for simulation).
- **Neural implicit surfaces** (NeRF-adjacent): $f$ defined by a neural network.

## Key Papers
- [[papers/lykkegaard-2025-metaball-rig]] — first mesh-free production character rig (Pixar OOOOO); hierarchical metaball/implicit rig

## Connections
- [[concepts/linear-blend-skinning]] — mesh-based alternative for character deformation

## Notes
Production advantages of implicit surfaces for characters:
- Natural smooth blending between body parts (no mesh seams).
- Topological flexibility: can merge/split without remeshing.
- Uniform surface normal computation everywhere.

Main production challenges:
- Rendering requires marching cubes or direct raymarching — needs specialized pipeline.
- Animation controls must drive implicit primitives, not mesh vertices — requires new tools.
- Downstream effects (fur, cloth attachment) rely on mesh and require adaptation.

OOOOO's rig [[papers/lykkegaard-2025-metaball-rig]] solved this by treating the implicit field as a "rigged shader" with a hierarchical primitive hierarchy, using Pixar's custom implicit renderer.
