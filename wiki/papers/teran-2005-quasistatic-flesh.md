---
title: "Robust Quasistatic Finite Elements and Flesh Simulation"
authors: [Teran, Joseph; Sifakis, Eftychios; Irving, Geoffrey; Fedkiw, Ron]
venue: SCA 2005 (Symposium on Computer Animation)
year: 2005
tags: [simulation, muscles, volumes]
source: raw/papers/teran-2005-quasistatic-flesh.pdf
---

## Summary
Establishes the FEM flesh simulation engine underlying ILM's production face pipeline. The key contribution is handling **element inversion** (elements that collapse to zero or negative volume during extreme deformations) in quasistatic nonlinear FEM via a modified Newton-Raphson solver and a modified diagonalized constitutive model. Introduced the diagonalized Piola-Kirchhoff stress for invertible elements. The quasistatic formulation (ignoring inertia) is appropriate for slow facial deformations and dramatically reduces the stiffness of the implicit solve. SCA 2005.

## Problem
Standard nonlinear FEM (Neo-Hookean, Mooney-Rivlin) breaks down when elements become inverted during extreme deformation — the constitutive model produces NaN/infinite stresses. Facial tissue undergoes extreme deformation near lips and eyelids. Previous face simulations used spring-mass (Terzopoulos), which lacks a principled material model.

## Method
**FEM discretization:** tetrahedral elements; piecewise linear displacement field.

**Quasistatic formulation:** equilibrium equation (no inertia):
```math
\mathbf{f}_{int}(\mathbf{x}) + \mathbf{f}_{ext} = 0
```
Solved by modified Newton-Raphson (Newton steps + line search).

**Invertible elements:** SVD-based stress diagonalization. Decompose deformation gradient $\mathbf{F} = \mathbf{U} \hat{\mathbf{F}} \mathbf{V}^T$. Clamp singular values to a small positive threshold before evaluating the constitutive model, then reconstruct:
```math
\mathbf{P}(\mathbf{F}) = \mathbf{U} \hat{\mathbf{P}}(\hat{\mathbf{F}}) \mathbf{V}^T
```
This ensures stress is always finite and well-defined even for collapsed elements.

**Material model:** Neo-Hookean (and Mooney-Rivlin variants) with separate parameters for passive tissue (fat, skin) and active muscle fibers.

**Muscle fibers:** transversely isotropic material model; active contraction along fiber direction:
```math
\Psi_{muscle} = \Psi_{passive}(\mathbf{F}) + a \cdot \Psi_{active}(\lambda_f)
```
where $\lambda_f = \sqrt{\mathbf{f}_0^T \mathbf{C} \mathbf{f}_0}$ is the stretch along fiber direction $\mathbf{f}_0$ and $a \in [0,1]$ is activation.

## Key Results
Stable quasistatic FEM simulation of facial flesh under extreme deformations (lip curl, eyelid close). Element inversions handled without simulation blowup. Demonstrated on face models with anatomical muscle geometry from MRI data. Formed the core computational engine for the ILM face pipeline (Sifakis et al. 2005, Cong et al. 2015–2017).

## Limitations
Quasistatic assumption: no secondary dynamics, no jiggle — the face is always at quasi-equilibrium. Computationally expensive per-frame (Newton iterations with large sparse linear solves). Requires volumetric tetrahedral mesh from MRI data (expensive to generate per subject). Material parameters not straightforward to calibrate.

## Connections
- [[papers/sifakis-2005-anatomy-muscles]] — uses this FEM engine for muscle activation recovery
- [[papers/cong-2015-anatomy-pipeline]] — deploys this engine at production scale
- [[papers/ichim-2017-phace]] — modern person-specific physics face; same FEM formulation
- [[papers/smith-2018-neo-hookean]] — improved Neo-Hookean energy with better inversion handling
- [[papers/kadlecek-2019-physics-face-data]] — extends with data-driven material calibration from gravity scans
- [[concepts/neo-hookean-simulation]] — Neo-Hookean flesh model detailed here
- [[concepts/muscles]] — transversely isotropic active muscle fiber model
- [[authors/teran-joseph]]
- [[authors/sifakis-eftychios]]
- [[authors/fedkiw-ronald]]

## Implementation Notes
The SVD-based inversion handling is now standard in all production FEM simulators. The key trick: never evaluate the constitutive model on the raw $\mathbf{F}$; always SVD-decompose, clamp, compute stress in diagonal space, rotate back. The modified Newton-Raphson with line search prevents divergence — if a Newton step increases energy, bisect the step length. Typical convergence: 5–15 Newton iterations per quasistatic solve.
