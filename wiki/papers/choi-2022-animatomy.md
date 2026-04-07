---
title: "Animatomy: an Animator-centric, Anatomically Inspired System for 3D Facial Modeling, Animation and Transfer"
authors: [Choi, Byungkuk; Eom, Haekwang; Mouscadet, Benjamin; Cullingford, Stephen; Ma, Kurt; Gassel, Stefanie; Kim, Suzi; Moffat, Andrew; Maier, Millicent; Revelant, Marco; Letteri, Joe; Singh, Karan]
venue: SIGGRAPH Asia 2022
year: 2022
tags: [blendshapes, correctives, neural, rig-generation, muscles]
source: raw/papers/Animatomy.pdf
---

## Summary
Animatomy is a production facial animation pipeline used on Avatar: The Way of Water (Weta FX) that replaces FACS action units with a set of *contractile muscle fiber curves* as the anatomic basis. Muscle contraction strains parameterize 3D facial scans, driving skin deformation and enabling clean expression transfer between actors and digital characters.

## Problem
FACS-based facial rigs have well-known limitations: action units conflate multiple muscles, provide poor localization, suffer from opposition/redundancy issues, and don't transfer cleanly across different face shapes. Artists end up with hundreds of corrective blendshapes that are painful to maintain and retarget.

## Method
**Muscle curves:** A set of muscle fiber curves is fit to the actor's face anatomy (using tissue-depth priors from forensic peg data). Each curve models a specific facial muscle (zygomaticus, orbicularis, etc.). Muscle *contraction strain* is the scalar deformation parameter per curve — analogous to a muscle's activation level.

**Dynamic scan capture and fitting:**
- Actor performs FACS actions, emotions, and speech: ~7,000 frames of 3D mesh sequences.
- Sequential registration (R3DS Wrap) aligns all frames to a template.
- Jaw solved using a non-linear jaw rig (Zoss et al. 2018, [[papers/zoss-2018-jaw-rig]]).
- Muscle strains per frame extracted by fitting the curve contraction model to the scan sequence.

**Strain-driven deformation:**
- A passive muscle simulation relates curve strains to skin vertex displacements.
- A manifold of plausible expressions is learned from the strain space (autoencoder).
- At runtime: strain values drive skin via learned mapping; strains are directly animatable.

**Expression transfer:**
- Strains are face-agnostic: the same strain values applied to a different character's muscle curves produce an analogous expression.
- Eliminates need for per-character blendshape retargeting.

**Integration:**
- Strains can be driven by performance capture (solving strains from camera data) or direct animator control (editing strain curves in the shot).
- Traditional rig modules (jaw, eyes) plug in alongside the strain system.

## Key Results
- Used in production on Avatar: The Way of Water.
- Clean expression transfer from actor to diverse characters (humans, Na'vi, creatures).
- Significant reduction in blendshape maintenance compared to FACS-based rigs.
- Strains provide more localized, non-redundant control than action units.

## Limitations
- Requires careful muscle curve fitting per actor — still a rigging authoring step.
- Passive simulation and manifold learning are offline; real-time inference uses the learned model.
- Assumes sufficient 3D scan data is available for the actor.

## Connections
- [[papers/zoss-2018-jaw-rig]] — jaw rig used as sub-component for mandible motion
- [[papers/lewis-2000-psd]] — FACS / pose-space paradigm that Animatomy replaces
- [[papers/holden-2015-inverse-rig]] — rig inversion in the strain space
- [[papers/radzihovsky-2020-facebaker]] — complementary ML-based rig baking approach
- [[concepts/blendshapes]] — what Animatomy significantly reduces
- [[authors/singh-karan]]

## Implementation Notes
Muscle curves are the key authoring primitive: a rigging artist places anatomically informed curves on the face mesh, seeded by standard facial muscle anatomy. The contraction direction is along the curve; the influence radius is the main artist parameter.

The passive muscle simulation (Choi et al. 2022 internal) uses the muscle curve deformation as a boundary condition and propagates the deformation to the skin via a physics-based layer — somewhat analogous to delta-mush but physically motivated.

## Quotes
> "Present FACS-based systems are plagued with problems of face muscle separation, coverage, opposition, and redundancy."

> "The strains, in turn, control skin deformation and readily transfer expression from an actor to characters."
