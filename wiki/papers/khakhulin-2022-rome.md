---
title: "ROME: Realistic One-shot Mesh-based Head Avatars"
authors: [Khakhulin, Taras; Sklyarova, Vanessa; Lempitsky, Victor; Zakharov, Egor]
venue: ECCV 2022
year: 2022
tags: [neural, digital-human, blendshapes, facial-capture, appearance, rig-generation]
source: raw/papers/2206.08343.pdf
---

## Summary
ROME reconstructs a person-specific rigged head avatar from a single photograph: it estimates head mesh geometry and a neural texture encoding photometric and geometric detail, then rigs and renders via a trained neural renderer. Uniquely, the mesh is not a fixed 3DMM topology — person-specific geometry deviations are recovered. ROME demonstrates competitive geometry recovery and strong cross-person reenactment quality from a single source image.

## Problem
Subject-specific neural avatars require minutes-to-hours of video capture and training. One-shot methods sacrifice quality. A system that recovers both accurate geometry *and* photorealistic appearance from a single photo — producing a rigged, animatable avatar — would enable scalable avatar creation.

## Method
**Geometry estimation:** From a single image, a mesh-based regressor estimates FLAME parameters plus per-vertex geometry offsets encoding person-specific shape deviations.

**Neural texture:** A neural texture map encodes photometric and fine-grained geometric detail (wrinkles, pores, hair-level) not captured by the mesh alone. Predicted by an image encoder.

**Neural renderer:** A trained warping-based renderer composites the mesh with neural texture under novel poses and expressions. Trained on large in-the-wild video datasets.

**Reenactment:** Given a driving video, FLAME expression coefficients are extracted per-frame and used to animate the source avatar.

## Key Results
- One-shot avatar from a single photo.
- Competitive geometry recovery vs multi-image methods.
- Strong cross-person reenactment — source identity preserved under target expression/pose.

## Limitations
- Neural texture captures per-frame detail but may not generalize to extreme out-of-distribution poses.
- Mesh geometry is FLAME-topology — non-FLAME deviations are approximated by vertex offsets.
- Rendering is neural (warping-based), not physically-based — lighting is baked in.

## Connections
- [[concepts/nonlinear-face-models]] — one-shot mesh+neural-texture avatar
- [[papers/yu-2023-nofa]] — NOFA is a concurrent one-shot method using NeRF/GAN inversion instead of mesh+neural texture
- [[papers/li-2017-flame]] — FLAME geometry backbone
- [[papers/feng-2021-deca]] — DECA is used for FLAME parameter estimation in driving pipeline
