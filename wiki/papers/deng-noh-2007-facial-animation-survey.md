---
title: "Computer Facial Animation: A Survey"
authors: [Deng, Zhigang; Noh, Junyong]
venue: "In: Deng & Noh (eds.), Data-Driven 3D Facial Animation, Springer"
year: 2007
tags: [blendshapes, muscles, facial-capture, facs, rig-generation, survey]
source: "http://graphics.cs.uh.edu/website/Publications/2007_facial_animation_survey_bookchapter.pdf"
---

## Summary
A comprehensive CG-focused survey of facial animation techniques as of 2007, covering the full pipeline from face modeling and rigging to animation and performance capture. Serves as a reference bridge between the FACS psychophysical literature and its practical implementation in computer graphics systems — blendshape rigs, muscle models, data-driven approaches, and performance capture. Particularly useful for understanding how AU-based parameterization entered mainstream CG, and how different animation paradigms relate to FACS.

## Problem
Facial animation spans multiple research communities (computer graphics, computer vision, speech processing, psychology) with inconsistent terminology and fragmented literature. A unified CG-centric survey was needed.

## Method
Survey organized around four pillars:
1. **Face Representation**: geometry models, blend shapes, muscle models, performance capture meshes
2. **Animation Control**: FACS-based parameterization, muscle activations, speech-driven animation, data-driven spaces
3. **Animation Synthesis**: keyframing, physical simulation, speech-driven, machine learning
4. **Performance Capture**: optical marker systems, markerless video, active depth sensors

Key FACS-related coverage:
- How action units map to blendshape targets in practice
- The Waters (1987) muscle model and its descendants
- Early performance capture systems using FACS as an intermediate representation
- Data-driven approaches that learn FACS-to-geometry mappings from captured data

## Key Results
- Establishes a consistent taxonomy for the field at a time when no single reference spanned all sub-areas
- Identifies the FACS → blendshape pipeline as the dominant industry approach (supplanting pure muscle simulation for most production work)
- Notes that muscle-based simulation remains important for secondary dynamics (skin sliding, bulging) even when rig control is blendshape-based
- Documents early neural/statistical approaches to facial animation

## Limitations
- Pre-deep learning (2007): neural methods now dominate performance capture and synthesis
- No coverage of USD/HDA pipeline, real-time FACS rigs, or neural auto-rigging
- Muscle model section reflects state as of 2006; significantly outdated relative to ILM FEM pipeline ([[papers/cong-2015-anatomy-pipeline]]) and Weta Animatomy ([[papers/choi-2022-animatomy]])

## Connections
- [[concepts/facs]] — survey's main contribution is placing FACS firmly in the CG context
- [[concepts/blendshapes]] — blendshape survey section is a concise pre-STAR reference
- [[concepts/muscles]] — covers Waters (1987) muscle lineage through 2006
- [[concepts/facial-blendshape-rigs]] — taxonomy of control paradigms maps to this concept page
- [[papers/ekman-friesen-1978-facs]] — primary source cited throughout
- [[papers/waters-1987-muscle-model]] — key muscle model covered in depth
- [[papers/lewis-2014-blendshape-star]] — the 2014 STAR supersedes this survey for blendshape-specific content

## Implementation Notes
- Available free online (UH Graphics lab server): the PDF remains an accessible entry point for the pre-2010 literature
- The survey's blendshape weight solving section predates JTDP03 and FACEIT; see [[papers/jtdp-2003-blendshape-fitting]] for the more rigorous formulation
