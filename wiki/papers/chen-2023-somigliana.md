---
title: "Somigliana Coordinates: an elasticity-derived approach for cage deformation"
authors: [Chen, Jiong; de Goes, Fernando; Desbrun, Mathieu]
venue: SIGGRAPH 2023
year: 2023
tags: [cage-deformation, deformation, math, elasticity]
source: raw/papers/2023.SiggraphPapers.CGD.pdf
---

## Summary
Introduces Somigliana Coordinates — a new class of cage deformation coordinates derived from the Somigliana identity (boundary integral formulation of linear elasticity). Generalizes Green Coordinates with physically plausible volume control, no shearing artifacts, and interactive bulging.

## Problem
Existing cage deformers (mean-value coordinates, Green coordinates) either suffer from shearing artifacts or lack volume control. Green Coordinates are the state of the art but cannot produce convincing bulge effects and can produce undesirable shearing under large deformations.

## Method
Derives cage deformation from the **Somigliana identity**:

```math
\mathbf{u}(\mathbf{x}) = \int_{\partial\Omega} \left[ T(\mathbf{y},\mathbf{x})\,\mathbf{u}(\mathbf{y}) - K(\mathbf{y},\mathbf{x})\,\mathbf{t}(\mathbf{y}) \right] d\sigma_\mathbf{y}
```

where $T$ and $K$ are elasticity kernels (traction and displacement Green's functions). The coordinates are **matrix-valued** — combining both cage vertex positions and face normals — and computed via a corotational scheme. This yields:
- Invariance under similarity transformations.
- Interactive volume bulging via a single parameter.
- No shearing in pure rotation.

Coordinates are evaluated numerically via quadrature (closed-form not available in 3D).

## Key Results
- Generalizes Green Coordinates: recovers them as a special case.
- Volume bulging controllable interactively.
- Demonstrated on 2D and 3D examples; superior to Green Coordinates on volume preservation metrics.

## Limitations
- Coordinate evaluation is more expensive than Green Coordinates (numerical quadrature).
- Matrix-valued coordinates have a larger memory footprint.
- Currently no closed-form 3D solution; quadrature approximation.

## Connections
- [[concepts/cage-deformation]]
- [[papers/degoes-2018-kelvinlets]] — same elasticity fundamental-solution methodology
- [[authors/degoes-fernando]]
- [[authors/desbrun-mathieu]]
- [[authors/chen-jiong]]

## Quotes
> "Our deformer thus generalizes Green coordinates, while producing physically-plausible spatial deformations that are invariant under similarity transformations and with interactive bulging control."
