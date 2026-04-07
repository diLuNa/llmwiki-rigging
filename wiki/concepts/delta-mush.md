---
title: "Delta Mush"
tags: [skinning, smoothing, deformation, lbs, correctives]
---

## Definition
Delta Mush is a deformation operator that smooths a base deformation (typically LBS) to remove artifacts, then restores original surface detail by adding back the rest-pose delta in the local frame of the smoothed surface. The key insight is separating *smooth shape* (from iterative Laplacian relaxation) from *surface detail* (from the rest-pose delta offset).

Per-frame evaluation:
1. Smooth the deformed mesh using $n$ iterations of Laplacian relaxation → produces a smooth base $\bar{\mathbf{p}}'$.
2. For each vertex $i$, compute rest-pose delta $\delta_i = \mathbf{p}^0_i - \bar{\mathbf{p}}^0_i$ in the local tangent frame.
3. Apply $\delta_i$ in the local tangent frame of $\bar{\mathbf{p}}'_i$ to recover the detailed result.

## Variants / Taxonomy
- **Original Delta Mush** [[papers/mancewicz-2014-delta-mush]]: iterative, per-frame Laplacian smoothing + delta reapply.
- **Direct Delta Mush (DDM)** [[papers/le-2019-direct-delta-mush]]: closed-form equivalent as a direct skinning method with precomputed weights. Several subvariants (v0–v3) offering quality/performance tradeoffs.

## Key Papers
- [[papers/mancewicz-2014-delta-mush]] — original formulation; production deployment at ILM
- [[papers/le-2019-direct-delta-mush]] — theoretical reformulation as direct skinning; real-time weights

## Connections
- [[concepts/linear-blend-skinning]] — the base deformation being corrected
- [[concepts/laplacian-smoothing]] — the operator used in the smooth step
- [[concepts/pose-space-deformation]] — alternative (sculpt-based) correction approach

## Notes
Delta Mush is the most widely deployed automatic skinning correction in production. It is a standard node in Maya (`deltaMush`), Houdini (`Delta Mush SOP`), and other DCCs.

Key tuning parameters:
- **Smooth iterations** (20–200): more iterations → smoother base, slower runtime.
- **Smooth amount** (0–1): blend between smoothed and original.
- **Envelope/mask**: per-vertex weight controlling how much Delta Mush is applied.

Practical tip: Delta Mush works best when the base LBS is already reasonable. It corrects candy-wrapper and bulge artifacts but cannot fix fundamentally wrong skinning weights.
