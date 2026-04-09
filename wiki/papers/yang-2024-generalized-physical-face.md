---
title: "Generalized Implicit Physical Face Model"
authors: [Yang, Lingchen; Chandran, Prashanth; Zoss, Gaspard; Beeler, Thabo; Gotardo, Paulo; Bradley, Derek]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [muscles, simulation, digital-human, neural]
source: raw/papers/yang-2024-generalized-physical-face.pdf
---

## Summary
Extends the **Implicit Physical Face Model** (Yang et al. 2023) to generalize across multiple identities and support physics-based style transfer between subjects. The generalized model learns a shared implicit neural face model over a population of subjects, conditioned on identity latent codes, muscle activations, and material property codes. A new identity can be embedded in the latent space from a small number of expression scans. Disney Research Zürich. SIGGRAPH 2024.

## Problem
The 2023 implicit physical face model was subject-specific: a separate model per person. This requires significant data (expression scans + FEM simulations) per subject and cannot generalize across people. A population model would enable: few-shot adaptation to new subjects, physics-based identity interpolation, and material style transfer.

## Method
**Generalized model:**
- Identity latent code $\mathbf{z}_{id} \in \mathbb{R}^d$ encodes subject-specific geometry and material properties
- Shared neural network $f_\theta(\mathbf{x}, \mathbf{z}_{id}, \mathbf{a})$ predicts deformed SDF and material field for any identity and activation
- Trained on a dataset of multiple subjects, each with expression scans and FEM simulations

**Few-shot adaptation:** given 5–20 scans of a new subject, optimize $\mathbf{z}_{id}$ to match the scans while keeping network weights frozen. Physics consistency maintained through the trained energy regularizer.

**Material style transfer:** swap $\mathbf{z}_{material}$ from subject A with subject B's geometry code $\mathbf{z}_{shape}$ — generates hybrid face with B's shape deforming with A's material stiffness.

## Key Results
Generalizes to new subjects from 5–20 scans. Material style transfer produces compelling identity-crossing animations. Faster identity embedding than from-scratch model fitting. Competitive surface error with per-subject models. SIGGRAPH 2024.

## Limitations
Population model requires large training dataset (multiple subjects × many expression scans × FEM simulation cost). Implicit representation still requires mesh extraction (marching cubes) for production integration. No direct handling of contact/collision between face and external objects (e.g., glasses, hands touching face).

## Connections
- [[papers/yang-2023-implicit-physical-face]] — direct predecessor (per-subject model)
- [[papers/chandran-2024-anatomically-constrained-face]] — parallel Disney Research: explicit anatomical constraints
- [[papers/zoss-2020-secondary-dynamics-capture]] — same group; secondary dynamics
- [[papers/ichim-2017-phace]] — explicit physics face; same goals, different representation
- [[papers/kadlecek-2019-physics-face-data]] — material parameter data that informs training
- [[concepts/muscles]] — generalized implicit muscle-driven face model
- [[concepts/implicit-surfaces]] — SDF-based face representation
- [[authors/yang-lingchen]]
- [[authors/chandran-prashanth]]
- [[authors/beeler-thabo]]
