---
title: "Elasticity-Inspired Deformers for Character Articulation"
authors: [Kavan, Ladislav; Sorkine, Olga]
venue: ACM Transactions on Graphics 2012
year: 2012
tags: [skinning, lbs, correctives, deformation, math]
source: ~no local pdf~
---

## Summary
Derives corrective deformers grounded in linearized elasticity theory, providing a principled framework for adding physically motivated secondary deformations on top of skeletal animation. The deformers correct LBS artifacts (volume loss, candy-wrapper) using elastic strain energy as the objective rather than ad hoc formulas.

## Problem
LBS artifacts (volume collapse, candy-wrapper at joints) are typically corrected by hand-sculpted pose-space deformations [[concepts/pose-space-deformation]], which require tedious manual authoring. An automatic, physically principled approach would reduce this burden.

## Method
Models the character mesh as a linearly elastic solid. The LBS deformation induces a strain field; the corrective displacement field minimizes the elastic strain energy subject to the skeletal pose constraints. Key steps:
1. Compute the Green–Lagrange strain induced by the LBS deformation at each vertex.
2. Solve for the displacement that minimizes the linearized elastic energy (a Poisson-like system).
3. The result is an elasticity-inspired corrective that runs on top of LBS automatically.

The framework generalizes LBS by adding strain-based correctives without requiring artist sculpting.

## Key Results
- Automatic correctives that reduce candy-wrapper and volume loss at joints.
- Physically principled: corrections derive from the same elasticity framework used in simulation.
- Shown to outperform linear correctives for large joint rotations.

## Limitations
- Linear elasticity assumption breaks down for very large deformations.
- Requires elastic material parameters per-region (or global defaults).
- More expensive than pure LBS; real-time viability depends on mesh resolution.

## Connections
- [[concepts/linear-blend-skinning]] — LBS is the base deformation this corrects
- [[concepts/pose-space-deformation]] — alternative (artist-driven) correction approach
- [[papers/degoes-2018-kelvinlets]] — same elasticity theoretical grounding
- [[authors/kavan-ladislav]]
- [[authors/sorkine-olga]]

## Implementation Notes
The elastic corrective solve is essentially a Laplacian solve weighted by the local strain of the LBS deformation. Can be precomputed per-pose sample and baked into blendshapes for real-time playback.
