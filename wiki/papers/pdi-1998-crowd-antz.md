---
title: "The PDI Crowd System for ANTZ"
authors: [PDI/DreamWorks]
venue: SIGGRAPH Sketches 1998
year: 1998
tags: [crowd-animation, rig-generation, procedural]
source: raw/papers/ThePDICrowdSystemforANTZ.pdf
---

## Summary
A 1-page SIGGRAPH sketch describing the two crowd animation systems built at PDI/DreamWorks for *ANTZ* (1998): the **Blending System** (motion cycle scripting with seamless transition and high-level behavioral controls) and the **Crowd Simulator** (physics-based particle system driving cycle selection for thousands of characters). Both systems are built on PDI's procedural scripting language.

## Problem
*ANTZ* required animating crowd shots ranging from a handful to 50,000+ ant characters — far too many to hand-animate individually. Animators needed both batch control over crowds and per-character refinement capability.

## Method
**Blending System:**
- Library of pre-animated motion cycles (created by character animators for quality).
- Scripted transitions between cycles using blending weights.
- High-level behavioral controls: balance, foot locking, body individuality.
- Outputs function-curve format — animators can refine per-character.
- Handles shape variation (differently proportioned bodies) while preserving motion character.

**Crowd Simulator:**
- Particle-system-like engine driving character placement and motion.
- Physical forces: obstacles, goals, flow fields, inter-character interaction.
- Motion cycle selection driven by current physical state (speed, heading).

**Scripting language:** Both systems written in PDI's proprietary procedural scripting language core to their pipeline.

## Key Results
- Crowd shots of 50,000+ ant characters achieved.
- Animators retain per-character refinement control.
- Seamless blending between motion cycles preserves animation quality.

## Limitations
- 1-page sketch — no technical detail on blending math or simulator physics.
- Proprietary PDI scripting language (not generalizable).
- Motion quality bounded by the cycle library.

## Connections
- [[concepts/pose-space-deformation]] — blending of pre-authored poses underlies the cycle system
- [[papers/pdi-1998-facial-antz]] — companion sketch on the PDI facial system for ANTZ

