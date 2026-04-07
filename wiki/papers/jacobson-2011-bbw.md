---
title: "Bounded Biharmonic Weights for Real-Time Deformation"
authors: [Jacobson, Alec; Baran, Ilya; Popović, Jovan; Sorkine, Olga]
venue: SIGGRAPH 2011
year: 2011
tags: [skinning, math, weights, biharmonic, bounded, laplacian]
source: raw/papers/jacobson-2011-bbw.pdf
---

## Summary
Computes smooth, bounded skinning weights by minimizing biharmonic energy subject to non-negativity and partition-of-unity constraints.

## Problem
Computing good skinning weights from a skeleton is hard. Manual painting doesn't scale; harmonic weights can violate boundedness.

## Method
Solve a constrained QP: minimize $\|LW\|^2$ where $L$ is the cotangent Laplacian, subject to $W \geq 0$, $\sum W = 1$, $W|_{handles} = I$.

## Limitations
- Offline solver — not real-time weight computation.
- Requires well-tessellated input mesh.

## Connections
- [[concepts/bounded-biharmonic-weights]]
- [[concepts/laplacian-smoothing]]
- [[concepts/linear-blend-skinning]]
- [[authors/jacobson-alec]]

## Implementation Notes
libigl has reference C++ implementation. Cotangent Laplacian is critical — uniform Laplacian gives poor results.
