---
title: "Stochastic Computation of Barycentric Coordinates"
authors: [de Goes, Fernando; Desbrun, Mathieu]
venue: SIGGRAPH 2024
year: 2024
tags: [cage-deformation, math, deformation, volumes]
source: raw/papers/2024.SiggraphPapers.GD.pdf
---

## Summary
A Monte Carlo method for computing barycentric coordinates (harmonic, Green, Somigliana, etc.) directly at query points via proximity queries to the cage, requiring no volumetric discretization, custom solves, or large memory footprints.

## Problem
Computing barycentric coordinates on cages typically requires expensive volumetric meshing or global linear solves. For characters with disconnected components (body + hair + clothes), maintaining a consistent volumetric domain is difficult. Memory cost is prohibitive at high resolution.

## Method
Reformulates the kernel integral defining barycentric coordinates as a **weighted least-squares minimization** amenable to Monte Carlo integration:

```math
\mathbf{u}(\mathbf{x}) \approx \sum_{k=1}^{N} w_k\,\mathbf{u}(\mathbf{y}_k)
```

where $\mathbf{y}_k$ are sampled via proximity queries (closest point, ray intersection) to the cage. Key insight: reformulating as WLS preserves **linear precision** (a fundamental requirement for barycentric coordinates) while enabling unbiased Monte Carlo estimation. A single denoising step removes MC noise post-computation.

## Key Results
- Computed harmonic coordinates on a 30.8k-point character (body + hair + shirt) with 88-vertex cage in 2.9 s (50 samples + 1 denoising step).
- No volumetric discretization or custom linear solve required.
- Works for coordinates evaluated both inside and outside the cage.
- Compatible with harmonic, Green, Somigliana, and other coordinate types.

## Limitations
- Monte Carlo noise; requires denoising for clean results.
- Accuracy scales with sample count (more samples = slower + cleaner).
- Currently evaluated offline; not interactive for large models.

## Connections
- [[papers/chen-2023-somigliana]] — Somigliana coordinates, computable via this method
- [[concepts/cage-deformation]]
- [[concepts/bounded-biharmonic-weights]] — related deformation weights computed via linear solve
- [[authors/degoes-fernando]]
- [[authors/desbrun-mathieu]]

## Quotes
> "Our key insight is a reformulation of the kernel integral defining barycentric coordinates into a weighted least-squares minimization that enables Monte Carlo integration without sacrificing linear precision."
