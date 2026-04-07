---
title: "Directing Cloth Draping through Blended UVs"
authors: [Olmos Guerra, Juan Carlos; de Goes, Fernando; Waggoner, Christine; Eberle, David]
venue: SIGGRAPH Talks 2025
year: 2025
tags: [simulation, deformation, usd, houdini]
source: raw/papers/2025.SiggraphTalks.CdGWE.pdf
---

## Summary
A cloth draping direction technique that reconciles stylized 3D garment shapes with physically-based simulation by generating custom UVs that blend 3D shape distortion into 2D fabric panels, retargeting the simulation to smoothly transition between prescribed 3D forms and physically plausible draping. Used on *Inside Out 2* and *Elio*.

## Problem
In stylized animation, artists want garments with clean silhouettes and prescribed 3D structure (e.g., a perfectly flat collar). Physical cloth simulation produces folds and draping that conflict with art direction. Choosing one destroys the other.

## Method
Key contribution: **UV blending** that encodes the distortion required to transition a garment from its 2D flat panel to a prescribed 3D form. Specifically:
- A flattening tool constructs low-resolution UV panels from the 3D garment shape.
- These UVs are blended to encode how much the 2D fabric must distort to reach the 3D target form.
- Cloth simulation uses the blended UVs as the rest configuration, producing physical draping that smoothly converges to the prescribed 3D shape.
- Pixar's C3D (3D cloth tailoring system, in use for 10+ years) provides the cloth infrastructure.

## Key Results
- Demonstrated on garment assets and animations from *Inside Out 2* (2024) and *Elio* (2025).
- Reconciles stylized 3D form and physical draping within one simulation.

## Limitations
- Requires authoring 3D target shapes per garment.
- UV blending may not capture all draping detail for complex cuts.

## Connections
- [[papers/degoes-2020-garment-refit]] — earlier garment-fitting work from de Goes
- [[papers/kim-2022-dynamic-deformables]] — cloth simulation infrastructure context
- [[authors/degoes-fernando]]

## Implementation Notes
The core idea is using a non-trivially-flat rest UV as input to the cloth solver — the simulation "wants" to flatten the UV but the 3D shape constraint pulls it toward the prescribed form. This is analogous to setting a desired strain field in FEM.
