---
title: "CurveCrafter: A System for Animated Curve Manipulation"
authors: [Willett, Nora S.; Fleischer, Kurt; Brown, Haldean; Le, Ilene; Meyer, Mark]
venue: SIGGRAPH 2023
year: 2023
tags: [rig-generation, deformation, houdini]
source: raw/papers/2023.Others.WFBEM.pdf
---

## Summary
An interactive system for authoring, editing, and retiming stylized 2D linework (silhouette curves, feature lines) on 3D animated characters. Allows animators to draw, redraw, erase, and shape-edit curves with temporally consistent propagation over tracked silhouettes.

## Problem
Stylized 2D line art on 3D characters requires per-frame curve editing that is temporally consistent, respects the character's 3D motion, and doesn't require frame-by-frame re-authoring. Standard 3D silhouette extraction doesn't provide enough artistic control.

## Method
- **Curve tracking**: silhouette curves are tracked across frames via surface parameterization.
- **Shape editing**: artists draw, redraw, or adjust curve shape/opacity on any frame; edits propagate forward/backward with temporal consistency.
- **Retiming**: curve timing can be adjusted independently of animation.
- Edit propagation algorithm ensures curves don't pop or drift as the surface deforms; handles silhouette curve expand/merge events.

## Key Results
- Used by five professional animators on three production shots.
- Used by effects lead on *Pete* (Pixar short film) for difficult production edits.
- Achieves temporal consistency even through silhouette topology changes.

## Limitations
- Focused on surface-attached curves; volumetric effects not addressed.
- Opacity editing limited to predefined curve types.

## Connections
- [[authors/fleischer-kurt]]
- [[authors/meyer-mark]]

## Implementation Notes
The curve tracking mechanism uses the surface UV parameterization to follow curve positions as the mesh deforms. In Houdini, a similar approach can be built using the `uvunwrap` + `primuv` workflow to track curves on animated geometry.
