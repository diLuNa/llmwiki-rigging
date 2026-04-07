---
title: "Sculpt Processing for Character Rigging"
authors: [de Goes, Fernando; Coleman, Patrick; Comet, Michael; Martinez, Alonso]
venue: SIGGRAPH Talks 2020
year: 2020
tags: [correctives, smoothing, sculpt-transfer, bandage, bi-laplacian, houdini]
source: raw/papers/2020.SiggraphTalks.GCCM.pdf
---

## Summary
Introduces a suite of geometric operations for processing sculptor-authored corrective shapes: sculpt transfer (moving a delta from one pose to another), bandage smoothing (bi-Laplacian relaxation on a local patch), and rest-aware relaxation. Targets production character rigging workflows.

## Problem
When riggers sculpt correctives, they typically do so at the rest pose and must manually re-pose and adjust the delta for every target pose. Existing smoothing operators don't respect the local rest-pose geometry.

## Method

### Sculpt Transfer
Given a delta sculpted at pose A, transfer to pose B by applying delta to rest mesh, deforming into pose B, comparing to unmodified pose B mesh. The residual is the transferred delta. Must account for how the rig's Jacobian changes between poses.

### Bandage Smoothing
A bi-Laplacian operator constrained to a user-specified vertex patch. Minimizes the energy $\|L^2 \delta\|^2$ subject to boundary constraints.

### Rest-Aware Relaxation
Extends bandage smoothing to penalize deviation from rest-pose shape, preventing correctives from erasing rest-pose detail.

## Key Results
Visually cleaner correctives, less manual iteration vs hand-smoothing. VEX-implementable.

## Limitations
- Transfer quality degrades at extreme pose differences.
- Bandage boundary selection is manual.

## Connections
- [[concepts/laplacian-smoothing]]
- [[concepts/pose-space-deformation]]
- [[concepts/blendshapes]]
- [[authors/degoes-fernando]]

## Implementation Notes
VEX HDA was built covering sculpt transfer, bandage smoothing, and rest-aware relaxation. Bi-Laplacian solved via iterative Gauss-Seidel relaxation in VEX.
