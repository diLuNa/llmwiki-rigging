---
title: "Sliding Deformation: Shape Preserving Per-Vertex Displacement"
authors: [Pinskiy, Dmitriy]
venue: Eurographics 2010 (Short Paper)
year: 2010
tags: [deformation, skinning, houdini, vex]
source: raw/papers/shapePreservingVertexDisplacement.pdf
---

## Summary
An algorithm for deforming a polygonal mesh by sliding vertices along the surface — creating the visual appearance of texture animation (detail sliding over skin) without a global parameterization. The method couples a local parameterization (minimal distortion per vertex region) with a global direction representation to ensure coherent sliding across the mesh.

## Problem
Animating surface detail — wrinkles, skin texture, flesh sliding over bone — requires moving mesh vertices tangentially along the surface rather than in world space. Global UV parameterization is too expensive and distortion-prone for interactive use; purely local approaches lose direction coherence across patch boundaries.

## Method
**Local parameterization spaces:** For each displaced vertex, build a local tangent-plane parameterization covering its neighborhood that minimizes area/angle distortion. This gives a precise mapping from 2D local UV to 3D surface in the affected region.

**Global direction in local frames:** A single sliding direction is specified in some global or object-space frame. To propagate this direction coherently across multiple local parameterization patches, the algorithm computes a representation of the global direction in each local frame while correcting for the parallel-transport error between adjacent patches.

**Displacement mapping:** Move each vertex along the surface by the prescribed direction and magnitude, using its local parameterization to project back to the nearest surface point after the displacement step. The result is a shape-preserving deformation: the mesh shape is maintained, only vertex positions on the surface change.

**Properties:**
- Inherently parallelizable (per-vertex local solves)
- Works on arbitrary topology meshes
- No global UV storage required
- Interactive feedback

## Key Results
- Achieves convincing sliding-flesh and wrinkle-migration effects.
- Low computational cost — suitable for production real-time deformation.
- Used at Walt Disney Feature Animation.

## Limitations
- 4-page short paper — implementation details are sparse.
- Sliding is tangential only; normal-direction deformation must be handled by a separate system.
- Direction coherence approximation may introduce small errors on highly curved surfaces.

## Connections
- [[papers/cutler-2007-art-directed-wrinkles]] — complementary approach: wrinkle placement vs. sliding
- [[papers/mancewicz-2014-delta-mush]] — another post-process deformation layer
- [[papers/degoes-2022-profile-curves]] — surface-aware deformation along curves

## Implementation Notes
In VEX: the core operation is projecting a world-space direction vector onto the local tangent plane (subtract the normal-projected component), then advancing the point by that projected vector, then re-snapping to the mesh surface (nearest-point projection). The parallel-transport correction across patches can be approximated with the `dihedral()` rotation between adjacent face normals.
