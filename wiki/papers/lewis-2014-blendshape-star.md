---
title: "State of the Art Report: Facial Blendshape Animation"
authors: [Lewis, J.P.; Anjyo, Ken; Rhee, Taehyun; Zhang, Mengjie; Pighin, Frederic; Deng, Zhigang]
venue: Eurographics 2014 (State of the Art Report)
year: 2014
tags: [blendshapes, correctives, pose-space, survey]
source: raw/papers/2014-EG-blendshape_STAR.pdf
---

## Summary
Comprehensive survey of blendshape facial animation covering the history, parameterization conventions, blend models, authoring workflows, performance-driven animation, and connections to statistical face models. The canonical reference for understanding blendshape systems as used in production animation (Gollum, Stuart, Lor, Ratatouille, etc.). Covers both normalized and non-normalized conventions, additive vs. replacement models, and interpolation schemes.

## Problem
Blendshape animation is the industry standard for character facial performance, but the space is fragmented: different studios use different parameterizations, weight conventions, and interpolation schemes. A unified survey to clarify concepts and terminology is needed.

## Method
**Core blendshape formulation:**

Additive (delta) blendshapes — the most common production convention:
```math
f = b_0 + \sum_{k=1}^{N} w_k (b_k - b_0) = b_0 + Bw \quad \text{(Eq. 3–4)}
```
where $b_0$ is the neutral mesh, $b_k$ are target shapes, $w_k \in [0,1]$ are weights, and $B \in \mathbb{R}^{3p \times N}$ is the delta matrix (each column is $b_k - b_0$).

Alternative (replacement) formulation — less common:
```math
f = \sum_{k=0}^{N} w_k b_k, \quad \sum w_k = 1 \quad \text{(Eq. 1–2)}
```

**Taxonomy of blendshape systems:**
- **Semantic blendshapes**: one per muscle/action unit (smiles, blinks). Most interpretable, most common in games.
- **Correction blendshapes**: pose-space deformations that activate on specific combinations of other shapes.
- **Principal component shapes**: PCA on face scans; compact but non-semantic.
- **FACS-based**: 44+ action units defining a universal vocabulary.

**Parameterization considerations:**
- Layer ordering: phoneme → emotion → modifier → corrective (hierarchical composition)
- Delta vs. absolute shapes: deltas compose more predictably in additive stacks
- Weight ranges: $[0,1]$ normalized vs. unbounded (overshooting in USD/UsdSkel)

**Interpolation:**
- Direct linear: artifacts at combinations not anticipated by the sculptor
- Pose-space interpolation (Lewis 2000): scattered data interpolation in pose parameter space
- Layered models: semantic layers with combination correctives

## Key Results / Survey Findings
- Industry consensus favors delta blendshapes with FACS-inspired semantic parameterization.
- Corrective blendshapes are universal but expensive to author — motivating data-driven alternatives.
- Performance-driven (expression transfer) systems have matured significantly since early 2000s.
- Statistical models (3DMMs) are converging with blendshape rigs in production.

## Connections
- [[papers/lewis-2000-psd]] — PSD (pose-space deformation) is the canonical correction scheme surveyed
- [[papers/li-2017-flame]] — FLAME's expression basis $B_E \psi$ is the statistical equivalent of semantic blendshapes
- [[papers/loper-2015-smpl]] — SMPL pose blend shapes are the body equivalent
- [[papers/choi-2022-animatomy]] — Animatomy is a production blendshape system that this survey provides historical context for
- [[papers/radzihovsky-2020-facebaker]] — ML baking of blendshape rigs; motivated by the authoring cost this survey describes
- [[papers/modesto-2014-dwa-face-system]] — DreamWorks face system; same era as this survey
- [[concepts/blendshapes]] — this paper is the primary reference for the concept page
- [[concepts/pose-space-deformation]] — PSD is covered extensively as the main correction scheme

## Quotes
> "Blendshapes have the property of being simple to understand and implement, easily art-directed, and computationally efficient." (Introduction)

> "Correction shapes are required at nearly every combination of shapes in a production rig." (§3, on the combinatorial cost of manual correctives)
