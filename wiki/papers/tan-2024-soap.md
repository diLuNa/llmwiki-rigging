---
title: "SOAP: Style-Omniscient Animatable Portraits"
authors: [Tan, Qingyang; Cao, Chen; Saito, Shunsuke; Romero, Javier; Rushmeier, Holly; Nam, Giljoo]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [neural, avatar-generation, 3d-diffusion, facial-animation, portrait-generation]
source: arXiv:TBA
doi: 10.1145/3721238.3730691
---

## Summary
Framework for generating rigged, topology-consistent 3D portrait avatars from any 2D image with animation controls. Uses style-omniscient diffusion model addressing domain gap and artifact issues in existing 3D diffusion approaches. Produces complete, animatable character rigs directly from portraits.

## Problem
3D diffusion models for portrait generation often lack animation controls or suffer from artifacts due to domain gap between 2D images and 3D geometry. Existing avatar reconstruction methods require video sequences or specialized capture systems.

## Method
- **Style-omniscient diffusion**: Image-conditioned 3D generation preserving input appearance characteristics
- **Topology consistency**: Ensures generated mesh is suitable for rigging and animation
- **Rig generation**: Automatic skeleton extraction and skinning weight computation
- **Deformation control**: Blendshape-based facial animation support

## Key Results
- Generates high-quality 3D avatars from single 2D portraits
- Maintains appearance consistency while producing animatable geometry
- Produces complete character rigs (skeleton + weights + blendshapes)
- Enables facial animation and expression transfer

## Limitations
- Quality depends on input portrait resolution and lighting
- Generalization to extreme face shapes limited by training data
- Fully automatic rigging may require manual refinement for complex deformations
- Torso/body generation quality below head quality

## Connections
- [[papers/li-2017-flame]] — morphable model foundation
- [[papers/xu-2020-rignet]] — neural rig generation
- [[papers/ma-2025-riganyface]] — character-specific neural rigging
- [[concepts/auto-rigging]] — automatic skeleton and weight generation
- [[techniques/ml-deformer]] — learned deformation

## Implementation Notes
- Domain gap mitigation through adversarial training between 2D and 3D samples
- Topology consistency enforced via graph-based losses
- Compatible with standard DCC tools (Houdini, Maya, Blender)
- Requires careful hyperparameter tuning for identity preservation

## External References
- ACM DL: [doi.org/10.1145/3721238.3730691](https://doi.org/10.1145/3721238.3730691)
- SIGGRAPH 2024 proceedings
