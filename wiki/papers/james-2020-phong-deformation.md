---
title: "Phong Deformation: A better C0 interpolant for embedded deformation"
authors: [James, Doug L.]
venue: SIGGRAPH 2020
year: 2020
tags: [simulation, deformation, volumes, math]
source: raw/papers/2020.SiggraphPapers.J.pdf
---

## Summary
Proposes Phong Deformation — a vertex-based quadratic interpolation scheme for embedded deformation in tetrahedral meshes — that greatly reduces faceting and shading artifacts compared to linear interpolation, at minimal computational overhead, without requiring mesh refinement.

## Problem
Physics simulations deform tetrahedral lattices; embedded surface geometry (the visible character mesh) is deformed by linearly interpolating tetrahedral element deformations. Linear interpolation produces visible faceting and normal discontinuities (C0 artifacts) that require expensive mesh refinement to resolve.

## Method
Analogous to Phong shading (vertex normals blended across a face), Phong Deformation:
1. Averages element-wise linear deformation models to vertices (cell-to-vertex reconstruction).
2. Barycentrically interpolates the vertex-based models at query points.
3. Blends the resulting quadratic estimate with the traditional linear interpolation using a weighting parameter.

The result is still C0 (no higher continuity guarantee), but visually much smoother than linear:

```math
\mathbf{x}' = (1-\alpha)\,\mathbf{x}'_\text{linear} + \alpha\,\mathbf{x}'_\text{Phong}
```

## Key Results
- Significantly reduced faceting on irregular tetrahedral meshes.
- Negligible additional cost vs. linear interpolation.
- Drop-in replacement; no changes to simulation or mesh.
- Works on irregular (production) tet meshes where smooth-tet schemes fail.

## Limitations
- Still C0; visible creases remain at sharp features.
- The blending parameter $\alpha$ requires tuning per-asset.
- Cell-to-vertex reconstruction step has choices that affect quality.

## Connections
- [[papers/smith-2018-neo-hookean]] — flesh sim context where embedded deformation is used
- [[papers/kim-2022-dynamic-deformables]] — production deformable context
- [[authors/james-doug]]

## Implementation Notes
The cell-to-vertex step is the same "Phong normal" averaging. Blending $\alpha=1$ is full Phong Deformation; $\alpha=0$ is standard linear. Start with $\alpha=0.5$ and tune visually.
