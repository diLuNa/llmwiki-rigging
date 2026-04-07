---
title: "Stable Neo-Hookean Flesh Simulation"
authors: [Smith, Breannan; de Goes, Fernando; Kim, Theodore]
venue: SIGGRAPH 2018
year: 2018
tags: [simulation, muscles, volumes, math]
source: raw/papers/2018.SiggraphPapers.SGK.b.pdf
---

## Summary
Presents a reformulated Neo-Hookean hyperelastic model that robustly preserves volume at Poisson's ratios near 1/2, is stable under extreme rotations and inversions, and converges faster than co-rotational elasticity. Used in Pixar's Fizz simulator for flesh and cloth.

## Problem
Real biological tissue has Poisson's ratio $\nu \approx 0.5$ (near-incompressible). Standard Neo-Hookean formulations become numerically unstable in this regime; co-rotational elasticity fails to preserve volume and produces spurious folds. Inversion robustness is required for production.

## Method
Decouples the volumetric and deviatoric components of the Neo-Hookean energy into a form that admits closed-form eigendecomposition of the force gradient. Key innovations:
- New stable formulation of the volumetric term $\Psi_V = \frac{\mu}{2}(J-1-\frac{\mu}{2\lambda})^2$ (approximate) that avoids the log singularity.
- Closed-form expressions for the 3×3 and 9×9 Hessians of $\Psi$.
- Analytically guaranteed positive semi-definite projected Hessian for Newton's method.

```math
\Psi(\mathbf{F}) = \frac{\mu}{2}(\text{tr}(\mathbf{F}^T\mathbf{F}) - 3) - \mu\ln J + \frac{\lambda}{2}(J-1)^2
```

## Key Results
- Superior volume preservation vs. co-rotational at $\nu = 0.488$.
- 2× faster convergence (fewer Newton/CG iterations) than co-rotational on a 45k-element skeletal character.
- Robust under large rotations and element inversions.

## Limitations
- Quasistatic regime emphasis; dynamic formulation requires additional time integration considerations.
- The simplified volumetric term introduces a mild approximation relative to exact Neo-Hookean.

## Connections
- [[papers/kim-2022-dynamic-deformables]] — course that builds on this formulation
- [[concepts/neo-hookean-simulation]]
- [[authors/smith-breannan]]
- [[authors/degoes-fernando]]
- [[authors/kim-theodore]]

## Implementation Notes
The closed-form Hessian eigendecomposition is the central implementation payoff: no numerical finite differences needed. The Pixar course (2022.SiggraphCourses.KE.pdf) provides C++ reference code for this model.

## Quotes
> "Our model maintains the fleshy appearance of the Neo-Hookean model, exhibits superior volume preservation, and is robust to extreme kinematic rotations and inversions."
