---
title: "DreamWorks Animation's Face System, a Historical Perspective: From ANTZ and Shrek to Mr Peabody & Sherman"
authors: [Modesto, Lucia; Walsh, Dick]
venue: SIGGRAPH 2014 (Talk)
year: 2014
tags: [blendshapes, correctives, muscles]
source: raw/papers/DWAFaceSystemHistoricalPerspective.pdf
---

## Summary
A 1-page SIGGRAPH 2014 talk sketch providing a historical overview of DreamWorks Animation's facial animation system from ANTZ (1998) through Shrek to Mr Peabody & Sherman (2014). Covers the evolution of the facial rig architecture over roughly 16 years of production.

## Problem
Documents the long-running development of a production facial animation pipeline across many films, and how the system evolved to meet increasing quality and efficiency demands.

## Method
Overview of the DWA face system components across eras:
- Origins in the PDI facial muscle system developed for ANTZ (see [[papers/pdi-1998-facial-antz]])
- Evolution through Shrek: blendshape-based FACS-inspired controls layered on the muscle system
- Increasing reliance on corrective shapes, pose-space deformation
- System architecture as of 2014: muscle rig + correctives + pipeline integration

## Key Results
Historical documentation of industrial facial animation system evolution. Shows the trend from pure muscle simulation toward hybrid muscle+corrective+blendshape approaches.

## Limitations
1-page sketch; very high-level, no algorithmic details.

## Connections
- [[papers/lewis-2000-psd]] — pose-space deformation methodology central to the DWA system
- [[papers/mancewicz-2014-delta-mush]] — published the same year, reflects related thinking
- [[concepts/blendshapes]]
