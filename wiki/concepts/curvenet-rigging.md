---
title: "Curvenet Rigging"
tags: [rig-generation, deformation, skinning, correctives]
---

## Definition
Curvenet rigging is a character articulation paradigm developed at Pixar in which artists draw and animate sparse 3D *curvenets* — collections of profile curves that outline how the surface should deform — and the system optimizes mesh deformation to match these curves while reconstructing surface detail. The key insight is separating the *articulation controller* (the curvenet) from the *surface representation* (the mesh).

## Variants / Taxonomy
- **Base curvenet rigging** [[papers/degoes-2022-profile-curves]]: core technique; curvenet drives a constrained Laplacian solve for the mesh.
- **Shaping rig** [[papers/nguyen-2023-curvenet-elemental]]: extends curvenet rigging with auto-generated surface-aligned direct manipulators per knot, enabling shot-level fine controls.
- **AutoSplines**: related Pixar tool for spine/tentacle-type appendages (Hessler & Talbot 2016).

## Key Papers
- [[papers/degoes-2022-profile-curves]] — original curvenet rigging formulation
- [[papers/nguyen-2023-curvenet-elemental]] — shaping rig extension; *Elemental* production deployment
- [[papers/singleton-2025-alien-rigs]] — curvenet use on non-humanoid aliens in *Elio*

## Connections
- [[concepts/pose-space-deformation]] — corrective sculpts can complement curvenet rigs
- [[concepts/laplacian-smoothing]] — curvenet solve is a constrained Laplacian problem

## Notes
Curvenet rigging addresses a fundamental pain point: weight painting and corrective sculpting are **indirect** controls — artists manipulate per-vertex numbers to achieve desired shapes, iterating until the implicit relationship between numbers and shape produces the desired result. Curvenet controls are **direct** — artists draw the shape they want.

The constrained Laplacian solve underpinning curvenet deformation:
```math
\min_{\mathbf{p}} \|\mathbf{L}\mathbf{p} - \mathbf{L}\mathbf{p}_0\|^2 \quad \text{s.t.} \quad C(\mathbf{p}) = \mathbf{c}
```
where $\mathbf{L}$ is the Laplacian operator, $\mathbf{p}_0$ is the rest pose, and $C(\mathbf{p}) = \mathbf{c}$ enforces curvenet interpolation constraints.
