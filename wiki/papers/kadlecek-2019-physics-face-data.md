---
title: "Reconstructing Personalized Anatomical Models for Physics-Based Body Animation"
authors: [Kadlecek, Petr; Ichim, Alexandru Eugen; Liu, Tiantian; Kavan, Ladislav; Pauly, Mark]
venue: PACM on Computer Graphics and Interactive Techniques (SIGGRAPH Asia 2017) — extended as PACMCGIT 2(2) 2019
year: 2019
tags: [muscles, simulation, digital-human, facial-capture]
source: raw/papers/kadlecek-2019-physics-face-data.pdf
---

## Summary
Proposes a data-driven approach to **calibrate material parameters** for personalized physics-based face (and body) models. The key insight: scan the same subject in multiple body poses under **gravity** — gravity creates known loading conditions that constrain material properties. EMG sensors simultaneously record muscle activation levels. This provides ground-truth data for fitting both elastic moduli and muscle fiber parameters per subject. Extends Phace (Ichim 2017) from expression-scan fitting to gravity-assisted calibration. PACMCGIT 2(2), 2019.

## Problem
Phace and ILM's anatomy models require material parameters (Neo-Hookean Young's modulus, Poisson ratio, muscle stiffness) but have no principled way to estimate these per-subject. Literature values vary widely across subjects and anatomical regions. Incorrect parameters cause implausible deformations (too stiff, too rubbery) or quantitatively wrong shape changes.

## Method
**Data acquisition:**
1. Subject scanned in $N$ poses under varying gravitational loading (e.g., face up, face down, tilted) → gravity deforms tissue differently at each orientation
2. EMG sensors on face muscles → ground-truth activation levels $a_k^{gt}$ during static holds
3. Result: pairs of (scan geometry, muscle activation) under known external loading

**Material calibration:**
```math
\min_{\boldsymbol{\theta}} \sum_{n=1}^N \| \mathbf{x}_{sim}(\mathbf{a}_n^{gt}, \boldsymbol{\theta}, \mathbf{g}_n) - \mathbf{x}_{scan_n} \|^2 + \lambda R(\boldsymbol{\theta})
```
where $\mathbf{g}_n$ is gravity direction for pose $n$. Optimize via gradient descent; Jacobian $\partial \mathbf{x}_{sim}/\partial \boldsymbol{\theta}$ computed by differentiating through the quasistatic FEM solve.

**Parameters calibrated per anatomical region:** separate Young's modulus for cheek fat, lip tissue, forehead skin, chin; separate muscle stiffness per muscle group.

**Body extension:** same methodology applied to body (torso, limbs) with gravity-varied poses.

## Key Results
Material parameters calibrated with gravity data produce significantly better match to unseen expression scans (not in training set) than literature-value parameters. Demonstrated 15–30% lower surface error vs. manually-set material parameters. EMG-constrained activations prevent overfitting. PACMCGIT 2(2), 2019.

## Limitations
Requires specialized data acquisition: gravity-varied scanning rig + synchronized EMG. Number of EMG sensors is limited (typically 10–30 surface electrodes vs. hundreds of muscles in the model). Some muscle groups remain uncalibrated. Gravity loading differentiates tissue stiffness but cannot fully disambiguate Poisson ratio from Young's modulus (need combined loading conditions).

## Connections
- [[papers/ichim-2017-phace]] — direct predecessor; Phace model used here
- [[papers/teran-2005-quasistatic-flesh]] — FEM engine for forward simulation
- [[papers/cong-2015-anatomy-pipeline]] — ILM anatomy models would benefit from this calibration
- [[papers/chandran-2024-anatomically-constrained-face]] — Disney Research follows up with implicit model and similar data-driven fitting
- [[concepts/muscles]] — per-subject material calibration for physics face models
- [[authors/kadlecek-petr]]
- [[authors/ichim-alexandru]]
- [[authors/kavan-ladislav]]
- [[authors/pauly-mark]]

## Implementation Notes
The key implementation challenge is differentiating through the quasistatic solve to get the material parameter Jacobian. This requires an adjoint sensitivity method: solve the forward system, then solve an adjoint linear system with the same stiffness matrix to get the gradient efficiently. The gravity-variation approach is clever: gravity is a known external force, so no instrumented loading device is needed — just a rotating couch/chair that changes subject orientation relative to gravity.
