---
title: "Dynamic Kelvinlets: Secondary Motions Based on Fundamental Solutions of Elastodynamics"
authors: [de Goes, Fernando; James, Doug L.]
venue: SIGGRAPH 2018
year: 2018
tags: [sculpting, elasticity, deformation, volumes, secondary-motion, math]
source: ~no local pdf~
---

## Summary
Extends the Kelvinlet framework from static elasticity to *elastodynamics*, deriving closed-form brush displacements that produce secondary motion effects — ripples, jiggle, traveling waves — from impulsive or persistent force distributions. Same real-time, closed-form advantages as Regularized Kelvinlets but now time-dependent.

## Problem
Static Kelvinlets produce instantaneous deformation with no temporal dynamics. Character sculpting and secondary motion effects require time-evolving deformations: a muscle jiggle after impact, a ripple across a belly, a tail whip follow-through.

## Method
Derives fundamental solutions (Kelvin state) of the *elastodynamic* wave equation in infinite 3D media:

```math
\rho\,\ddot{\mathbf{u}} = \mu\,\nabla^2\mathbf{u} + (\lambda+\mu)\nabla(\nabla\cdot\mathbf{u}) + \mathbf{b}
```

Regularizes with a spatial blob $\rho_\varepsilon$ (as in static Kelvinlets) to obtain smooth, bounded dynamic brushes. Impulsive, step, and ramp force profiles yield different time-evolution shapes. Supports longitudinal and transverse wave modes separately.

## Key Results
- Closed-form, real-time dynamic deformations with physically based wave behavior.
- Demonstrated on secondary motion: muscle jiggle, belly ripple, tail whip.
- Seamless composability with static Regularized Kelvinlets [[papers/degoes-2018-kelvinlets]].

## Limitations
- Infinite elastic medium assumption — no boundary reflections.
- Linear elastodynamics — large deformations not captured.
- No damping model (undamped waves travel indefinitely without augmentation).

## Connections
- [[papers/degoes-2018-kelvinlets]] — static predecessor; same framework
- [[papers/degoes-2019-sharp-kelvinlets]] — concurrent sharpness extension
- [[concepts/kelvinlets]]
- [[authors/degoes-fernando]]
- [[authors/james-doug]]
