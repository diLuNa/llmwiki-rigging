---
title: "Interactive Display and Animation of B-Spline Solids as Muscle Shape Primitives"
authors: [Ng-Thow-Hing, Victor; Fiume, Eugene]
venue: Computer Animation and Simulation 1997 (Eurographics Workshop)
year: 1997
tags: [muscles, simulation, deformation, math, skinning]
source: https://link.springer.com/chapter/10.1007/978-3-7091-6874-5_6
---

## Summary
Proposes trivariate B-spline solids as the primary shape primitive for anatomically-based muscle modeling. A muscle is represented as a volumetric B-spline solid parameterized in 3D; the parametric $u$-direction defines muscle fibre orientation; the spring-mass model applied to control points produces physically-based dynamic deformation. Data-fitting procedures construct the solid from profile curves or medical contour data. The first principled approach to representing muscles as volumetric shapes with internal structure rather than surface meshes or implicit primitives.

## Problem
Existing muscle representations (cylinders, ellipsoids, surface patches) lack the volumetric richness needed for anatomically accurate animation:
- No internal fibre structure — cannot model anisotropic contraction
- Cannot capture complex cross-sectional shapes from medical data
- Surface-only models cannot preserve volume during deformation
- Spring-mass models applied to surface meshes have no notion of "inside"

## Method

### B-Spline Solid Representation
A trivariate B-spline solid $\mathbf{S}(s,t,u)$ maps parameters $(s,t,u) \in [0,1]^3$ to 3D world space:

```math
\mathbf{S}(s,t,u) = \sum_{i} \sum_{j} \sum_{k} N_{i,p}(s)\, N_{j,q}(t)\, N_{k,r}(u)\, \mathbf{P}_{ijk}
```

where $N_{i,p}$ are B-spline basis functions of degree $p$ over a knot vector. The control points $\mathbf{P}_{ijk}$ form a 3D lattice. Unlike the Bernstein (FFD) version, B-spline basis functions have **local support** — only nearby control points influence any given region.

### Fibre Orientation
Iso-parametric curves in the $u$-direction define muscle fibre bundles:

```
fibre direction at (s,t,u) = ∂S/∂u (normalized)
```

This allows the solid to model the complex helical fibre arrangements of real muscles (e.g., pennate muscles). The 3D parameterization allows fibre density to vary across the cross-section.

### Data Fitting
Two fitting procedures:

1. **Profile curves**: Draw 2D profile curves outlining the muscle boundary; fit the B-spline solid to reproduce these profiles while maintaining smooth interior.

2. **Medical contour data**: Stack 2D contours from MRI/CT slices; fit the solid to reproduce the contour cross-sections at each slice.

Fitting uses least-squares minimization in the $L^2$ norm over the B-spline parameter space.

### Spring-Mass Dynamics
A spring-mass system is applied to the control points $\mathbf{P}_{ijk}$:
- **Interior springs**: Connect adjacent control points in all three parametric directions, resisting stretching
- **Torsional springs**: Resist twisting
- **Mass**: Proportional to the volume element at each control point

Contraction is modeled as shortening springs in the $u$-direction (fibre direction). External forces (contact, gravity, neighboring muscles) are applied to control points.

The dynamic state of the solid is fully described by the positions and velocities of its control points — a compact $(l+1)(m+1)(n+1)$-dimensional state vector.

## Key Results
- Demonstrated on soleus and other lower-leg muscles
- Data-fit from real MRI contour data
- Interactive animation of contraction and deformation at near-real-time rates (on 1997 hardware)
- Volume preservation enforced via spring constraints on control point Jacobian

## Limitations
- Spring-mass dynamics are not physically accurate for soft tissue (no stress-strain curve, no viscosity model) — superseded by FEM approaches for high-fidelity simulation
- Data-fitting is a manual or semi-automatic process
- No collision handling between adjacent muscle volumes
- The solid represents the muscle bulk only; attachment to bones via tendons requires additional modeling

## Connections
- [[concepts/b-spline-volumes]] — this paper's primary contribution to the B-spline volume literature
- [[papers/sederberg-1986-ffd]] — foundational FFD; Ng-Thow-Hing generalizes to B-splines for local support
- [[concepts/muscles]] — foundational reference for volumetric muscle shape representation
- [[papers/teran-2005-quasistatic-flesh]] — FEM-based successor for accurate muscle/flesh simulation
- [[papers/cong-2016-art-directed-blendshapes]] — modern production muscle simulation
- [[authors/ng-thow-hing-victor]]

## Implementation Notes
- The B-spline evaluation $\mathbf{S}(s,t,u)$ is separable: evaluate three 1D B-spline basis vectors and take their outer product to get the weight tensor for the control points. This is $O((l+1)(m+1)(n+1))$ per point after precomputing basis values.
- For Houdini VEX: store control points as prim attributes on a `Grid` SOP (or use `Lattice` SOP); evaluate the B-spline basis at vertex local coordinates.
- Knot vector design: clamp the B-spline at both ends (repeated knots at 0 and 1) so that boundary control points exactly interpolate the boundary — important for specifying muscle attachment points at the tendon ends.
- The parametric $u$ direction should be aligned with the long axis of the muscle to give meaningful fibre orientations.
