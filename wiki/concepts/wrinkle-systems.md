---
title: "Wrinkle Systems"
tags: [correctives, pose-space, simulation, deformation]
---

## Definition
Wrinkle systems generate surface displacement deformations — on clothing or skin — that capture fine fold geometry beyond what a base deformation rig produces. They sit as a post-process layer on top of skinning or simulation results.

## Variants / Taxonomy

- **Art-directed pose-space wrinkles**: Artist sculpts wrinkle patterns on reference poses. At runtime, surface stress or pose proximity weights blend between reference patterns. Fast, history-independent, highly art-directable. [[papers/cutler-2007-art-directed-wrinkles]]
- **Mesh-tension driven wrinkles**: Mesh compression is measured as a scalar tension field; wrinkle texture maps are blended in proportion to local tension. Works at texture level (albedo + displacement). [[papers/raman-2022-mesh-tension-wrinkles]]
- **Simulation-based wrinkles**: Cloth simulation or finite-element skin simulation produces wrinkles physically. High fidelity but slow and hard to art-direct. [[papers/smith-2018-neo-hookean]]
- **Analytic wrinkles**: Geometric formulas (e.g., cylinder compression) produce plausible wrinkle geometry without artist input or simulation.

## Key Papers
- [[papers/cutler-2007-art-directed-wrinkles]] — curve-based, stress-weighted blending; PDI/DreamWorks production system
- [[papers/raman-2022-mesh-tension-wrinkles]] — tension-driven texture blending for synthetic face renders

## Connections
- [[concepts/pose-space-deformation]] — wrinkle blending as a specialized pose-space application
- [[concepts/delta-mush]] — smoothing layer that wrinkle systems typically run after
- [[papers/mancewicz-2014-delta-mush]] — post-process smoothing

## Wrinkle Taxonomy (Anatomical — for Character Design)

Source: Melinda Ozel, [[queries/melindaozel-deep-dives]]

### Dynamic Wrinkles (Expression Lines)
Form from **repeated facial expressions**. Direction is **perpendicular to underlying muscle fiber direction** (e.g., vertical frontalis fibers → horizontal forehead wrinkles).

Used in character design to signal habitual emotional life:
- Medial forehead wrinkles (AU1) → empathetic, worried, hopeful
- Full horizontal forehead wrinkles (AU1+2) → sociable, engaged
- Glabellar furrows (AU4) → anger, concentration, confusion
- Crow's feet (orbicularis orbitalis/AU6) → joy history
- Nasolabial smile lines (AU12) → happiness

**Important caveat:** dynamic wrinkle patterns are also affected by genetics and facial morphology — they are not guaranteed evidence of habitual expressions.

### Static Wrinkles
NOT caused by muscle movement. Causes:
- **Gravity** — skin fold from decades of gravitational loading
- **Compression / sleep position** — e.g., a vertical left-forehead crease from habitual left-side sleeping (Anthony Hopkins example); these do not correlate with any muscle
- **Intrinsic aging** — collagen/elastin degradation
- **UV/extrinsic aging** — sun damage
- **Skin anisotropy** — skin is directionally dependent; wrinkles propagate along lines of least mechanical resistance

**Rigging implication:** Static wrinkles belong in the **neutral mesh geometry**, not in blendshapes. They should not change with expression (only deform passively under skin stretch).

## Notes
The stress / tension signal is the key design choice. Options range from simple edge-length ratios to the full Green–Lagrange strain tensor. A practical production signal: compute the ratio of deformed-to-rest edge lengths averaged over incident edges, then threshold to extract compression (negative strain) as a wrinkle trigger.

In Houdini, tension can be computed as a point wrangle using `neighbours()` + `rest` geometry input, then fed into a blendshape SOP to mix wrinkle targets.
