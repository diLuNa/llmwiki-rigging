---
title: "Fabrig: A Cloth-Simulated Transferable 3D Face Parameterization"
authors: [Zhu, ChangAn; Joslin, Chris]
venue: ACM 2024 (conf. TBD)
year: 2024
tags: [blendshapes, simulation, muscles, rig-generation]
source: raw/papers/Fabrig.pdf
---

## Summary
Fabrig parameterizes a 3D face using anatomy-inspired muscle and fat patches whose deformation is driven by cloth simulation rather than volumetric physics. This makes the rig transferable across diverse characters without per-character blendshape preparation, supports physical secondary motion, and provides local anatomical editing controls accessible to artists.

## Problem
Existing face parameterization methods are either limited to human faces, require laborious per-character blendshape sculpting, or use expensive volumetric simulation. Methods that allow physics-based simulation suffer from limited character compatibility and editability.

## Method
**Anatomy-inspired surface patches:**
- From a normalized 3D face mesh, generate three types of surface patches: skull (rigid), muscle patches (deforming), and fat patches (secondary motion).
- These patches are generated deterministically from the face geometry — no face-specific blendshapes needed.

**Muscle blendshape templates:**
- A set of template muscle blendshapes (corresponding to anatomical facial muscles) is transferred from a canonical face to each character's muscle patches via mesh deformation transfer.
- Blendshape weights directly control each muscle's contraction.

**Cloth simulation for physics:**
- The muscle patches deform via blendshape weights; fat patches are simulated as cloth driven by the muscle motion.
- This replaces the computationally heavy volumetric simulation with a lighter surface simulation, gaining dynamic skin wrinkling and secondary jiggle.

**Skull mesh for rigid motion:**
- A skull mesh handles rigid jaw and head motion, constraining the muscle and fat patches as boundary conditions for the cloth simulation.

**Transfer:**
- Since patches are generated from any normalized face mesh, the parameterization automatically transfers to new characters — human or non-human — without additional artist work.

## Key Results
- Parameterizes diverse characters (humans, orcs, fantasy creatures) from the same pipeline.
- Natural secondary motion from cloth simulation without volumetric computation.
- Animatable by marker-based mocap retargeting.
- Objective evaluation confirms accurate reconstruction of facial poses.

## Limitations
- Cloth simulation quality depends on simulation parameter tuning (stiffness, damping) which may need per-character adjustment.
- The skull-fitting step requires approximate face anatomy.
- Not evaluated on extreme non-humanoid characters.

## Connections
- [[papers/choi-2022-animatomy]] — similar anatomy-inspired muscle curve approach, production-scale
- [[papers/mancewicz-2014-delta-mush]] — surface smoothing applied to skin deformation
- [[papers/sumner-2004-deformation-transfer]] — deformation transfer used for muscle blendshape retargeting
- [[concepts/blendshapes]]
- [[concepts/neo-hookean-simulation]] — cloth/soft tissue simulation class used for fat patches
