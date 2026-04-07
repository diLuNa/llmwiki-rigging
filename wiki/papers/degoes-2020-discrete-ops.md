---
title: "Discrete Differential Operators on Polygonal Meshes"
authors: [de Goes, Fernando; Butts, Andrew; Desbrun, Mathieu]
venue: SIGGRAPH 2020
year: 2020
tags: [math, laplacian, deformation, houdini]
source: raw/papers/2020.SiggraphPapers.GBD.pdf
---

## Summary
Constructs a principled family of discrete differential operators (gradient, Laplacian, covariant derivative, shape operator) for arbitrary polygonal meshes — including non-planar and non-convex faces — extending existing tools beyond triangulated meshes. Enables geometry processing algorithms to run natively on quad and n-gon production meshes.

## Problem
Most discrete differential geometry operators (cotangent Laplacian, etc.) are derived for triangle meshes. Production meshes are predominantly quad or mixed polygon. Existing approaches either triangulate (losing mesh structure) or use ad hoc polygon extensions.

## Method
Builds on exterior calculus (discrete differential forms) extended to polygonal meshes. Key steps:
- Decompose each polygon into virtual triangles for integration but preserve polygon topology.
- Derive consistent discrete gradient and Laplacian operators acting on both scalar fields (0-forms) and vector fields (1-forms/tangent fields).
- Covariant derivative and shape operator follow from the same framework.
- All operators satisfy a discrete Stokes theorem on polygonal domains.

## Key Results
- Gradient, Laplacian, covariant derivative, shape operator — all consistent on polygonal meshes.
- Demonstrated: grooming (fur/feather direction fields via Poisson equations on quad meshes).
- Seamless extension of triangle-mesh algorithms (e.g., harmonic parameterization, vector field design).

## Limitations
- Focused on surface operators; volumetric (tetrahedral/hex) operators not addressed.
- Non-planar polygon handling is approximate for highly warped faces.

## Connections
- [[concepts/laplacian-smoothing]] — Laplacian operator is a key instance
- [[concepts/bounded-biharmonic-weights]] — related operator (biharmonic = Laplacian²)
- [[authors/degoes-fernando]]
- [[authors/desbrun-mathieu]]

## Implementation Notes
The cotangent-weight Laplacian generalizes naturally to polygons via virtual triangle decomposition. In Houdini, this is relevant when implementing custom smoothing or parameterization SOPs on non-triangulated meshes.
