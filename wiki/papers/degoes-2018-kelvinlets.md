---
title: "Regularized Kelvinlets: Sculpting Brushes based on Fundamental Solutions of Elasticity"
authors: [de Goes, Fernando; James, Doug L.]
venue: SIGGRAPH 2018
year: 2018
tags: [sculpting, elasticity, deformation, volumes, math]
source: raw/papers/2018.SiggraphPapers.GJ.pdf
---

## Summary
Introduces Regularized Kelvinlets: closed-form, physically based sculpting brushes derived from the fundamental solutions (Kelvin state) of linear elasticity. Brushes correspond to grab, scale, twist, and pinch operations and provide real-time volumetric deformation with interactive volume control.

## Problem
Real-time sculpting tools typically use ad hoc falloff functions with no physical basis, yielding implausible volume behavior. Physics-based approaches (FEM) are too slow for interactive use.

## Method
Derives brush displacements as the regularized version of Kelvinlets — fundamental solutions of linear elasticity in infinite 2D/3D media. For a force distribution $f(\mathbf{x})$ applied at a brush center, the displacement field $\mathbf{u}(\mathbf{x})$ is:

```math
\mathbf{u}(\mathbf{x}) = \mathbf{K}_\epsilon(\mathbf{x}) \cdot \mathbf{f}
```

where $\mathbf{K}_\epsilon$ is a regularized Green's function parameterized by brush scale $\epsilon$. Compound brushes with arbitrarily fast spatial decay are constructed via multi-scale extrapolation. Pointwise displacement and derivative constraints can be imposed through a single linear solve.

## Key Results
- Four primitive brush types (grab, scale, twist, pinch) with closed-form expressions.
- Real-time performance on high-resolution meshes.
- Volume control via Lamé parameter tuning.
- Demonstrated on volume sculpting and 2D image editing.

## Limitations
- Infinite-medium assumption; behavior near boundaries is approximate.
- No collision handling with other geometry.
- Purely elastic model — no plasticity or large-deformation effects.

## Connections
- [[papers/degoes-2019-sharp-kelvinlets]] — extension with cusp/non-smooth profiles
- [[concepts/kelvinlets]] — concept page for the Kelvinlet family
- [[authors/degoes-fernando]]
- [[authors/james-doug]]

## Implementation Notes
Closed-form expressions make these straightforward to implement in VEX or Python. The regularization parameter $\epsilon$ directly maps to brush radius. The grab brush is the most commonly used; scale and twist are useful for volume correction passes.

## Quotes
> "These deformations thus provide the realism and plausibility of volumetric elasticity, and the interactivity of closed-form analytical solutions."
