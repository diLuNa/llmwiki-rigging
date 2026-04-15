---
title: "Metaball Madness - The Rigging Of An Implicit Surface Character"
authors: [Lykkegaard, Anna-Christine; Butts, Andrew; Teo, Julian]
venue: SIGGRAPH Talks 2025
year: 2025
tags: [rig-generation, implicit-surfaces, houdini, digital-human]
source: raw/papers/2025.ooooo_rig.pdf
doi: 10.1145/3721239.3734079
---

## Summary
OOOOO — the liquid supercomputer character in Pixar's *Elio* (2025) — became Pixar's **first mesh-free character rig**. Her design required capabilities impossible with traditional mesh-based rigs: arms sliding anywhere on her body, separating liquid chunks, absorbing objects, growing arms on the fly, and facial features sliding across her surface. The solution is a hierarchical system of implicit surface primitives (SDFs) and operators — a rigged shader architecture — that gives animators full fidelity control while remaining downstream-renderable.

## Problem
Traditional character rigging operates on a fixed mesh topology: joints and blendshapes deform specific vertices. OOOOO's behaviors are topologically dynamic:
- Arms appear anywhere on the body surface (no fixed attachment point)
- Body can split into disconnected liquid blobs (topology change)
- Facial features (eyes, mouth) can slide across the body
- Objects can be absorbed (merged into the body volume)

None of these are representable with a fixed-vertex-count mesh deformed by LBS or blendshapes.

## Method

### Primitive Types
Two new prim types were introduced in Pixar's rigging software:

**BlObjects** — GLSL code for SDF (Signed Distance Field) computation:
- Standard primitives: ellipsoids, rounded boxes, tori
- Custom SDFs: mouth, eyelids, arm shapes
- Each BlObject defines a local SDF contributing to the character's global implicit surface

**BlOperators** — apply boolean/smooth operations to children:
- Smooth union (metaball blending) of child BlObjects
- Subtraction (carving cavities)
- Intersection
- Ability to combine hierarchically for complex shapes

### Hierarchical Architecture
The character is a scene graph of BlObjects and BlOperators, organized hierarchically like a traditional rig but operating on implicit functions rather than mesh geometry:

```
OOOOO_body (BlOperator: smooth union)
├── body_core (BlObject: ellipsoid)
├── left_arm (BlObject: custom SDF)
│   └── driven by rig control: arm_position (sliding on body surface)
├── right_arm (BlObject: custom SDF)
├── face_group (BlOperator: smooth union)
│   ├── left_eye (BlObject: ellipsoid)
│   ├── right_eye (BlObject: ellipsoid)
│   └── mouth (BlObject: custom SDF)
└── absorbed_object (BlObject: activated on interaction)
```

Any BlObject can be parented to a surface-sliding control, giving animators the appearance of features that move across the body. Adding or removing arms is as simple as adding/removing BlObjects from the hierarchy.

### Renderability
The SDF hierarchy is evaluated at render time as a raymarched implicit surface. Reference: [Luo et al. 2025] for the rendering pipeline. The rig drives SDF parameters; the renderer marches rays against the resulting implicit surface.

### Animation Paradigm Preservation
Despite the mesh-free representation, the animation controls follow standard paradigms:
- Translate/rotate/scale controls for each BlObject
- Facial expression controls (mouth open/close, eye shape) as custom SDF parameters
- Corrective shapes implemented as SDF parameter offsets

## Key Results
- First production mesh-free character rig at Pixar
- Full animator fidelity: all standard animation controls preserved
- Supports topological changes (splitting, merging, arm placement) impossible with traditional rigs
- Downstream-renderable via raymarching at production quality

## Limitations
- Not compatible with downstream mesh-based pipelines (cloth simulation, intersection detection, etc.) without conversion
- SDF evaluation and compositing is more expensive than mesh deformation for some operations
- Custom SDF authoring requires technical artist with shader knowledge
- Difficult to retarget to different characters without redesigning the SDF hierarchy

## Connections
- [[concepts/implicit-surfaces]] — the foundational representation: SDFs, metaballs, smooth blending
- [[papers/lykkegaard-2025-ooooo-rig]] — this paper
- [[authors/butts-andrew]] — co-author; Pixar TD

## Implementation Notes
- The smooth union operator (metaball blending) is typically implemented as: $f_{blend}(d_1, d_2) = \frac{d_1 d_2 - k}{\sqrt{d_1^2 + d_2^2}}$ or the exponential variant $f = -\frac{1}{k}\ln(e^{-k d_1} + e^{-k d_2})$ (Inigo Quilez formulas)
- Custom SDF primitives can be prototyped in Shadertoy or similar GLSL environments before integration
- Houdini equivalent: VEX SDF operators + Volume Boolean SOP for prototyping; Karma XPU for raymarching production render
- For downstream cloth/sim: convert implicit to mesh via marching cubes at needed frequency — works for static poses, challenging for topology-changing animation

## Quotes
> "OOOOO became Pixar's first mesh-free character rig." (Abstract)
> "The system's architecture supports a hierarchical arrangement of implicit surface primitives and operators, allowing for complex transformations while preserving normal animation paradigms." (Abstract)
