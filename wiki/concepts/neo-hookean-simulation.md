---
title: "Neo-Hookean Flesh Simulation"
tags: [simulation, muscles, volumes, math]
---

## Definition
Neo-Hookean elasticity is a hyperelastic material model that captures the nonlinear stress-strain behavior of soft biological tissue. The strain energy density is:

```math
\Psi(\mathbf{F}) = \frac{\mu}{2}(\text{tr}(\mathbf{F}^T\mathbf{F}) - 3) - \mu\ln J + \frac{\lambda}{2}(J-1)^2
```

where $\mathbf{F}$ is the deformation gradient, $J = \det(\mathbf{F})$, and $(\mu, \lambda)$ are Lamé parameters. For biological tissue, $\lambda \gg \mu$ (Poisson ratio $\nu \to 0.5$, near-incompressible).

## Variants / Taxonomy
- **Classical Neo-Hookean**: log-based volumetric term; unstable at $J \to 0$ (inversions); poor convergence near incompressibility.
- **Co-rotational elasticity**: separates rotation from deformation; fails to preserve volume; not Neo-Hookean.
- **Stable Neo-Hookean** [[papers/smith-2018-neo-hookean]]: replaces log term with a polynomial approximation; admits closed-form eigendecomposition of the Hessian; robust to inversions and extreme rotations.

## Key Papers
- [[papers/smith-2018-neo-hookean]] — Stable Neo-Hookean formulation used in Pixar's Fizz
- [[papers/kim-2022-dynamic-deformables]] — production implementation guide with C++ code
- [[papers/james-2020-phong-deformation]] — embedded deformation technique for visualizing simulated tet meshes
- [[papers/pfaff-2021-meshgraphnets]] — learns neo-Hookean and co-rotational FEM dynamics as a mesh GNN surrogate

## Connections
- [[concepts/laplacian-smoothing]] — mesh-processing operators used in cleanup post-simulation

## Notes
For production character simulation, the key practical properties of Stable Neo-Hookean are:
1. Robust to element inversion (characters in extreme poses can invert tets).
2. Near-incompressible regime ($\nu = 0.48$–$0.499$) is stable.
3. Hessian eigendecomposition is closed-form → fast projected Newton convergence.

Implementation reference: [[papers/kim-2022-dynamic-deformables]] course notes with open-source C++.
