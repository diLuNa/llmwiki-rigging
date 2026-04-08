---
title: "EMOCA: Emotion Driven Monocular Face Capture and Animation"
authors: [Danecek, Radek; Black, Michael J.; Bolkart, Timo]
venue: CVPR 2022
year: 2022
tags: [neural, digital-human, blendshapes, facial-capture, appearance]
source: raw/papers/2204.11312.pdf
---

## Summary
EMOCA extends DECA-style monocular FLAME reconstruction with a deep perceptual emotion consistency loss — a pretrained affect classifier enforces that the reconstructed 3D expression conveys the same emotional state as the input image. Standard photometric reconstruction losses are insufficient for faithful expression recovery; the emotional perceptual term fills the gap. EMOCA also regresses valence/arousal and basic expression categories directly from FLAME parameters, demonstrating that 3D geometry carries usable affective signal.

## Problem
Monocular 3D face reconstruction methods (DECA, Deep3D) optimize photometric and landmark losses that do not penalize emotionally wrong expressions — a reconstructed face can look plausible geometrically while conveying the wrong emotion. For applications in animation, performance retargeting, and affective computing, emotional fidelity is as important as geometric accuracy.

## Method
**Base:** DECA encoder-decoder (FLAME shape $\beta$, expression $\psi$, pose $\theta$, lighting, albedo).

**Emotion consistency loss:**
```math
\mathcal{L}_\text{emo} = \| E_\text{aff}(\hat{I}) - E_\text{aff}(I) \|_2
```
where $E_\text{aff}$ is a pretrained affect recognition network (AffectNet-trained ResNet50), $I$ is the input image, and $\hat{I}$ is the differentiably rendered output. The loss pulls the predicted expression $\psi$ to match not just the pixel distribution but the emotional semantics.

**Emotion regression head:** An additional MLP on top of FLAME $\psi$ parameters predicts valence, arousal, and 8 basic emotion classes.

Training on VGGFace2 + AffectNet + VoxCeleb. FLAME expression space is the latent for all downstream tasks.

## Key Results
- Significantly better expression quality than DECA on in-the-wild images, especially for subtle and asymmetric expressions.
- 3D geometry-based emotion recognition performs comparably to image-based methods on wild data.
- Established a new evaluation axis (emotional fidelity) for 3D face reconstruction.
- EMOCA v2 incorporates MICA identity prior ([[papers/zielonka-2022-mica]]) for better identity disentanglement.

## Limitations
- Still constrained to FLAME expression space (52 expression PCA coefficients) — cannot represent detail beyond FLAME's capacity.
- Emotion loss is supervision, not constraint — the emotion space alignment can still fail for extreme or culturally specific expressions.
- Requires differentiable renderer; training is heavier than standard reconstruction baselines.

## Connections
- [[concepts/nonlinear-face-models]] — EMOCA is a FLAME-based reconstruction method with a perceptual expression loss
- [[concepts/facial-blendshape-rigs]] — FLAME expression parameters serve as the rig output
- [[papers/feng-2021-deca]] — EMOCA extends DECA with emotional supervision
- [[papers/li-2017-flame]] — FLAME is the underlying parametric model
- [[papers/zielonka-2022-mica]] — MICA provides better identity prior used in EMOCA v2
- [[papers/retsinas-2024-smirk]] — SMIRK further improves in-the-wild expression reconstruction
- [[authors/black-michael]]
- [[authors/bolkart-timo]]

## Implementation Notes
The key practical contribution is the affect loss as a plug-in training signal — it can be added to any differentiable face reconstruction pipeline. AffectNet pretrained weights are publicly available. The FLAME expression coefficients $\psi \in \mathbb{R}^{50}$ remain the output; no change to rig format.
