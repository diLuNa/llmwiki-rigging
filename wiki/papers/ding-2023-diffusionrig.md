---
title: "DiffusionRig: Learning Personalized Priors for Facial Appearance Editing"
authors: [Ding, Zheng; Zhang, Xuaner; Ye, Zhihao; Peng, Sida; Kimmel, Ron; Tu, Zhiwei]
venue: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2023)
year: 2023
tags: [neural, digital-human, blendshapes, rig-generation, appearance]
source: raw/papers/Ding_DiffusionRig_Learning_Personalized_Priors_for_Facial_Appearance_Editing_CVPR_2023_paper.pdf
---

## Summary
DiffusionRig trains a personalized diffusion model conditioned on a 3D face rig (expression, lighting, pose) to enable high-fidelity facial appearance editing from a small set of reference images. The rig (rendered from a physical face model like FLAME) serves as a structural condition signal, while the diffusion model learns the person-specific appearance prior. Enables identity-preserving editing of expression, lighting, and pose without explicit 3D reconstruction or re-rendering.

## Problem
Editing facial appearance in images (changing expression, lighting, or head pose) while preserving identity requires either expensive 3D reconstruction pipelines or large personalized datasets. Generic diffusion models hallucinate identity details; rig-based methods lack the photorealism of neural rendering.

## Method
**Three control modes (as shown in the pipeline):**
1. **Expression rigging**: condition on rendered expression coefficients from a fitted FLAME mesh → change facial expression while preserving identity and lighting.
2. **Lighting rigging**: condition on environment map / SH lighting → relight the face under the same expression and pose.
3. **Pose rigging**: condition on rendered head pose → change head rotation while preserving expression and appearance.

**Architecture:**
- A diffusion UNet conditioned on rendered "rig images" (low-resolution renders of the physical face model at target rig parameters).
- **Personalization**: the diffusion model is fine-tuned per-person on a small set (10–50) of reference images, learning appearance priors (skin color, hair, freckles, etc.) not captured by the rig render.
- At inference: given target rig parameters, render the rig; run the diffusion model conditioned on the render → outputs a photorealistic image matching the target rig and the person's appearance.

**Conditioning mechanism:**
- Rig renders are concatenated to the noisy latent in the UNet input.
- Separate conditioning paths for different rig types (expression, lighting, pose) share the same backbone.

## Key Results
- High-quality, identity-preserving expression edits from a small photo set.
- Convincing relighting without 3D reconstruction.
- Competitive with dedicated 3D neural rendering approaches but more flexible.
- Generalizes across diverse individuals (multiple ethnicities, ages, hairstyles).

## Limitations
- Requires per-person finetuning (~10 min per identity); not fully zero-shot.
- Rig quality depends on the fitted physical model (FLAME fitting errors propagate).
- Primarily operates in 2D image space — does not produce 3D geometry.
- Expression editing is limited by the expressiveness of FLAME's expression space.

## Connections
- [[papers/li-2017-flame]] — DiffusionRig uses FLAME as the face rig representation for conditioning
- [[papers/radzihovsky-2020-facebaker]] — FaceBaker bakes rig → appearance via neural inference; DiffusionRig uses diffusion for higher quality
- [[papers/bagautdinov-2018-facial-cvae]] — similar goal (VAE-based face appearance model) but pre-diffusion era
- [[concepts/digital-human-appearance]] — diffusion-based photorealistic face appearance conditioned on rig parameters
- [[concepts/blendshapes]] — expression rig inputs are FLAME expression coefficients (equivalent to blendshape weights)

## Implementation Notes
The conditioning pipeline:
```python
# Fit FLAME to source images → get expression/pose/lighting params
flame_params = fit_flame(reference_images)  # per-person finetuning step

# At inference:
rig_render = render_flame(flame_params, target_expression, target_pose, target_lighting)
# Run diffusion conditioned on rig_render
output_image = diffusion_model(noise, condition=rig_render, guidance_scale=7.5)
```
The key insight: using low-quality rig renders (vertex-colored FLAME) as condition is sufficient — the diffusion model fills in all appearance details from the personalized prior.
