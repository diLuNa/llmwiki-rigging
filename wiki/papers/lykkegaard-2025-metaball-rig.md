---
title: "Metaball Madness - The Rigging Of An Implicit Surface Character"
authors: [Lykkegaard, Anna-Christine; Butts, Andrew; Teo, Julian]
venue: SIGGRAPH Talks 2025
year: 2025
tags: [rig-generation, implicit-surfaces, deformation, neural]
source: raw/papers/2025.ooooo_rig.pdf
---

## Summary
Describes the first mesh-free character rig at Pixar, built for OOOOO — a liquid supercomputer in *Elio* (2025). The system rigs a shader (implicit surface) rather than a mesh, using a hierarchical arrangement of implicit surface primitives and operators, while maintaining normal animation paradigms and downstream renderability.

## Problem
OOOOO's design as a liquid/fluid entity requires smooth, topologically-flexible shape changes that are incompatible with a fixed mesh. No production system existed for rigging an implicit surface character that animators could drive with conventional controls.

## Method
Architecture:
- **Implicit surface primitives**: hierarchically arranged metaballs/implicit primitives that can be transformed, blended, and combined via field operators.
- **Field operators**: support complex transformations (merge, subtract, smooth blend) while preserving smooth topology.
- **Rigged shader**: the "mesh" is the zero-level set of the implicit field; rendered directly without explicit tessellation at animation time.
- **Normal animation paradigm**: animators use standard Presto controls (transforms, rig parameters) that drive the implicit primitive hierarchy.
- Downstream renderability ensured via [Luo et al. 2025] implicit surface rendering pipeline.

## Key Results
- First mesh-free production character at Pixar.
- Achieved in *Elio* (2025) for the OOOOO character.
- Animators could work within normal workflows despite underlying implicit representation.

## Limitations
- Relies on a custom implicit surface rendering pipeline.
- Complex shape edits (e.g., sharp features) may require special handling in the implicit framework.
- Limited to characters whose design fits implicit surface representation.

## Connections
- [[papers/singleton-2025-alien-rigs]] — other *Elio* alien rigs
- [[concepts/implicit-surfaces]]
- [[authors/butts-andrew]]

## Implementation Notes
The metaball/implicit surface approach gives naturally smooth blending between body parts — a classic advantage of implicit modeling. For production use, the key engineering challenge is making implicit evaluation fast enough for interactive animation and ensuring the rendering pipeline can handle the resulting signed distance field efficiently.
