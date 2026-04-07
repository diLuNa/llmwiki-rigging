---
title: "Projective Dynamics: Fusing Constraint Projections for Fast Simulation"
authors: [Bouaziz, Sofien; Martin, Sebastian; Liu, Tiantian; Kavan, Ladislav; Pauly, Mark]
venue: SIGGRAPH 2014
year: 2014
tags: [simulation, volumes, math, muscles]
source: ~no local pdf~
---

## Summary
Projective Dynamics is an implicit time integration framework for physics simulation that reformulates constraint-based simulation as repeated local projections (cheap, per-element) and a global solve (one sparse linear system per step). Produces stable, fast simulation of cloth, soft bodies, and fluids at interactive rates.

## Problem
Implicit time integration of elastic systems requires expensive Newton iterations with factorized Jacobians per step. Position-based dynamics (PBD) is fast but not physically accurate. A method combining PBD speed with implicit-integration correctness and extensibility was needed.

## Method
Reformulates the implicit integration energy as:

```math
\min_{\mathbf{q}} \frac{1}{2h^2}\|\mathbf{M}^{1/2}(\mathbf{q}-\mathbf{s})\|^2 + \sum_i w_i \|\mathbf{A}_i\mathbf{q} - \mathbf{p}_i\|^2
```

where $\mathbf{p}_i$ are auxiliary variables constrained to a constraint manifold (the "projection"). Minimization alternates:
1. **Local step**: update each $\mathbf{p}_i$ independently (projection onto constraint manifold — cheap, parallel).
2. **Global step**: fix $\mathbf{p}_i$, solve a sparse linear system for $\mathbf{q}$ (system matrix is constant — prefactored once).

Constraints include strain limiting, bending, volume preservation, and contact.

## Key Results
- Stable simulation at interactive rates for cloth, soft bodies.
- System matrix is constant — factorization amortized over all timesteps.
- Easily extensible to new constraint types.
- Widely adopted in research and production (Unity DOTS Physics, etc.).

## Limitations
- Convergence is slow for stiff constraints; requires many iterations for accuracy.
- The constant system matrix means the method approximates full Newton — energy not exactly minimized.
- High-frequency contact and collision still requires dedicated handling.

## Connections
- [[papers/smith-2018-neo-hookean]] — Neo-Hookean energy fits the local-global framework
- [[papers/kim-2022-dynamic-deformables]] — production context; Fizz uses similar ideas
- [[concepts/neo-hookean-simulation]]
- [[authors/kavan-ladislav]]
- [[authors/bouaziz-sofien]]
