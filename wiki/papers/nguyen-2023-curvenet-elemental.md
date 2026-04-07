---
title: "Shaping the Elements: Curvenet Animation Controls in Pixar's Elemental"
authors: [Nguyen, Duc; Talbot, Jeremie; Sheffler, William; Hessler, Mark; Fleischer, Kurt; de Goes, Fernando]
venue: SIGGRAPH Talks 2023
year: 2023
tags: [rig-generation, deformation, correctives]
source: raw/papers/2023.SiggraphTalks.NTSHFG.pdf
---

## Summary
Production deployment of curvenet rigging on *Elemental* (Pixar, 2023). Introduces a *shaping rig* layer that auto-generates surface-aligned direct manipulators per curvenet knot, enabling shot-level fine animation controls on top of the base curvenet deformation system.

## Problem
Curvenet rigging [[papers/degoes-2022-profile-curves]] provides powerful base deformation but lacks direct knot-level animation controls for shot-level polish. Artists need manipulators that move naturally with the deforming surface without manual setup per character.

## Method
Extends curvenet rigging with a **shaping rig**:
- Auto-generates a surface-aligned direct manipulator (transform control) at each curvenet knot.
- Manipulators are defined relative to the deforming surface frame (not world space), so they naturally follow the character.
- Minimal setup: one-click auto-generation from the base curvenet rig.
- Results in a clean mapping from animation controls → curvenet adjustments → mesh deformation.

Applied to Wade (the water character) in *Elemental* for face, lips, eyes, and hair articulation.

## Key Results
- Enabled fine art-directable surface control on a non-humanoid (water/fluid) character.
- Demonstrated across head, lips, eyes, and hair curvenet regions.
- Minimal additional setup cost over base curvenet system.

## Limitations
- Manipulators are relative to surface frame; artists accustomed to world-space controls need adjustment.
- Still requires base curvenet authoring.

## Connections
- [[papers/degoes-2022-profile-curves]] — the base curvenet rigging system this extends
- [[papers/singleton-2025-alien-rigs]] — further curvenet use on *Elio*
- [[concepts/curvenet-rigging]]
- [[authors/degoes-fernando]]
- [[authors/fleischer-kurt]]
- [[authors/sheffler-william]]
