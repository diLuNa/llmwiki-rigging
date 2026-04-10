---
title: "Facial Action Coding System: A Technique for the Measurement of Facial Movement"
authors: [Ekman, Paul; Friesen, Wallace V.]
venue: Consulting Psychologists Press
year: 1978
tags: [blendshapes, facial-capture, rig-generation, digital-human, muscles, facs]
source: "(manual — not a PDF; access via Paul Ekman Group LLC)"
---

## Summary
The original FACS manual defines a comprehensive taxonomy of human facial movement, decomposing any visible expression into a combination of **Action Units (AUs)** — the minimal anatomically distinct movements producible by the face. The 1978 manual (revised 2002) identifies 44 AUs corresponding to individual muscles or muscle groups, plus head/gaze movement descriptors and an A–E intensity scale. FACS is the universal reference vocabulary for CG facial rigging: virtually every production facial rig — and every neural facial model trained on expression data — grounds its parameterization in FACS AUs.

## Problem
Facial movement had no consistent objective vocabulary, making cross-researcher comparison and systematic animation impossible. Prior approaches (categorized emotion labels, holistic gestalt ratings) were subjective and non-decomposable.

## Method
Ekman and Friesen mapped all visible surface facial movements to their underlying anatomical causes (muscle origins), defined the minimal set of distinct movements (AUs), and developed a coding procedure where trained coders assign AU codes + intensity ratings to video frames. The system is learnable by non-anatomists through the FACS manual with training.

**Key structure:**
- **44 Action Units**: upper face (AUs 1–7, 41–46), lower face (AUs 9–28), head movement (AUs 51–57), gaze (AUs 61–65)
- **Intensity codes A–E**: A=trace, B=slight, C=marked/pronounced, D=extreme, E=maximum
- **Bilateral coding**: most AUs can activate independently left (L) and right (R) — e.g., AU12R for right-side smile only
- **Combinations**: any expression = set notation of active AUs, e.g., happiness = AU6+AU12, contempt = AU12R+AU14R (uniquely unilateral)

## Key Results
- Demonstrated that facial expressions of 7 basic emotions (happiness, sadness, surprise, fear, anger, disgust, contempt) have cross-culturally consistent FACS signatures
- FACS provides high inter-rater reliability when coders are trained: >70% agreement on AU occurrence, >80% on intensity
- Became the standard for affective computing, clinical psychology, HCI, and CG facial animation research

## Limitations
- Coding is time-intensive (manual video analysis); automated FACS coding is an active research area
- The universality claim for 7 emotions has been debated; later work (Barrett 2017) argues cultural variation is more significant
- The 2002 revision added new AUs and refinements; some early CG references may cite the 1978 version with a slightly different AU numbering
- Formally covers *visible surface movement* only — it does not prescribe how to achieve AU combinations in synthetic faces

## Connections
- [[concepts/facs]] — dedicated concept page with full AU table and CG mapping
- [[concepts/blendshapes]] — FACS AUs are the canonical parameterization for facial blendshape palettes
- [[concepts/facial-blendshape-rigs]] — production rigs organized around FACS AUs
- [[papers/lewis-2014-blendshape-star]] — surveys how FACS drives blendshape authoring in production
- [[papers/epic-2021-metahuman-rig]] — MetaHuman: full FACS-grounded production rig at scale
- [[papers/choi-2022-animatomy]] — muscle-based alternative: replaces FACS AUs with anatomic strain parameters
- [[papers/qin-2023-nfr]] — Neural Face Rigging: uses FACS as training supervision signal (ICT FaceKit)
- [[papers/waters-1987-muscle-model]] — muscle-based face model predating FACS adoption in CG; Waters later mapped muscles to approximate AU activations

## Implementation Notes
- In a CG rig, each FACS AU typically corresponds to one or two blendshapes (bilateral AUs split L/R)
- Bilateral AUs: AU1, AU2, AU4, AU6, AU7, AU12, AU14, AU15 — all commonly split in production
- Intensity A–E maps to weight [0, 1] in most rigs; some allow negative weights for overshooting
- The 2002 revised manual is the current standard; obtain from [paulekman.com](https://www.paulekman.com/facial-action-coding-system/)
- ICT FaceKit (53 expressions) and ARKit (52 blend shapes) are the most widely used FACS-compatible rigs in research and real-time applications respectively

## Quotes
> "FACS describes facial behavior, not how it is felt or intended, not what it communicates, but what the face does." — Ekman & Friesen, 1978

> "The action coding technique for analyzing facial behavior was derived from an analysis of the musculature of the face, distinguishing what we believe is the full set of distinguishable facial muscular movements." — Ekman & Friesen, 1978
