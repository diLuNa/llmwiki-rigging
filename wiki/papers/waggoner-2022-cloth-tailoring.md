---
title: "Revamping the Cloth Tailoring Pipeline at Pixar"
authors: [Waggoner, Christine; de Goes, Fernando]
venue: SIGGRAPH Talks 2022
year: 2022
tags: [simulation, deformation, houdini]
source: ~no local pdf~
---

## Summary
Describes Pixar's C3D cloth tailoring system — a 3D-first garment design workflow in which artists directly model garments as 3D meshes (rather than 2D patterns), and C3D auto-generates simulation-ready geometry. Covers system design, authoring workflow, and production lessons from over a decade of use.

## Problem
Traditional cloth simulation uses 2D pattern-based design (like real sewing), which is unfamiliar to 3D artists. A 3D-first workflow lowers the barrier for artists while maintaining production-quality cloth simulation.

## Method
C3D workflow:
- Artist models a low-resolution 3D garment mesh directly (no 2D patterns needed).
- C3D auto-generates: a higher-resolution simulation mesh, UV panels, seam constraints, and layering rules.
- Simulation runs on the generated mesh; results are deformed back to the artist's low-res model.
- Supports multi-layer garments, fold-overs, and tightness controls.

The system has been in production at Pixar for 10+ years across many features.

## Key Results
- 3D-first workflow accessible to any 3D artist.
- Used across multiple Pixar features (*Inside Out 2*, *Elio*, and others).
- Foundation for [[papers/olmos-2025-cloth-draping]] blended-UV draping technique.

## Limitations
- 3D-authored garments lack the pattern-making precision of 2D sewn designs.
- Auto-generated simulation mesh quality depends on artist's 3D mesh topology.

## Connections
- [[papers/olmos-2025-cloth-draping]] — blended UV extension of this pipeline
- [[papers/kim-2022-dynamic-deformables]] — simulation engine running under C3D
- [[authors/degoes-fernando]]
