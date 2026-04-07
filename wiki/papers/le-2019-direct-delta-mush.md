---
title: "Direct Delta Mush Skinning and Variants"
authors: [Le, Binh Huy; Lewis, J.P.]
venue: SIGGRAPH 2019
year: 2019
tags: [skinning, lbs, deformation, math]
source: ~no local pdf~
---

## Summary
Reformulates Delta Mush as an equivalent *direct* skinning method with a closed-form set of skinning weights, enabling real-time evaluation without iterative smoothing passes. Provides a theoretical foundation for Delta Mush and several variants with different deformation properties.

## Problem
Delta Mush [[papers/mancewicz-2014-delta-mush]] is computed iteratively (many Laplacian smoothing passes per frame), making it expensive at animation rates on high-resolution meshes. A direct formulation would enable precomputed weights for real-time use.

## Method
Shows that Delta Mush is mathematically equivalent to a skinning method of the form:

```math
\mathbf{p}'_i = \sum_j w_{ij}(\mathbf{p}^0) \, T_j \, \mathbf{p}^0_i
```

where the weights $w_{ij}$ are derived analytically from the Laplacian smoothing operator. Introduces several variants:
- **DDM-v0**: direct reformulation of standard Delta Mush.
- **DDM-v1**: adds per-vertex scale factors for better volume control.
- **DDM-v2**: adds per-vertex rotation for better twist handling.
- **DDM-v3**: full affine variant with best quality, highest cost.

Weights are precomputed at bind time; runtime evaluation is a single matrix-weighted combination — same complexity as LBS.

## Key Results
- Matches Delta Mush quality with orders-of-magnitude speedup at runtime.
- Provides smooth, volume-preserving deformation with no corrective sculpts.
- Variants offer quality/performance tradeoffs.
- Demonstrated on production characters at real-time rates.

## Limitations
- Weights depend on the rest pose mesh — they must be recomputed if the rest pose changes.
- DDM-v2/v3 are more expensive than LBS; DDM-v0/v1 are competitive.
- Like Delta Mush, does not fully replace hand-sculpted correctives for extreme poses.

## Connections
- [[papers/mancewicz-2014-delta-mush]] — the iterative method this reformulates
- [[concepts/linear-blend-skinning]] — same evaluation paradigm, better weights
- [[papers/jacobson-2014-skinning-course]] — survey context
- [[authors/le-binh]]
