---
title: "Modeling Facial Geometry using Compositional VAEs"
authors: [Bagautdinov, Timur; Wu, Chenglei; Saragih, Jason; Fua, Pascal; Sheikh, Yaser]
venue: CVPR 2018
year: 2018
tags: [neural, blendshapes, facial-capture, digital-human]
source: raw/papers/Bagautdinov_Modeling_Facial_Geometry_CVPR_2018_paper.pdf
---

## Summary
A hierarchical variational autoencoder (VAE) for learning non-linear face geometry representations from 3D scan data. Lower layers capture global face shape; higher layers encode local deformations. The resulting parameterization decomposes the face into semantically meaningful regions and provides a well-behaved latent space suited for face tracking optimization.

## Problem
Linear face models (PCA blendshapes, multilinear models) cannot represent non-linear variations like deep wrinkles or complex local deformations without very large basis sets. Prior non-linear deep learning approaches lack the smooth, optimizable parameter space needed for tracking.

## Method
**Mesh parameterization:** The face mesh is parameterized in UV space, enabling application of convolutional networks directly to mesh geometry (as if it were an image).

**Insight — linear models as shallow autoencoders:** PCA and blendshape models are equivalent to linear autoencoders. Replacing linear encoder/decoder with non-linear (convolutional) ones increases representational power while maintaining the autoencoder structure.

**Compositional architecture:**
- *Global VAE*: convolutional VAE over the full face mesh capturing global shape variation. Latent space is well-behaved for optimization (continuous, regularized via KL divergence).
- *Local VAEs*: separate VAEs per face region (cheeks, forehead, lips, etc.) capturing local deformations not explained by the global model.
- *Composition*: global model defines base shape; local models add residual deformations. Analogous to coarse-to-fine blendshape sets.

The model is trained on a large dataset of 3D face scans from diverse expressions and subjects.

## Key Results
- Non-linear parameterization captures fine facial detail that linear models miss.
- Well-behaved latent space enables face tracking via latent-space gradient optimization.
- Compositional structure provides interpretable, region-specific control — useful for rig-like facial control.

## Limitations
- Requires large-scale 3D scan training data.
- Inference is slower than PCA; not suitable for real-time without a learned inverse.
- The UV parameterization requires a canonical topology.

## Connections
- [[papers/choi-2022-animatomy]] — muscle-based alternative to learned geometry parameterization
- [[papers/radzihovsky-2020-facebaker]] — ML-based rig baking, related goal
- [[papers/holden-2015-inverse-rig]] — rig inversion approach applicable to learned face spaces
- [[concepts/blendshapes]] — the linear baseline this work improves on
- [[concepts/digital-human-appearance]]
