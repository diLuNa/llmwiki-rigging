---
title: "Smoothing Operators — Comparison"
---

| Operator | Smoothness | Volume preservation | Geometry-aware | Cost |
|----------|-----------|---------------------|----------------|------|
| Uniform Laplacian ($L$) | Low | ❌ shrinks | ❌ | Low |
| Cotangent Laplacian | Medium | ⚠️ | ✅ | Medium |
| Bi-Laplacian ($L^2$) | High (fair) | ⚠️ | ✅ (with cotangent) | Medium+ |
| Mean curvature flow | High | ❌ | ✅ | High |

## For Corrective Shapes
The bi-Laplacian with cotangent weights (as in [[papers/degoes-2020-sculpt]]) is the best choice: smooth, fair, geometry-aware, and implementable via iterative relaxation in VEX.

## Related
- [[concepts/laplacian-smoothing]]
