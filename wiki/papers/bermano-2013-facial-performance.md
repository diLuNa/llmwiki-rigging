---
title: "Facial Performance Enhancement Using Dynamic Shape Space Analysis"
authors: [Bermano, Amit; Bradley, Derek; Beeler, Thabo; Zund, Fabio; Nowrouzezahrai, Derek; Baran, Ilya; Sorkine-Hornung, Olga; Pfister, Hanspeter; Sumner, Bob; Bickel, Bernd; Gross, Markus]
venue: ACM Transactions on Graphics (TOG) 2013
year: 2013
tags: [blendshapes, facial-capture, digital-human, neural]
source: ~no local PDF~
---

## Summary
Enhances the quality of facial performance capture by analyzing the statistical distribution of face shapes over time (dynamic shape space). Low-quality or missing tracking frames are reconstructed by finding the most probable shape given the learned shape manifold and temporal context. Effectively denoises and fills gaps in performance capture data.

## Problem
Facial performance capture produces noisy or incomplete tracking data — self-occlusions, lighting failures, and rapid motion cause tracking failures. Standard temporal filtering loses expression detail; purely geometric approaches ignore the statistical structure of face motion.

## Method
**Shape space learning:** PCA or nonlinear manifold model learned from a corpus of correctly-tracked face shapes. Captures the distribution of plausible facial configurations for the specific actor.

**Dynamic analysis:** Temporal model captures how the face transitions through shape space over time — accounting for motion dynamics and natural transition probabilities.

**Enhancement / completion:** Noisy or missing frames are replaced by the maximum-likelihood shape given:
1. The learned shape manifold (plausibility constraint).
2. Neighboring frames in shape space (temporal coherence).
3. Partial observations (e.g., visible portion of face).

**Output:** Cleaned blendshape weight trajectories or corrected mesh sequences ready for production.

## Key Results
- Significantly improved tracking quality on real performance capture data.
- Robust gap-filling on occluded or failed frames.
- Temporal coherence preserved without over-smoothing expression detail.

## Limitations
- Requires a large corpus of per-actor training data for shape space learning.
- PCA shape space may not generalize to extreme expressions outside training distribution.
- Does not model muscle anatomy — purely data-driven.

## Connections
- [[papers/bagautdinov-2018-facial-cvae]] — learned face shape spaces using VAE (neural successor)
- [[papers/choi-2022-animatomy]] — anatomy-driven alternative for facial shape space
- [[concepts/blendshapes]] — the representation cleaned/enhanced by this system
- [[authors/beeler-thabo]] — co-author
- [[authors/sorkine-olga]] — co-author

