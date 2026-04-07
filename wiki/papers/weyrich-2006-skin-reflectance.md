---
title: "Analysis of Human Faces using a Measurement-Based Skin Reflectance Model"
authors: [Weyrich, Tim; Matusik, Wojciech; Pfister, Hanspeter; Bickel, Bernd; Donner, Craig; Tu, Chien; McAndless, Janet; Lee, Jinho; Ngan, Addy; Jensen, Henrik Wann; Gross, Markus]
venue: SIGGRAPH 2006
year: 2006
tags: [digital-human, appearance, facial-capture]
source: raw/papers/AnalysisOfHumanFaces.pdf
---

## Summary
Large-scale capture and statistical analysis of 3D face geometry, skin reflectance, and subsurface scattering from 149 subjects. Builds a measurement-based BSSRDF model parameterized per-individual and provides artist tools to edit appearance via population statistics — changing skin type, transferring albedo/BRDF parameters between subjects.

## Problem
Rendering photoreal digital humans requires accurate skin appearance models. Prior work captured single subjects or used fitted analytic BRDFs. No large-scale database of measured face appearance existed to study population variation or enable data-driven editing.

## Method
**Capture rig:** Custom multi-light, multi-camera setup. Per-subject acquisition captures: (1) 3D face geometry via structured light, (2) spatially varying BRDF (bidirectional reflectance) via gradient illumination, (3) subsurface scattering parameters.

**BSSRDF model:** Outgoing radiance integrated over the surface A:
```math
L(x_o,\omega_o) = \int_A \int_\Omega S(x_i,\omega_i,x_o,\omega_o)\,L(x_i,\omega_i)\,(N\cdot\omega_i)\,d\omega_i\,dA(x_i)
```
Each subject's skin is described by: albedo maps (spatially varying reflectance), specular reflectance parameters, and subsurface scattering coefficients (fitted to a multi-layer dipole model).

**Statistical analysis:** PCA over the 149-subject parameter database reveals dimensions of variation (age, gender, ethnicity, skin tone). Artists can edit faces by moving in PCA space or by transferring statistics between subjects.

**Applications:** Skin type transfer, freckle/mole texture synthesis, population-statistics-driven appearance editing.

## Key Results
- First large-scale (149-subject) measured face appearance database.
- Successful appearance transfer between subjects via parameter statistics.
- Validated against ground truth photographs.

## Limitations
- Capture rig is bulky and expensive; not real-time or casual-capture.
- BSSRDF model assumes a specific layered skin structure.
- Static appearance — expression-driven appearance changes not modeled.

## Connections
- [[papers/gruber-2024-gantlitz]] — generative model producing the same multi-modal maps (albedo, specular, displacement) from this lineage
- [[papers/bagautdinov-2018-facial-cvae]] — neural geometry counterpart for face shape
- [[concepts/digital-human-appearance]]

## Implementation Notes
The albedo and specular maps produced by this pipeline are the same modalities targeted by modern face texture generation systems (GANtlitz, etc.). The capture methodology is now substantially democratized — mobile phone capture pipelines and NeRF-based reconstruction achieve similar per-subject fidelity.
