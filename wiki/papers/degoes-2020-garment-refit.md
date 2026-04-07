---
title: "Garment Refitting for Digital Characters"
authors: [de Goes, Fernando; Fong, Donald; O'Malley, Meredith]
venue: SIGGRAPH Talks 2020
year: 2020
tags: [simulation, deformation, mesh-wrap]
source: raw/papers/2020.SiggraphTalks.GFO.pdf
---

## Summary
A garment refit technique that transfers clothing meshes between characters of different body shapes via an iterative scheme alternating relaxation (using affine-invariant coordinates) and rebinding (resetting garment-to-body spacing). Used in Pixar's *Soul* to transfer garments across diverse characters.

## Problem
Manually refitting garments between characters is time-consuming. A tool needs to adapt 3D garment geometry to a new body shape while preserving the garment's design intent (silhouette, tightness) and handling multi-layer overlaps, seams, and fold-overs.

## Method
Iterative refit loop:
1. **Relaxation step**: deform garment using affine-invariant coordinates (from [[papers/degoes-2019-mesh-wrap]]) to adapt to the target body shape while minimizing mesh distortion.
2. **Rebinding step**: recompute the spacing between garment and body surface according to user-prescribed tightness values, enforcing the desired fit.
Supports multi-layer constraints (layer ordering), seam constraints, and fold-over constraints.

## Key Results
- Successfully transferred hoodie, jeans, pants across adult/teen/kid body types.
- Used in production on *Soul* (2020).
- Handles complex multi-layer garments.

## Limitations
- Convergence speed depends on body shape dissimilarity.
- Tightness parameters require per-garment authoring.

## Connections
- [[papers/degoes-2019-mesh-wrap]] — affine-invariant coordinates used in relaxation step
- [[papers/olmos-2025-cloth-draping]] — later cloth work from same team
- [[authors/degoes-fernando]]

## Implementation Notes
The rebinding step is essentially a closest-point projection with a prescribed offset along the body normal. The alternating relaxation/rebind loop typically converges in 5–20 iterations for moderate body shape differences.
