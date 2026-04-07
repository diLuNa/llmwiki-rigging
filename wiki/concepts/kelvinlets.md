---
title: "Kelvinlets"
tags: [sculpting, elasticity, deformation, volumes, math]
---

## Definition
Kelvinlets are closed-form sculpting brush displacements derived from the fundamental solutions of linear elasticity (the Kelvin state). Given a force distribution applied at a brush center with scale $\epsilon$, the displacement field $\mathbf{u}(\mathbf{x})$ is a regularized Green's function of the Lamé equations:

```math
\mathbf{u}(\mathbf{x}) = \mathbf{K}_\epsilon(\mathbf{x}) \cdot \mathbf{f}
```

The regularization parameter $\epsilon$ controls brush radius; Lamé parameters $(\mu, \lambda)$ control material compressibility.

## Variants / Taxonomy
- **Regularized Kelvinlets** [[papers/degoes-2018-kelvinlets]]: original formulation. Four primitive brush types: grab, scale, twist, pinch. Smooth $C^\infty$ falloff.
- **Multi-scale (tri-scale) Kelvinlets**: construct faster spatial decay via linear extrapolation across brush scales. Reduces far-field influence but remains inherently smooth.
- **Sharp Kelvinlets** [[papers/degoes-2019-sharp-kelvinlets]]: Bi-Laplacian and Cusp variants with non-smooth, cusp-like profiles and fast far-field decay. Independent control of locality and spikiness.

## Key Papers
- [[papers/degoes-2018-kelvinlets]] — original formulation; grab, scale, twist, pinch brushes
- [[papers/degoes-2019-sharp-kelvinlets]] — Bi-Laplacian extension with cusp profiles

## Connections
- [[concepts/laplacian-smoothing]] — Laplacian operator applied to Kelvinlet kernels in Sharp Kelvinlets
- [[authors/degoes-fernando]]
- [[authors/james-doug]]

## Notes
Practical advantage over ad hoc sculpting brushes: volume behavior is physically motivated. The compressibility is controlled by the Poisson ratio embedded in the Lamé parameters — set $\nu \to 0.5$ for near-incompressible (volume-preserving) sculpts.

In VEX: the grab Kelvinlet is the most common. Given brush center $\mathbf{c}$, force $\mathbf{f}$, scale $\epsilon$:
```
vector r = pos - center;
float re = sqrt(dot(r,r) + epsilon*epsilon);
float a = 1.0/(8*PI*mu);
float b = 1.0/(4*(1-nu));  // for compressible
vector u = a * ( (2*(1-nu)/re + epsilon*epsilon/(re*re*re)) * force
               + b/(re*re*re) * dot(r,force) * r );
```
