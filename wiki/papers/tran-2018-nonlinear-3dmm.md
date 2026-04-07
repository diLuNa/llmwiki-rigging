---
title: "Nonlinear 3D Face Morphable Model"
authors: [Tran, Luan; Liu, Xiaoming]
venue: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2018)
year: 2018
tags: [neural, digital-human, blendshapes, rig-generation]
source: raw/papers/1804.03786v3.pdf
---

## Summary
Replaces the linear PCA basis of classical 3DMMs with a convolutional encoder-decoder network, learning a nonlinear face shape and texture space from large 2D image datasets (no 3D supervision required at training time). The model retains the explicit decomposition of identity and expression components while allowing much richer shape variation than linear PCA.

## Problem
Linear 3DMMs (Basel Face Model, Surrey Face Model) use PCA — which can only represent a Gaussian distribution of faces — and require expensive 3D scan datasets for training. A nonlinear model learned from the far more plentiful 2D image data would capture the true non-Gaussian distribution of face shapes and textures.

## Method
**Architecture:**

The nonlinear 3DMM replaces the linear PCA decoder with a convolutional network:

- **Encoder** $E$: CNN that maps a 2D face image $I$ to shape+texture latent codes $(\alpha_\text{id}, \alpha_\text{exp}, \alpha_\text{tex})$.
- **Shape decoder** $f_S$: MLP/CNN that maps $(\alpha_\text{id}, \alpha_\text{exp})$ to a 3D face mesh (vertex positions). In the nonlinear model, $f_S$ is a neural network instead of a linear matrix multiplication.
- **Texture decoder** $f_T$: maps $\alpha_\text{tex}$ to face albedo.
- **Differentiable renderer**: projects the 3D mesh to 2D, enabling training on 2D images with photometric loss.

**Training pipeline (weakly supervised on 2D images):**
1. Encode image $I \to \alpha$.
2. Decode mesh $S = f_S(\alpha_\text{id}, \alpha_\text{exp})$.
3. Render to 2D using camera parameters.
4. Minimize photometric loss + landmark loss (2D facial landmarks vs rendered projections) + regularization.

No 3D scan supervision needed — landmarks and photometric consistency drive the learning.

**S/T (Source/Target) training**: pairs of images from the same identity (different expressions) or different identities ensure the latent decomposition is semantically meaningful.

## Key Results
- Better reconstruction of faces with extreme expressions, wrinkles, and non-Gaussian shapes.
- Trained on ~500k in-the-wild face images — much larger scale than scan-based models.
- Competitive reconstruction accuracy vs linear 3DMMs, with qualitatively much richer variety.

## Limitations
- The learned latent space is less interpretable than linear PCA (no direct semantic axis per component).
- Identity/expression disentanglement is softer than in scan-trained models with paired sequences.
- Texture model is limited by the in-the-wild training data quality.

## Connections
- [[papers/ranjan-2018-coma]] — CoMA approaches the same problem from the mesh generation side; Nonlinear 3DMM learns from 2D images
- [[papers/li-2017-flame]] — FLAME is the linear parametric model; this work replaces its linear basis with a CNN
- [[papers/zheng-2022-imface]] — ImFace takes the nonlinearity further with implicit representations
- [[papers/bagautdinov-2018-facial-cvae]] — similar goal (nonlinear face geometry model) using a compositional VAE
- [[concepts/digital-human-appearance]] — face shape model learned from wild data
- [[concepts/blendshapes]] — the expression decoder $f_S(\alpha_\text{exp})$ is a nonlinear blendshape system
