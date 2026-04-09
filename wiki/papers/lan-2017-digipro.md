---
title: "Physics-Based Facial Animation at DreamWorks Animation"
authors: [Lan, Lana; Prasso, Luca; Achorn, Brian; Meredith, Michael]
venue: DigiPro 2017
year: 2017
tags: [muscles, simulation, blendshapes, digital-human]
source: knowledge
---

## Summary
Studio presentation from DreamWorks Animation describing their production approach to physics-informed facial animation. Details how DWA's existing FACS blendshape rigs are augmented with physics-based secondary dynamics and how muscle-simulation-derived shapes inform sculpted blendshape targets. Covers the practical workflow for integrating physical effects into animation at feature film production scale without requiring real-time simulation. DigiPro 2017.

## Problem
DreamWorks Animation needed to add physical realism (soft-tissue jiggle, skin sliding, fat-layer dynamics) to their established FACS blendshape rig workflow without breaking the existing animation pipeline or requiring artists to work with physics simulations directly.

## Method
**Workflow approach:**
- Physics simulation runs offline as a **post-process** on top of approved animation curves
- Secondary dynamics (skin jiggle, lip/cheek soft-tissue lag) extracted via quasi-static or dynamic FEM simulation and stored as corrective animation layers
- Muscle-inspired blendshape targets: key expression shapes sculpted with awareness of anatomical muscle pull directions (informed by Waters/Terzopoulos models) to produce more natural deformations
- Integration with DWA's proprietary face rig (descendant of PDI/DreamWorks muscle+blendshape approach from *ANTZ* era)

**PDI/DWA lineage:** DreamWorks Animation's facial pipeline descends from PDI's work (Bhat et al. 1999, Modesto 2014), which used explicit muscle fiber curves as low-level controls under blendshape targets. This approach continues: muscle curves define the deformation direction, blendshapes capture the result.

## Key Results
Deployed on DreamWorks feature films. Demonstrated improvement in skin dynamics realism. DigiPro 2017 presentation.

## Limitations
Secondary dynamics as a post-process cannot interact with animation cloth or hair simulation. Muscle-inspired sculpting is an art direction practice, not a simulation — cannot generalize to arbitrary new expressions. Not fully automatic.

## Connections
- [[papers/pdi-1998-facial-antz]] — DWA/PDI facial rig lineage this work continues
- [[papers/modesto-2014-dwa-face-system]] — DWA face system historical overview
- [[papers/bradley-2017-blendshape-physics]] — related: adding physics on top of blendshapes (Eurographics Research 2017)
- [[papers/cong-2016-art-directed-blendshapes]] — ILM's contemporaneous approach (using actual simulation instead of physically-inspired sculpting)
- [[concepts/muscles]] — DWA production muscle-informed face pipeline
- [[concepts/blendshapes]] — production blendshape rig with physics layer
- [[authors/prasso-luca]]
- [[authors/lan-lana]]
