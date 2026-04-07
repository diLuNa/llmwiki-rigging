---
title: "Patch-based Surface Relaxation"
authors: [de Goes, Fernando; Sheffler, William; Comet, Michael; Martinez, Alonso; Kutt, Aimei]
venue: SIGGRAPH Talks 2018
year: 2018
tags: [smoothing, correctives, houdini, laplacian, deformation]
source: raw/papers/2018.SiggraphTalks.GSCMK.pdf
---

## Summary
A patch-aware surface relaxation method that uses local decal maps to encode the desired edge-flow structure of a reference mesh, enabling relaxation that respects quad patch layout rather than just minimizing curvature. Used at Pixar for post-simulation cleanup and rigging in *Bao* and *Incredibles 2*.

## Problem
Standard Laplacian smoothing operators blur surface details and destroy quad patch layout (edge flow structure). When relaxing deformed meshes back toward a rest configuration, existing operators don't preserve the local patch topology that riggers and modelers care about.

## Method
Three contributions:
1. **Decal-map weighting**: local UV maps encode the desired patch edge-flow structure; used as weights in the relaxation operator.
2. **Patch-transfer update rule**: transfers a reference patch arrangement to a deformed mesh iteratively.
3. **Surface-constrained regime**: uses decal maps to project relaxed points back onto the surface, enabling sliding within the surface for volume preservation.

## Key Results
- Preserves quad patch layout under large deformations.
- Demonstrated on post-sim cleanup and rest-pose restoration for Pixar production assets.
- Outperforms vanilla Laplacian on edge-flow fidelity metrics.

## Limitations
- Requires pre-authored decal maps (setup cost).
- Iterative; convergence speed depends on mesh complexity and deformation magnitude.

## Connections
- [[concepts/laplacian-smoothing]] — the baseline this extends
- [[papers/degoes-2020-sculpt]] — related sculpt relaxation work
- [[authors/degoes-fernando]]
- [[authors/sheffler-william]]

## Implementation Notes
The decal map concept is essentially a per-vertex or per-face local UV that encodes desired flow direction. In Houdini, a similar effect can be approximated by using `uv` attributes as weights in a custom SOP.
