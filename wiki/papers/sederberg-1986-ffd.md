---
title: "Free-form Deformation of Solid Geometric Models"
authors: [Sederberg, Thomas W.; Parry, Scott R.]
venue: SIGGRAPH 1986
year: 1986
tags: [deformation, skinning, cage-deformation, math]
source: https://dl.acm.org/doi/10.1145/15886.15903
---

## Summary
The foundational paper for Free-Form Deformation (FFD). Wraps a 3D region of space in a trivariate Bernstein polynomial volume parameterized by a regular control point lattice. Moving control points deforms the ambient space continuously and differentiably; any embedded geometry (meshes, particles, solids) follows by re-evaluating its local coordinates. Introduced the idea of "deforming space rather than objects," enabling resolution-independent, smooth deformations without model-specific encoding.

## Problem
Direct mesh editing is cumbersome: every vertex must be moved individually, deformations are non-smooth, and the method does not generalize across representations (polygons, NURBS, CSG). There is no clean mathematical framework for intuitive, smooth, global-to-local deformation of arbitrary 3D geometry.

## Method

### Lattice Setup
A parallelpiped control lattice of $(l+1) \times (m+1) \times (n+1)$ control points $\mathbf{P}_{ijk}$ is placed around the object to be deformed. Three linearly independent axes $\mathbf{S}$, $\mathbf{T}$, $\mathbf{U}$ define the lattice coordinate system. For each embedded point $\mathbf{X}$, local coordinates $(s,t,u)$ are computed by projection onto the lattice axes.

### Deformation Map
The deformed position of a point with local coordinates $(s,t,u)$ is:

```math
\text{FFD}(s,t,u) = \sum_{i=0}^{l} \sum_{j=0}^{m} \sum_{k=0}^{n} \binom{l}{i}\binom{m}{j}\binom{n}{k} s^i(1-s)^{l-i} t^j(1-t)^{m-j} u^k(1-u)^{n-k} \mathbf{P}_{ijk}
```

This is a **trivariate Bernstein polynomial** evaluated at $(s,t,u)$. The basis functions are products of 1D Bernstein polynomials; the control points $\mathbf{P}_{ijk}$ define the deformation.

### Properties
- **Continuity**: $C^\infty$ within the lattice (Bernstein polynomials are analytic).
- **Convex hull property**: Deformed point lies in the convex hull of control points.
- **Affine invariance**: Applies to any geometric representation (polygons, NURBS, CSG, voxels).
- **Local coordinates stored once**: For static objects, $(s,t,u)$ are computed once offline; deformed positions require only a polynomial evaluation per animation frame.

### B-Spline Generalization
Shortly after, Griessmair and Purgathofer (1989) and others generalized FFD to B-spline basis functions, providing **local support** (only nearby control points affect a given region). This is the "B-spline volume" variant used in most production implementations.

## Key Results
- Applied to solid geometric models, NURBS surfaces, and polygon meshes in the original paper.
- Enables smooth, spatially coherent deformations by editing a small number of control points (typically $4^3 = 64$).
- Reduction in DOF: a million-vertex mesh controlled by 64 control points.

## Limitations
- Bernstein polynomial has global support within the lattice: moving any control point affects the entire enclosed region. (Solved by B-spline generalization.)
- No volume preservation guarantee: the deformation can collapse volume at extreme control point movements.
- Lattice must enclose the entire object being deformed, or separate lattices are needed for partial coverage.
- Finding local coordinates $(s,t,u)$ for arbitrary point positions requires solving a nonlinear system if the lattice is non-cuboid.

## Connections
- [[concepts/b-spline-volumes]] — the foundational reference for all B-spline/Bernstein volume deformation
- [[concepts/cage-deformation]] — cages are the modern generalization: same "deform space" idea but with arbitrary polyhedral topology (harmonic, Green, Somigliana coordinates)
- [[papers/ng-thow-hing-1997-bspline-solid]] — applies trivariate B-spline solids (generalization of FFD) to muscle shape modeling
- [[papers/kurenkov-2017-deformnet]] — differentiable FFD layer; makes control points learnable via neural networks

## Implementation Notes
- **PyGeM** (Python): `from pygem import FFD` — full B-spline FFD with arbitrary lattice sizes and CAD/mesh support. https://github.com/mathLab/PyGeM
- **Houdini**: Lattice SOP implements FFD-style deformation. For KineFX, the lattice can be driven by rig controls.
- Local coordinate computation: for axis-aligned cuboid lattice, $(s,t,u)$ = normalized dot product with axes. For arbitrary parallelpiped, solve $\mathbf{X} = \mathbf{X_0} + s\mathbf{S} + t\mathbf{T} + u\mathbf{U}$ for $(s,t,u)$.
- Bernstein evaluation is a linear function of control point positions: the full deformation is $\mathbf{P}_{deformed} = B \cdot \mathbf{P}_{control}$ where $B$ is the Bernstein basis matrix — trivially differentiable.
