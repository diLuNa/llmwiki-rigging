---
title: "Sharp Kelvinlets: Elastic Deformations with Cusps and Localized Falloffs"
authors: [de Goes, Fernando; James, Doug L.]
venue: ACM Transactions on Graphics 2019
year: 2019
tags: [sculpting, elasticity, deformation, volumes, math]
source: raw/papers/2019.Others.GJ.pdf
---

## Summary
Extends Regularized Kelvinlets with two new brush families — Bi-Laplacian Kelvinlets and Cusp Bi-Laplacian Kelvinlets — that provide sharp, non-smooth deformation profiles with fast far-field decay, giving artists more control over brush spikiness and locality without multi-scale extrapolation overhead.

## Problem
Standard Regularized Kelvinlets have inherently smooth falloffs (C∞), which limits expressiveness for sharp creases or very localized edits. Multi-scale extrapolation (tri-scale brushes) partially addresses falloff, but is computationally redundant.

## Method
Two new constructions:
1. **Bi-Laplacian Kelvinlets**: apply the Laplacian operator to the Kelvinlet solution, producing faster far-field decay. Allows compact, localized brushes without multi-scale tricks.
2. **Cusp Bi-Laplacian Kelvinlets**: a multi-scale convolution scheme layering Kelvinlet deformations into a finite but spiky profile, enabling cusp-like edits with sharp falloffs.
3. **Sharp Kelvinlets**: combine both — analytic fundamental solutions with independent control over *locality* (how far the influence reaches) and *spikiness* (how sharp the profile peak is).

```math
\mathbf{u}_{\text{sharp}}(\mathbf{x}) = \mathbf{K}_\epsilon(\mathbf{x}) - \alpha\,\Delta\mathbf{K}_\epsilon(\mathbf{x})
```

Closed-form expressions provided for 2D and 3D in both incompressible and compressible cases.

## Key Results
- Sharper, more localized brush edits than tri-scale Kelvinlets.
- Closed-form; maintains real-time performance.
- Blending Bi-Laplacian and Cusp variants gives continuous control over sharpness.

## Limitations
- Still assumes infinite linear elastic medium.
- Cusp profiles can produce non-smooth normal fields if used aggressively.

## Connections
- [[papers/degoes-2018-kelvinlets]] — predecessor; this paper extends it
- [[concepts/kelvinlets]]
- [[authors/degoes-fernando]]
- [[authors/james-doug]]

## Implementation Notes
Reference implementation provided in the paper. The Laplacian applied to a Green's function is a standard biharmonic operation — straightforward to add as a modifier on top of an existing Kelvinlet implementation.
