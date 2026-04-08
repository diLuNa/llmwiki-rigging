---
title: "Digital Human Appearance"
tags: [digital-human, appearance, facial-capture, neural]
---

## Definition
The set of techniques for capturing, modeling, and rendering the visual appearance of digital human skin — encompassing geometry (wrinkles, pores, displacement), reflectance (albedo, specular BRDF, subsurface scattering), and multi-modal texture maps that drive photoreal rendering. Distinct from deformation/rigging, but tightly coupled with face texture and geometry pipelines.

## Variants / Taxonomy

### Measurement-Based Capture
Acquire per-subject reflectance from multi-light / multi-camera rigs. Outputs spatially-varying BRDFs, albedo maps, specular maps, subsurface scattering coefficients.
- Key paper: [[papers/weyrich-2006-skin-reflectance]]

### Generative Models
Learn a generative distribution over appearance from captured datasets. Enable synthesis of novel subjects, appearance editing, and data augmentation.
- Key paper: [[papers/gruber-2024-gantlitz]] — StyleGAN producing 4K multi-modal face textures

### Neural Geometry
Learned non-linear face shape representations (VAE, PCA) replacing linear blendshape bases for per-subject reconstruction and parameterization.
- [[papers/bagautdinov-2018-facial-cvae]] — compositional VAE for face geometry
- [[papers/feng-2021-deca]] — FLAME + per-identity neural displacement; wrinkles conditioned on expression; in-the-wild images
- [[papers/danecek-2022-emoca]] — emotion-faithful FLAME reconstruction from monocular video

### Neural Avatar Rendering (3DGS / NeRF)
Real-time photorealistic rendering of parametrically controlled face avatars using neural representations.
- [[papers/qian-2024-gaussian-avatars]] — 3DGS bound to FLAME triangles; rig-driven real-time rendering
- [[papers/ma-2024-gaussian-blendshapes]] — Gaussian blendshape bases; ~370 fps; high-frequency detail beyond mesh rigs
- [[papers/giebenhain-2024-npga]] — NPHM-conditioned Gaussian avatars; +2.6 dB PSNR over prior methods
- [[papers/zhuang-2022-mofanerf]] — morphable NeRF face model; shape/expression/appearance in one MLP
- [[papers/yu-2023-nofa]] — one-shot NeRF avatar from single image via EG3D GAN inversion
- [[papers/ding-2023-diffusionrig]] — diffusion model conditioned on FLAME rig for personalized appearance editing

### Rendering Integration
Multi-modal maps (albedo, specular, displacement, normals) consumed by standard rendering pipelines (path tracing, RSL/OSL shaders). Displacement maps tiled for skin pore detail.

## Multi-Modal Map Types
| Map | Content | Resolution |
|-----|---------|-----------|
| Albedo | Diffuse reflectance color | 4K+ |
| Specular attenuation | Specularity modulation | 4K+ |
| Displacement | Sub-mm surface geometry (pores, wrinkles) | 4K+ tiled |
| Normals | Surface orientation for shading | 4K+ |
| Subsurface scattering | Mean free path per-region | lower res |

## Key Papers
- [[papers/weyrich-2006-skin-reflectance]] — first large-scale (149-subject) measured face appearance database; BSSRDF model
- [[papers/gruber-2024-gantlitz]] — generative 4K multi-modal face textures (albedo/specular/displacement/normals)
- [[papers/bagautdinov-2018-facial-cvae]] — compositional VAE face geometry; non-linear learned parameterization

## Connections
- [[concepts/wrinkle-systems]] — expression-dependent appearance variation
- [[papers/raman-2022-mesh-tension-wrinkles]] — tension-driven wrinkle texture blending at runtime

## Notes
The measurement modalities established by Weyrich 2006 (albedo, specular, subsurface) remain standard in digital human pipelines nearly 20 years later. GANtlitz (2024) generates the same map types at 4K using a generative model instead of per-subject capture, dramatically reducing cost. Mobile phone capture + NeRF reconstruction now achieves comparable per-subject fidelity to the original multi-light rig approach.
