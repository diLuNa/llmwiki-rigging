---
title: "Character Articulation through Profile Curves"
authors: [de Goes, Fernando; Sheffler, William; Fleischer, Kurt]
venue: SIGGRAPH 2022
year: 2022
tags: [rig-generation, deformation, correctives, skinning]
source: raw/papers/2022.SiggraphPapers.GSF.pdf
---

## Summary
Introduces *curvenet rigging* — a new character articulation paradigm in which artists draw sparse 3D curves (curvenets) that profile the deforming surface, and the system optimizes mesh deformation to match these profile curves while reconstructing surface details. Replaces the repetitive weight-painting and corrective sculpting workflow.

## Problem
Conventional skinning + corrective sculpt workflows require laborious, indirect authoring: artists set joint weights on thousands of vertices and hand-sculpt correctives one pose at a time. The controls (weights, blend targets) don't directly express the desired surface shape.

## Method
**Curvenet rigging** workflow:
1. Artist draws and animates sparse *curvenets* — collections of 3D profile curves that outline how the surface should deform.
2. System analyzes curvenet layout to quantify deformation along each curve, independent of mesh connectivity.
3. Mesh deformation is computed by solving an optimization that reconstructs surface detail while interpolating the profile curves.

The optimization separates articulation control (curvenet) from surface representation (mesh), allowing the same curvenets to drive different mesh resolutions.

```math
\min_{\mathbf{p}} \|\mathbf{L}\mathbf{p} - \mathbf{L}\mathbf{p}_0\|^2 \quad \text{s.t.} \quad C(\mathbf{p}) = \mathbf{c}
```

where $C$ enforces interpolation of curvenet positions.

## Key Results
- Produced *Profile Mover* tool used on a Panda character.
- Single curvenet drives all mesh detail without per-vertex weight authoring.
- Separation of articulation and mesh resolution enables LOD support.

## Limitations
- Curve placement and animation is a new authoring skill for riggers.
- Reconstruction quality depends on curvenet density vs. surface detail frequency.

## Connections
- [[papers/nguyen-2023-curvenet-elemental]] — production deployment of this system on *Elemental*
- [[papers/singleton-2025-alien-rigs]] — further curvenet use on *Elio*
- [[concepts/curvenet-rigging]]
- [[authors/degoes-fernando]]
- [[authors/sheffler-william]]
- [[authors/fleischer-kurt]]

## Implementation Notes
Curvenet constraints turn this into a constrained Laplacian smoothing solve. The key insight is separating articulation from detail: animate the coarse curvenet profile, then reconstruct the fine mesh. Similar in spirit to cage deformation but using open curves rather than a closed cage.
