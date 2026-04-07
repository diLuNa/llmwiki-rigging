---
title: "Cage Deformation"
tags: [deformation, math, skinning]
---

## Definition
Cage deformation is a free-form deformation technique where a low-polygon *cage* mesh surrounds the character; displacing cage vertices deforms the interior (and exterior) via generalized barycentric coordinates. Each interior point $\mathbf{x}$ is expressed as a weighted combination of cage vertex positions:

```math
\mathbf{x} = \sum_i w_i(\mathbf{x})\,\mathbf{v}_i
```

The weights $w_i$ must satisfy *linear precision* (they reproduce linear functions exactly) and typically non-negativity and partition-of-unity.

## Variants / Taxonomy
- **Mean Value Coordinates (MVC)**: generalize barycentric coordinates to arbitrary polygons; can be negative outside convex cages.
- **Harmonic Coordinates** [[papers/joshi-2007-harmonic-coords]]: weights solve Laplace equation inside the cage; always non-negative; require volumetric solve.
- **Green Coordinates** [[papers/lipman-2008-green-coords]]: use both cage vertex positions *and* face normals; similarity-invariant; closed-form; state-of-the-art before Somigliana.
- **Somigliana Coordinates** [[papers/chen-2023-somigliana]]: derived from Somigliana identity (elasticity); generalizes Green Coordinates; adds interactive volume bulging control.
- **Stochastic Barycentric Coordinates** [[papers/degoes-2024-stochastic-bary]]: Monte Carlo evaluation of any coordinate type; no volumetric solve needed.

## Key Papers
- [[papers/joshi-2007-harmonic-coords]] — Harmonic Coordinates: non-negative, require volumetric solve
- [[papers/lipman-2008-green-coords]] — Green Coordinates: similarity-invariant, closed-form
- [[papers/chen-2023-somigliana]] — Somigliana Coordinates: elasticity-derived, volume control
- [[papers/degoes-2024-stochastic-bary]] — stochastic evaluation of barycentric coordinates

## Connections
- [[concepts/bounded-biharmonic-weights]] — alternative deformation weights (not cage-based but related spirit)
- [[concepts/linear-blend-skinning]] — alternative deformation paradigm

## Notes
Cages are most useful when:
- The character has complex mesh topology but few natural bone joints.
- Volume-preserving or physically-motivated deformation is needed beyond what LBS provides.
- The same cage drives multiple mesh LODs.

Practical note: Green Coordinates are the most commonly implemented in production tools. Somigliana Coordinates improve volume behavior significantly but require numerical quadrature for evaluation.
