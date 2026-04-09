---
title: "Muscle Simulation for Film Characters: Deploying the System for King Kong"
authors: [Cong, Matthew; Bao, Michael R.; Fedkiw, Ronald]
venue: SIGGRAPH Talks 2017
year: 2017
tags: [muscles, simulation, blendshapes, digital-human]
source: raw/papers/cong-2017-kong-muscle-talk.pdf
---

## Summary
Production case study on deploying ILM's anatomy-based muscle simulation system for **King Kong** in *Kong: Skull Island* (2017). Documents the full workflow from MRI-derived anatomy model (Cong 2015) through simulation-based blendshape generation (Cong 2016) to final character animation. First public report of a muscle simulation system used for a production VFX character. Identifies practical challenges: simulation stability at extreme expressions, blendshape count management, animator workflow integration. SIGGRAPH Talks 2017.

## Problem
Deploying the muscle simulation pipeline at production scale (full film schedule, multiple animators, director revisions) surfaces practical challenges not addressed in research papers: blend shape count explosion, simulation artifacts at extreme poses, integration with existing Maya/proprietary rigging pipelines, and performance under production deadlines.

## Method
**Deployment workflow:**
1. **MRI scan** of reference sculpt (not a real human: digital Kong head)
2. **Anatomy model** via Cong 2015 pipeline: tissue segmentation, tet mesh, muscle atlas registration
3. **Simulation blendshapes** via Cong 2016: FEM muscle activation for each AU + key combination shapes
4. **Integration into production rig:** blendshape targets exported as standard Maya blendshape deformer; same controls as traditional FACS rig
5. **Artist workflow:** animators drive the FACS controls; simulation-quality deformations are transparent to artists

**Practical innovations:**
- Selective combination shape generation: only AU pairs with visible physical interaction receive dedicated combination shapes (reduces count from $O(N^2)$ to manageable)
- Simulation stability: clamp activation ranges to safe regions; fallback to linear interpolation for unstable regions
- Art direction layer: sculpt corrections on top of simulation blendshapes for director-specified tweaks

## Key Results
Successfully deployed on Kong character in *Kong: Skull Island*. Achieved muscle-quality tissue deformation (cheek bulging, skin sliding) in a production timeline. Director noted improved believability of extreme expressions vs. hand-sculpted approach. First production VFX character with anatomy-physics-derived blendshape rig. SIGGRAPH Talks 2017.

## Limitations
Kong is a fictional character — MRI from a sculpt, not a real primate. Blendshape count still significant even with selective combination shapes. No runtime physics — only baked simulation. Dynamic effects (jiggling, secondary dynamics) handled separately.

## Connections
- [[papers/cong-2015-anatomy-pipeline]] — anatomy model generation pipeline
- [[papers/cong-2016-art-directed-blendshapes]] — blendshape generation method deployed here
- [[papers/bao-2019-face-capture-muscles]] — follow-on work: muscle activations for face capture
- [[papers/teran-2005-quasistatic-flesh]] — FEM simulation engine
- [[concepts/muscles]] — production deployment of anatomy simulation pipeline
- [[concepts/blendshapes]] — simulation-derived blendshapes in production
- [[authors/cong-matthew]]
- [[authors/fedkiw-ronald]]
