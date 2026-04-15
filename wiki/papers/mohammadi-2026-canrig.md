---
title: "CANRIG: Cross-Attention Neural Face Rigging with Variable Local Control"
authors: [Mohammadi, Arad; Weiss, Sebastian; Buhmann, Jakob; Ciccone, Loic; Sumner, Robert W.; Bradley, Derek; Guay, Martin]
venue: Computer Graphics Forum (Eurographics 2026), Vol. 45, No. 2
year: 2026
tags: [facial-animation, blendshapes, neural, rig-generation, digital-human]
source: raw/papers/CANRIG-Cross-Attention-Neural-Face-Rigging-with-Variable-Local-Control-Paper.pdf
---

## Summary
CANRIG (Cross-Attention Neural face RIGging) automates facial rigging by using cross-attention between sparse user-placed control handles and mesh vertices, modulated by a user-defined editing region. This gives animators both the automation/naturalness of neural face models and the granular local control professional production demands. A shape-preserving extension supports iterative additive edit layers — changing the control layout does not disturb previously established edits. Published in Computer Graphics Forum (Eurographics 2026) by DisneyResearch|Studios and ETH Zürich.

## Problem
Traditional facial rigging requires weeks of expert technical artist time to build a rig, and then animators must manipulate hundreds of controls to achieve varied expressions. Two opposing paradigms exist:
- **Neural face models** (e.g., FLAME, CoMA): natural, automated, but sacrifice local control — deformations are globally coupled through latent codes
- **Blendshape rigs**: precise local control but require extensive manual setup and many controls

Neither provides the combination required for production: automation + naturalness from data + fine-grained local control that adapts flexibly to per-shot needs.

## Method

### Core Idea: Cross-Attention Deformation
Deformation is modeled as **cross-attention** between control handles and mesh vertices:

```
Keys, Values:   control handles h_1,...,h_K   (positions + handle descriptors)
Queries:        mesh vertices v_1,...,v_N
Modulation:     user-defined region R          (soft spatial mask)
Output:         per-vertex displacement Δv
```

Attention weights determine how strongly each control handle influences each mesh vertex. The user-defined region $R$ spatially modulates the attention: handles outside the region have near-zero influence on vertices inside, and vice versa. This decouples local edits — moving a handle on the forehead does not affect the mouth.

**Variable control density**: The user can place any number of control handles ($K$ is not fixed) in any layout — coarse (few handles, large region) for broad deformations, fine (many handles, small region) for precise edits. The cross-attention architecture naturally handles variable-length handle sets.

### Shape-Preserving Additive Layers
CANRIG introduces an **additive deformation layer** system:
1. User establishes a base edit with handles $H_1$, region $R_1$
2. Base deformation is frozen
3. User adds a new layer with handles $H_2$, region $R_2$ for fine editing
4. The new layer produces displacements additive to layer 1; layer 1 deformations are guaranteed untouched

This mirrors a Photoshop-layer metaphor: each layer is independently controllable and non-destructive.

### Training
Trained on a dataset of professional facial performances with diverse expressions and face shapes. The network learns the statistical prior of facial deformations from data, enabling it to produce natural, plausible deformations from sparse handle inputs rather than requiring every vertex to be explicitly driven.

Loss: combination of vertex position error and perceptual losses on rendered images.

## Key Results
- Enables animation and VFX workflows with significantly fewer controls than traditional rigs
- Variable local control: the same model supports both coarse (global expression) and fine (eyelid corner) edits without model changes
- Shape-preserving layers ensure iterative workflows — coarse-to-fine editing without re-doing earlier work
- Demonstrated in both animation (expressive character) and high-end VFX (photo-real face) pipelines
- Open-access publication (CC BY-NC-ND)

## Limitations
- Requires training on professional facial performance data — model quality depends on dataset diversity
- Attention-based architecture may struggle with extremely local, high-frequency edits far from any handle
- Not yet demonstrated for non-humanoid facial shapes
- Handle placement is a new interaction paradigm that animators need to learn

## Connections
- [[concepts/facial-blendshape-rigs]] — traditional paradigm this work seeks to replace/augment
- [[concepts/nonlinear-face-models]] — the neural face model background (FLAME, CoMA) that provides the statistical prior
- [[papers/ma-2025-riganyface]] — concurrent neural auto-rigging work; different approach (FACS-based blendshapes vs. control handle interaction)
- [[authors/sumner-robert]] — co-author; DisneyResearch|Studios / ETH Zürich
- [[authors/bradley-derek]] — co-author; DisneyResearch|Studios

## Implementation Notes
- Cross-attention between handles and vertices is $O(KN)$ — efficient for typical face meshes ($N$ ~ 10k vertices) and sparse handle sets ($K$ ~ 10–100)
- The spatial region modulation can be implemented as a Gaussian-weighted mask centered on the user-defined region boundary
- Additive deformation layers can be stacked by accumulating displacements; each layer is a separate forward pass of the network with a frozen base mesh
- For Houdini: handle positions can be driven by SOP-level controls; network inference via Python SOP; region mask as a vertex color attribute

## Quotes
> "By modeling deformation as cross-attention between control handles and mesh vertices—modulated by a user-defined region—we enable seamless transitions from precise local adjustments to broad global changes." (Abstract)
> "Our method delivers the best of both worlds: the automation and naturalness of neural methods with the granular control that professional animators demand." (Abstract)
