---
title: "Crafting Expressive, Non-Humanoid Alien Characters"
authors: [Singleton, Kevin; Dwek, Daniela; Aydogdu, Ozgur; Muscarella, Anthony]
venue: SIGGRAPH Talks 2025
year: 2025
tags: [rig-generation, skinning, deformation, correctives]
source: raw/papers/2025.SiggraphTalks.SDAM.pdf
---

## Summary
Production talk from *Elio* (Pixar, 2025) describing rig and topology innovations for non-humanoid alien characters with unconventional anatomies (limbless, multi-segmented, fluid forms), using curvenet rigs, AutoSplines, and custom deformers in Pixar's Presto.

## Problem
Non-humanoid characters with unique physiologies (blanket wings, multi-segment bodies, fluid shapes) don't map to standard humanoid rigging assumptions. Conventional bone-and-weight approaches produce unacceptable results for extreme non-standard anatomy.

## Method
Character-specific innovations using Pixar's Presto toolkit:
- **Ambassador Questa** (marine flatworm): hierarchical blanket-wing rig with curvenet controls for the expressive wing membrane.
- **AutoSplines** [[Hessler & Talbot 2016]]: for segmented/tentacle-like appendages.
- **CurveNets** ([[papers/degoes-2022-profile-curves]], [[papers/nguyen-2023-curvenet-elemental]]): for fluid surface control on unusual anatomies.
- **Tooth-sliding mouth** [[Speirs et al. 2024]]: adapted for non-humanoid face shapes.
- Collaborative Animation+Characters workflow: early previs models in Maya/ZBrush to validate articulation before committing to final rigs.

## Key Results
- Rigged full alien cast of *Elio* with unique per-character rig approaches.
- Production-validated on the theatrical release.
- Modular rig architecture enables creative iteration without full rig rebuilds.

## Limitations
- Highly character-specific; limited transferable methodology beyond toolkit selection.

## Connections
- [[papers/degoes-2022-profile-curves]] — curvenet rigging used extensively
- [[papers/nguyen-2023-curvenet-elemental]] — curvenet production tools
- [[papers/lykkegaard-2025-metaball-rig]] — OOOOO (Elio) mesh-free rig, same film
- [[papers/hoffman-2024-insideout2-rig]] — prior Pixar rig challenges talk
- [[concepts/curvenet-rigging]]
- [[authors/singleton-kevin]]
