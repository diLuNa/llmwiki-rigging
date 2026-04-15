---
title: "Learning Free-Form Deformations for 3D Object Reconstruction"
authors: [Jack, Dominic; Pontes, Jhony K.; Sridharan, Sridha; Fookes, Clinton; Shirazi, Sareh; Maire, Frederic; Eriksson, Anders]
venue: ACCV 2018 (Asian Conference on Computer Vision)
year: 2018
tags: [neural, deformation, cage-deformation, rig-generation, math]
source: https://arxiv.org/abs/1803.10932
---

## Summary
Trains a neural network to predict free-form deformation (FFD) control point displacements for single-image 3D object reconstruction. Unlike methods that predict per-vertex displacements directly, FFD parameterization provides smooth, compact deformation representations that generalize better across shape instances. Achieves state-of-the-art on ShapeNet point-cloud and volumetric metrics using a template deformation approach.

## Problem
Per-vertex neural deformation predictions for 3D reconstruction suffer from: high dimensionality (scale with mesh resolution), lack of spatial coherence (each vertex predicted independently), and no guarantee of smooth surfaces. FFD provides a low-dimensional proxy that produces smooth, spatially coherent deformations from a small number of predicted values.

## Method

### Differentiable FFD Layer
A regular control lattice of $L \times M \times N$ control points is placed around a template shape. The network predicts displacements $\Delta\mathbf{P}_{ijk}$ for each control point. Template point positions are deformed via the Bernstein evaluation:

```
P_def = P_template + Σ_{i,j,k} Bern(i,j,k | s,t,u) · ΔP_{ijk}
```

The key property: gradients $\partial \text{Loss}/\partial \Delta\mathbf{P}_{ijk}$ flow directly through the Bernstein basis evaluation, which is a fixed linear operator.

### Architecture
- Encoder: ResNet or VGG pretrained on ImageNet, producing a latent shape code from the input image
- Decoder: MLP predicting $3 \times (L+1)(M+1)(N+1)$ control point displacements
- FFD layer: applies predicted displacements to template points (differentiable)
- Loss: Chamfer distance between deformed template and ground-truth point cloud

### Template Selection
One template per ShapeNet category. The template is a canonical shape (e.g., average airplane, chair, car) that the FFD must deform to match any instance in that category.

## Key Results
- State-of-the-art on ShapeNet 3D reconstruction benchmarks (point cloud metrics: Chamfer distance; volumetric metrics: IoU)
- Smooth, artifact-free surface deformations from small (e.g., $4^3 = 64$) control point lattices
- Better generalization than per-vertex prediction, particularly for unseen shapes

## Limitations
- Single template per category limits expressiveness for highly varied shape categories
- Bernstein basis has global support: sparse shapes (e.g., a chair with thin legs) may produce compromises where the lattice creates undesired coupling
- No self-intersection prevention in the FFD layer

## Connections
- [[papers/sederberg-1986-ffd]] — the FFD technique made differentiable
- [[papers/kurenkov-2017-deformnet]] — concurrent differentiable FFD approach; similar idea, different retrieval strategy
- [[concepts/b-spline-volumes]] — mathematical foundation

## Implementation Notes
- Code available at time of publication; check project page / arXiv for updated links
- The FFD layer can be implemented in ~30 lines of PyTorch using `torch.einsum` for the trivariate Bernstein basis computation
- Extending to B-spline (local support): replace the dense Bernstein basis matrix with a sparse B-spline matrix — same gradient flow but only nearby control points affect each template point
