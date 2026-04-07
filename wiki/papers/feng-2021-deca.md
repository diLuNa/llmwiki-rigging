---
title: "DECA: Learning an Animatable Detailed 3D Face Model from In-The-Wild Images"
authors: [Feng, Yao; Feng, Haiwen; Black, Michael J.; Bolkart, Timo]
venue: ACM Transactions on Graphics (SIGGRAPH 2021)
year: 2021
tags: [digital-human, blendshapes, neural, rig-generation, facial-capture, appearance]
source: raw/papers/2012.04012v2.pdf
---

## Summary
DECA (Detailed Expression Capture and Animation) reconstructs a detailed, animatable 3D face from a single in-the-wild image. It extends the FLAME parametric model with a neural detail displacement field that encodes per-identity wrinkles, pores, and high-frequency geometry. Crucially, details are conditioned on both identity and expression parameters so they animate consistently — wrinkles deepen with squinting, smooth out when relaxed. The model trains entirely on unstructured internet images via differentiable rendering.

## Problem
Parametric models (FLAME, 3DMM) capture only coarse shape; raw image-to-3D reconstruction methods entangle texture and geometry detail. No prior method learns expression-dependent high-frequency detail from 2D supervision alone.

## Method
DECA adds a detail branch on top of the FLAME coarse reconstruction pipeline:

**Coarse branch** — regression network estimates FLAME parameters $(\beta, \theta, \psi)$ plus albedo, lighting, and camera from a single image. Reconstruction loss via differentiable rendering.

**Detail branch** — a separate detail code $\delta \in \mathbb{R}^{128}$ per image is encoded by a ResNet-50. A detail decoder $f_\delta$ maps $(\delta, \beta, \psi)$ to per-vertex displacement $D_\text{detail} \in \mathbb{R}^{N \times 3}$ in UV space:
```math
V_\text{detailed} = M(\beta,\theta,\psi) + D_\text{detail}(\delta,\;\beta,\;\psi)
```
Conditioning on $\beta$ (shape) and $\psi$ (expression) makes details identity-consistent and expression-dependent.

**Disentanglement via detail consistency loss:** Two images of the same identity should share a coarse-shape code but can have different detail codes. A soft consistency loss pushes the coarse codes to match across images of the same subject while allowing $\delta$ to capture residual per-image variation.

**Texture synthesis** uses a separate UV texture decoder + adversarial loss to predict detailed albedo maps.

## Key Results
- Reconstructs production-quality wrinkles and pores from a single selfie
- Expression-dependent details animate correctly under novel expressions (crow's feet deepen on squinting)
- Outperforms FLAME-only fitting and DECA-coarse on 3D vertex error across NoW, REALY, and FaceScape benchmarks
- Enables downstream tasks: expression retargeting, face swapping, video reconstruction

## Limitations
- Detail code $\delta$ is global per-image — cannot represent spatially independent details (e.g., one-sided wrinkle)
- Expression-dependent details are limited to the FLAME expression space; exotic non-FLAME deformations don't animate correctly
- Training signal is indirect (rendering loss only) — fine geometry may be inconsistently supervised
- Jaw articulation realism limited by FLAME's 1-DOF jaw joint

## Connections
- [[papers/li-2017-flame]] — DECA's coarse branch is a FLAME regressor; details are built on top
- [[papers/tran-2018-nonlinear-3dmm]] — nonlinear face model; DECA's detail branch is complementary
- [[papers/ranjan-2018-coma]] — CoMA also encodes face geometry; DECA uses 2D supervision instead
- [[papers/ding-2023-diffusionrig]] — DiffusionRig uses DECA reconstruction as conditioning for diffusion
- [[concepts/blendshapes]] — FLAME expression $B_E(\psi)$ is the base expression system
- [[concepts/digital-human-appearance]] — detail geometry and texture synthesis
- [[authors/black-michael]]
