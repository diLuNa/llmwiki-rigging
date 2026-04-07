---
title: "The PDI Facial Animation System for ANTZ"
authors: [PDI/DreamWorks]
venue: SIGGRAPH Sketches 1998
year: 1998
tags: [blendshapes, muscles, rig-generation]
source: raw/papers/ThePDIfacialAnimationSystem.pdf
---

## Summary
A 1-page SIGGRAPH sketch describing the muscle-based facial animation system built at PDI/DreamWorks for *ANTZ* (1998). The system uses a complete set of anatomically-inspired virtual muscles (300+ controls including muscles, bone movements, eye rotations) layered into intuitive high-level controls. Muscle activations cause physically-plausible soft/hard area deformation; layered interface enables both bulk and fine per-muscle animation.

## Problem
*ANTZ* required convincing ant facial animation conveying a full range of human-like expressions. Traditional blendshape rigs lack the layering and physical intuition of anatomy-based systems. Direct muscle control of 300+ elements would be too slow for animators.

## Method
**Virtual muscles:** Complete set of muscles corresponding to real human facial anatomy (frontalis, corrugator, etc.), re-applied to ant character geometry. Same muscle combinations as human expression rules.

**Material-respecting deformation:** Hard regions (bone-like) deform minimally; soft regions (cheeks) bulge/compress with activation. Physically motivated but not physically simulated.

**Layered interface:**
- Low level: individual muscle / bone / eye controls (300+)
- High level: combined controls like `r_brow_mad`, `l_eye_widen` — compound activations authored by technical directors

**Procedural scripting:** Interface built on PDI's procedural scripting language; supports scripted expression sequences and emotion overlays.

## Key Results
- Expressive ant faces capable of full human emotional range despite non-human anatomy.
- Layered approach allows both bulk art direction and fine per-muscle refinement.
- Used in production on *ANTZ* (1998), DreamWorks' first fully CG feature film.

## Limitations
- 1-page sketch — no math or deformation formulation.
- Muscle system is kinematic / corrective-based, not physically simulated.
- Proprietary PDI infrastructure; not generalizable.

## Connections
- [[papers/choi-2022-animatomy]] — modern anatomy-inspired facial rig (Weta FX, Avatar 2)
- [[papers/pdi-1998-crowd-antz]] — companion sketch on the crowd system
- [[papers/modesto-2014-dwa-face-system]] — DreamWorks face system retrospective
- [[concepts/blendshapes]] — blendshape layer above the muscle system

