---
title: "Bounded Biharmonic Weights (BBW)"
tags: [skinning, weights, biharmonic, bounded, math]
---

## Definition
Skinning weights computed by minimizing biharmonic energy subject to non-negativity and partition-of-unity constraints. Produces smooth, bounded weights with approximately local support.

## Energy
```math
\min_{W} \sum_j \|\Delta W_j\|^2 \quad \text{s.t.} \quad W \geq 0,\ \mathbf{1}^T W = 1
```
where $\Delta$ is the cotangent Laplacian.

## Key Papers
- [[papers/jacobson-2011-bbw]] — original paper

## Connections
- [[concepts/laplacian-smoothing]]
- [[concepts/linear-blend-skinning]]
