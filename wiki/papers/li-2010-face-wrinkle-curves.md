---
title: "Realistic Wrinkle Generation for 3D Face Modeling Based on Automatically Extracted Curves"
authors: [Li, Lin; Liu, Fei; Li, Congbo; Chen, Guoan]
venue: Computers & Graphics 2010
year: 2010
tags: [correctives, wrinkle-systems, digital-human]
source: raw/papers/RealisticWrinkleGenerationFor3DFaceModeling.pdf
---

## Summary
An image-based approach to generating static wrinkle geometry on 3D face models. Extracts wrinkle curves automatically from a 2D face photograph using Canny edge detection, projects them onto a 3D face mesh, then applies three shape control functions — cross-section shape (CSCF), depth attenuation (DAF), and width attenuation (WAF) — to sculpt realistic wrinkle profiles. Adaptive mesh subdivision refines the influence region.

## Problem
Hand-sculpting wrinkles on 3D face models is labor-intensive. Prior approaches require manual curve placement or expensive capture setups. A method to automatically extract and transfer wrinkle geometry from a reference photograph is useful for individualized 3D face reconstruction.

## Method
**Image preprocessing:** Grayscale conversion (linear), noise reduction (transfinite-pixel neighborhood averaging), high-pass sharpening.

**Wrinkle curve extraction:** Improved Canny edge detector on the preprocessed face image, filtered to retain wrinkle-like edges.

**Curve projection:** Feature-point alignment between image and 3D mesh maps extracted curves onto the surface.

**Shape control functions:**
- *CSCF (Cross-Section Shape Control)*: controls wrinkle cross-section profile (e.g. V-shape, U-shape)
- *DAF (Depth Attenuation)*: depth amplitude varies along curve length
- *WAF (Width Attenuation)*: width amplitude varies along curve length

**Adaptive subdivision:** Subdivides mesh in the wrinkle influence region for adequate vertex density before displacement.

## Key Results
- Believable static wrinkles from a single reference photograph.
- Control functions allow artist adjustment of wrinkle character.
- Demonstrated on individualized 3D human face models.

## Limitations
- Static wrinkles only — no expression-driven deformation.
- Fully geometry-based — no texture/normal map output.
- Canny extraction is sensitive to illumination in the source photograph.
- Predates modern capture rigs and neural reconstruction.

## Connections
- [[concepts/wrinkle-systems]] — static geometry-based approach
- [[papers/cutler-2007-art-directed-wrinkles]] — art-directed dynamic wrinkles (contemporary)
- [[papers/raman-2022-mesh-tension-wrinkles]] — modern expression-driven wrinkle blending

