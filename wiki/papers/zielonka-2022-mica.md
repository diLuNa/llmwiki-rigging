---
title: "Towards Metrical Reconstruction of Human Faces"
authors: [Zielonka, Wojciech; Bolkart, Timo; Thies, Justus]
venue: ECCV 2022
year: 2022
tags: [neural, digital-human, blendshapes, facial-capture]
source: raw/papers/2204.06607.pdf
---

## Summary
MICA (MetrIC fAce) trains a FLAME *shape* (identity-only) predictor that produces metrically accurate, expression- and pose-invariant face geometry from a single image. Using ArcFace identity features as input and metric-scale ground-truth supervision from a unified multi-dataset benchmark (2,300+ identities), MICA achieves 15–24% lower shape error than prior state of the art on the NoW benchmark. MICA's identity latents are now standard inputs for downstream expression systems (EMOCA v2, SMIRK).

## Problem
Self-supervised face reconstruction methods (trained on 2D in-the-wild images) cannot recover actual face metric scale due to the perspective projection ambiguity — they learn relative shape proportions, not true dimensions. For applications in medical measurement, avatar creation from a photo, and stable tracking, metric accuracy in the neutral identity shape is essential.

## Method
**Input:** Single face image → ArcFace embedding $\mathbf{f} \in \mathbb{R}^{512}$ (expression/pose invariant by design of face recognition training).

**Architecture:** MLP regressor $g(\mathbf{f}) \to \beta \in \mathbb{R}^{300}$ predicting FLAME shape coefficients.

**Supervision:** Metric 3D scan correspondences from a unified dataset combining multiple small/medium 3D face databases. Scale-consistent ground truth enables absolute metric supervision — not just relative shape.

**Key insight:** Decouples the shape estimation problem from expression and pose (handled by ArcFace invariance) and from appearance (handled by using geometry-only FLAME shape output). Identity is estimated purely from identity-discriminative features.

## Key Results
- 15% lower error on NoW benchmark vs prior SOTA.
- 24% lower error on REALY benchmark.
- Expression- and pose-invariant: works across wide head rotation and extreme expression.
- Widely adopted as a frozen identity backbone in EMOCA v2, SMIRK, and NPGA.

## Limitations
- Only predicts neutral identity shape $\beta$; expression $\psi$ must be estimated separately by a downstream method.
- Metric accuracy requires the face to be visible enough for ArcFace to extract reliable features — heavy occlusion degrades results.
- FLAME shape space limit: 300 PCA coefficients; fine-scale identity detail (pores, wrinkles) not captured.

## Connections
- [[concepts/nonlinear-face-models]] — widely used identity prior in neural face reconstruction pipelines
- [[concepts/facial-blendshape-rigs]] — FLAME shape $\beta$ is the identity basis
- [[papers/li-2017-flame]] — FLAME is the output parametric model
- [[papers/danecek-2022-emoca]] — EMOCA v2 uses MICA identity prior
- [[papers/retsinas-2024-smirk]] — SMIRK builds on MICA
- [[authors/black-michael]]
- [[authors/bolkart-timo]]

## Implementation Notes
MICA is a lightweight add-on to any FLAME-based pipeline: run ArcFace on input image → run MICA MLP → obtain $\beta$. Then run a separate expression/pose estimator initialized with this $\beta$. Pretrained weights publicly available. Inference is near-instantaneous (ArcFace + single MLP forward pass).
