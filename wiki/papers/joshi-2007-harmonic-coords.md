---
title: "Harmonic Coordinates for Character Articulation"
authors: [Joshi, Pushkar; Meyer, Mark; DeRose, Tony; Green, Brian; Sanocki, Tom]
venue: SIGGRAPH 2007
year: 2007
tags: [cage-deformation, deformation, skinning, math]
source: ~no local pdf~
---

## Summary
Proposes harmonic coordinates as skinning weights for cage-based character deformation. The coordinates are the solution to the Laplace equation inside the cage with boundary conditions set by the cage vertices, guaranteeing non-negativity everywhere inside the cage and smooth, well-behaved deformation.

## Problem
Existing cage deformers (MVC) can produce negative coordinates, leading to artifacts. Skinning weights for character deformation should be non-negative, smooth, and monotone — properties that linear or polynomial interpolation schemes can violate.

## Method
Harmonic coordinates $\phi_j(\mathbf{x})$ are defined as the solution to:

```math
\Delta \phi_j = 0 \quad \text{inside cage}, \qquad \phi_j = \delta_{ij} \quad \text{on cage vertex } i
```

solved via finite elements or boundary element methods on a volumetric discretization. Properties:
- **Non-negative** everywhere inside the cage (maximum principle for harmonic functions).
- **Smooth** (harmonic = minimum variation).
- **Partition of unity** and linear precision.
- Automatically produce localized influence — distant cage handles have diminishing weight.

## Key Results
- Cleaner, artifact-free deformation vs. MVC for complex characters.
- Non-negativity eliminates inverted/folded regions.
- Demonstrated on Pixar-style characters.

## Limitations
- Requires volumetric discretization (tetrahedral mesh or voxel grid) inside the cage — expensive to precompute.
- Resolution-dependent: coarse discretization introduces discretization error.
- No closed-form expression; always requires a solve.

## Connections
- [[papers/lipman-2008-green-coords]] — Green Coordinates: closed-form alternative, similarity-invariant
- [[papers/degoes-2024-stochastic-bary]] — stochastic computation of harmonic coordinates without volumetric solve
- [[papers/jacobson-2011-bbw]] — Bounded Biharmonic Weights: related automatic weight scheme
- [[concepts/cage-deformation]]
- [[concepts/bounded-biharmonic-weights]]
- [[authors/meyer-mark]]
- [[authors/degoes-fernando]] (DeRose is Tony DeRose, Pixar colleague)

## Implementation Notes
The volumetric solve is the main implementation cost. [[papers/degoes-2024-stochastic-bary]] eliminates this by reformulating as Monte Carlo integration — strongly preferred for complex multi-component characters.
