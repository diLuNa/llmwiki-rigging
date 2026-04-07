---
title: "Deformation Transfer for Triangle Meshes"
authors: [Sumner, Robert W.; Popović, Jovan]
venue: SIGGRAPH 2004
year: 2004
tags: [deformation, correctives, skinning, mesh-wrap, math]
source: ~no local pdf~
---

## Summary
Given a source mesh deforming across poses and a target mesh at rest, Deformation Transfer computes target deformations that mimic the style of the source deformations while respecting the target's rest geometry. The key is transferring the local deformation gradients (per-triangle transformation matrices) rather than vertex positions.

## Problem
Retargeting deformations between meshes of different shapes is non-trivial. Pose-space offsets (deltas) from the source mesh cannot be directly applied to a target with different geometry — the deltas encode both the desired shape change and the source mesh's local geometry. A method is needed that transfers the *deformation intent* but respects the target's structure.

## Method
For each triangle $i$, compute the deformation gradient $Q_i$ (the affine transformation from rest to posed source):

```math
Q_i = \text{argmin}_Q \| Q S_i - D_i \|_F^2
```

where $S_i$ and $D_i$ are the rest and deformed source triangle edge matrices. Transfer $Q_i$ to the corresponding target triangle and solve for target vertex positions that minimize:

```math
\sum_i \| Q_i T_i^{\text{rest}} - T_i^{\text{deformed}} \|_F^2
```

This is a sparse linear system (one per spatial dimension) solvable via least squares.

## Key Results
- Transfers deformation style robustly between meshes of different shapes.
- Used at Pixar for sculpt transfer (cited in [[papers/degoes-2020-sculpt]]).
- Works even when source and target have different vertex counts.
- Generalizes naturally to corrective transfer.

## Limitations
- Requires a consistent correspondence between source and target triangles (typically provided by a mesh wrap).
- Triangle-level gradients miss vertex-level detail (smooth interiors but sharp boundaries need care).
- Can produce artifacts at mesh boundaries or near high-curvature regions.

## Connections
- [[papers/degoes-2020-sculpt]] — cites this as the basis for sculpt transfer
- [[papers/degoes-2019-mesh-wrap]] — mesh wrap provides the triangle correspondence needed here
- [[concepts/pose-space-deformation]]
- [[authors/sumner-robert]]

## Implementation Notes
The per-triangle deformation gradient is a 3×3 matrix computed from three edge vectors. The global solve is a Poisson problem (same structure as Laplacian surface editing). Open-source implementations available in libigl.
