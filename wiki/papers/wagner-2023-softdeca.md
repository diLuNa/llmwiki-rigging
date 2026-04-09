---
title: "SoftDECA: Soft Physics for Facial Animation"
authors: [Wagner, Nicolas; Ichim, Alexandru Eugen; Beeler, Thabo; Pauly, Mark]
venue: ACM Transactions on Graphics (SIGGRAPH 2023)
year: 2023
tags: [simulation, digital-human, blendshapes, neural, facial-capture]
source: raw/papers/wagner-2023-softdeca.pdf
---

## Summary
**SoftDECA** adds a differentiable soft-body physics layer on top of DECA (a neural 3DMM fitting system). The physical layer models the skin as an elastic shell that deforms due to underlying muscle/bone motion, adding realistic tissue dynamics to the normally quasistatic DECA reconstructions. The method jointly optimizes DECA's shape/expression codes and the physics layer's material parameters from image sequences, producing face reconstructions with plausible secondary dynamics. SIGGRAPH 2023.

## Problem
DECA and other 3DMM fitting methods produce quasistatic, per-frame face reconstructions. Temporal dynamics (secondary skin motion, lag effects) are not modeled. Adding physics as a post-process requires known material parameters and decouples the physics from the appearance fitting.

## Method
**Architecture:**
- **DECA backbone:** encodes image → FLAME parameters (identity $\beta$, expression $\psi$, pose $\theta$)
- **Physical layer:** differentiable elastic shell simulation over FLAME surface; material parameters $(E, \nu, \rho)$ are additional learned parameters
- **Forward model:** FLAME deformation defines the kinematic "target" shape; physics layer computes elastic response of skin shell, adding corrective displacement $\mathbf{u}_{phys}$
- **Total shape:** $\mathbf{x} = \mathbf{x}_{DECA}(\beta, \psi, \theta) + \mathbf{u}_{phys}$

**Differentiability:** elastic shell simulation is differentiable with respect to material parameters (using adjoint method) → can be included in end-to-end gradient optimization from image losses.

**Training:** jointly optimize DECA encoder weights + shell material parameters $(E, \nu, \rho)$ from video sequences using photometric + landmark losses.

## Key Results
Reconstructions with SoftDECA show temporal coherence and secondary skin dynamics not present in vanilla DECA. Material parameters estimated from video are physically reasonable. Demonstrated on in-the-wild video. SIGGRAPH 2023.

## Limitations
Elastic shell is a surface model — no volumetric tissue or subcutaneous fat dynamics. Material parameters are person-shared rather than region-specific. The physics layer adds dynamics but not the full complexity of tissue sliding (no sliding contact with underlying structures). Computational overhead vs. vanilla DECA.

## Connections
- [[papers/feng-2021-deca]] — DECA backbone used here
- [[papers/teran-2005-quasistatic-flesh]] — volumetric FEM alternative (vs. shell model here)
- [[papers/ichim-2017-phace]] — fuller physics face model (same advisor group)
- [[papers/bradley-2017-blendshape-physics]] — earlier: physics on top of blendshapes
- [[papers/kadlecek-2019-physics-face-data]] — material parameter calibration methods
- [[concepts/muscles]] — context: SoftDECA adds tissue dynamics to neural face fitting
- [[concepts/nonlinear-face-models]] — extends DECA (a nonlinear 3DMM) with physics
- [[authors/wagner-nicolas]]
- [[authors/ichim-alexandru]]
- [[authors/beeler-thabo]]
- [[authors/pauly-mark]]
