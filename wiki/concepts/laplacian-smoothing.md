---
title: "Laplacian Smoothing"
tags: [smoothing, laplacian, math, geometry]
---

## Definition
The discrete mesh Laplacian $L$ maps each vertex to a weighted average of its neighbors minus itself. Applying it repeatedly smooths a mesh by diffusing high-frequency detail.

## Variants

### Uniform Laplacian
Weights all neighbors equally: $L v_i = \frac{1}{|N_i|} \sum_{j \in N_i} v_j - v_i$. Simple but geometry-unaware; produces poor results on irregular meshes.

### Cotangent Laplacian
Weights by cotangent of opposite angles: $L v_i = \sum_{j \in N_i} (\cot \alpha_{ij} + \cot \beta_{ij})(v_j - v_i)$. Geometrically correct discrete Laplace-Beltrami operator.

### Bi-Laplacian ($L^2$)
Applying the Laplacian twice: $\Delta^2 = L \cdot L$. Produces smoother results than $L$ alone. Used in [[papers/degoes-2020-sculpt]] for bandage smoothing.

## Key Papers
- [[papers/degoes-2020-sculpt]] — bi-Laplacian for corrective shape smoothing
- [[papers/jacobson-2011-bbw]] — cotangent Laplacian as energy for weight optimization

## Connections
- [[concepts/bounded-biharmonic-weights]]

## Notes
In VEX, the cotangent Laplacian requires computing per-halfedge cotangent weights from triangle geometry. Iterative relaxation (Gauss-Seidel) is a practical approximation for real-time or interactive use.
