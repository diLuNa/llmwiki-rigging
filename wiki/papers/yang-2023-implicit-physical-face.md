---
title: "Implicit Physical Face Model"
authors: [Yang, Lingchen; Chandran, Prashanth; Zoss, Gaspard; Beeler, Thabo; Gotardo, Paulo; Bradley, Derek]
venue: ACM Transactions on Graphics (SIGGRAPH 2023)
year: 2023
tags: [muscles, simulation, digital-human, neural]
source: knowledge
---

## Summary
Introduces an **implicit neural representation** for a physically-based face model — replacing the explicit volumetric tetrahedral mesh with a continuous neural field. The implicit model encodes both the geometry and the elastic material properties as functions of a latent code and muscle activations. Forward simulation becomes neural network evaluation, enabling differentiable physics and fast generation of face poses under muscle control. Disney Research Zürich. SIGGRAPH 2023.

## Problem
Explicit FEM-based face models (Teran 2005, Ichim 2017, Kadlecek 2019) require a fixed tetrahedral mesh per subject, expensive manual or MRI-based construction, and slow per-frame FEM solves. An implicit representation would allow: resolution-free geometry, arbitrary topology changes, and faster amortized inference via neural network evaluation.

## Method
**Implicit representation:**
- Face geometry encoded as a continuous signed distance function $f_\theta: \mathbb{R}^3 \times \mathcal{Z} \times \mathcal{A} \to \mathbb{R}$, where $\mathcal{Z}$ is identity latent code, $\mathcal{A}$ is muscle activation space
- Material properties encoded as a field over the implicit volume: $E_\theta(\mathbf{x}), \nu_\theta(\mathbf{x})$ (Young's modulus, Poisson ratio)

**Training:** learn the neural fields by fitting to a dataset of expression scans and corresponding physics simulations (generated offline with FEM). The implicit model learns to predict the deformed shape given activations, amortizing the FEM cost.

**Physics consistency:** the implicit model is regularized by an elastic energy term: deformation from neutral to activated state must satisfy approximate FEM equilibrium. This ensures physical plausibility rather than pure data interpolation.

## Key Results
Demonstrated on real subjects. Neural implicit forward model runs orders of magnitude faster than explicit FEM. Captures tissue bulging, sliding, and wrinkling (emergent from trained energy). Can generate novel expression poses not in the training set via smooth interpolation in activation space. SIGGRAPH 2023.

## Limitations
Training requires a large corpus of FEM simulation data (expensive to generate). Implicit representation makes it hard to integrate with production rigs (no explicit mesh). Temporal dynamics not captured (quasistatic equivalent). Identity generalization (to new subjects) requires new training or fine-tuning.

## Connections
- [[papers/teran-2005-quasistatic-flesh]] — FEM engine providing training supervision
- [[papers/ichim-2017-phace]] — explicit physics face model this implicitizes
- [[papers/kadlecek-2019-physics-face-data]] — material calibration for the training data
- [[papers/yang-2024-generalized-physical-face]] — direct follow-up generalizing this approach
- [[papers/chandran-2024-anatomically-constrained-face]] — parallel Disney Research work with explicit anatomical constraints
- [[papers/zoss-2020-secondary-dynamics-capture]] — same group; secondary dynamics capture
- [[concepts/muscles]] — implicit neural face with muscle activation control
- [[concepts/implicit-surfaces]] — SDF representation extended to physics
- [[authors/yang-lingchen]]
- [[authors/chandran-prashanth]]
- [[authors/beeler-thabo]]
