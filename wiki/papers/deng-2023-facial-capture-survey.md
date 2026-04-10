---
title: "A Survey on the Pipeline Evolution of Facial Capture and Tracking for Digital Humans"
authors: [Deng, Zhigang; et al.]
venue: Multimedia Systems (Springer), 2023
year: 2023
tags: [blendshapes, facial-capture, facs, digital-human, survey, rig-generation]
source: "https://link.springer.com/article/10.1007/s00530-023-01081-2"
---

## Summary
A 2023 survey covering the full pipeline evolution of facial capture and tracking for digital humans, from early marker-based systems through markerless video, to ARKit-based consumer capture and emerging neural methods. Documents how FACS parameterization entered the capture pipeline as an intermediate representation, how ARKit's TrueDepth camera displaced dedicated hardware for many workflows, and the state of the art in neural face reconstruction and retargeting. Serves as the modern update to [[papers/deng-noh-2007-facial-animation-survey]] by the same first author.

## Problem
The facial capture field spans hardware (structured light, depth cameras, markers, RGB), computer vision (face reconstruction, tracking, AU detection), and animation (blendshape solving, retargeting), with no unified reference as of 2023 that integrates all three layers.

## Method
Survey structured around four pipeline stages:
1. **Capture hardware evolution**: optical markers → structured light → RGB-D → ARKit TrueDepth
2. **Facial tracking algorithms**: landmark detection, model fitting (3DMM, FLAME), neural reconstruction
3. **Expression parameterization**: FACS AU detection, blendshape solving, performance retargeting
4. **Digital human integration**: rig driving, real-time delivery (Live Link Face, OpenXR), post-production polish

Key coverage:
- ARKit TrueDepth pipeline as mainstream baseline for consumer capture (60 Hz, 52 weights, on-device)
- FACS as the standard intermediate representation between capture and rig
- Neural face reconstruction methods (DECA, EMOCA, MICA) for markerless video capture
- Real-time retargeting to MetaHuman and custom blendshape rigs

## Key Results
- ARKit has displaced expensive dedicated facial tracking hardware in a large segment of virtual production
- FACS-based intermediate representations (AU weights or FACS-derived blendshape weights) are now standard across academic and production pipelines
- Neural methods (FLAME-fitting, monocular reconstruction) approach marker quality at a fraction of the setup cost
- The 52-weight ARKit parameterization has become the de facto interchange format between capture and rig

## Limitations
- 2023 snapshot: does not cover very recent (2024–2025) neural auto-rigging (RigAnyFace, CANRIG) or Gaussian avatar methods
- Limited coverage of XR-device face tracking (Meta Quest Pro, HTC OpenXR) which emerged 2022–2023
- Survey does not address muscle-based simulation pipelines (Animatomy, ILM FEM) in depth

## Connections
- [[concepts/facs]] — FACS as the standard intermediate representation throughout
- [[concepts/arkit-blendshapes]] — ARKit capture pipeline covered as mainstream baseline
- [[concepts/facial-blendshape-rigs]] — driving production rigs from captured data
- [[concepts/rig-inversion]] — blendshape weight solving from markers/video
- [[papers/deng-noh-2007-facial-animation-survey]] — predecessor survey by same first author (2007)
- [[papers/feng-2021-deca]] — DECA neural face reconstruction covered in survey
- [[papers/danecek-2022-emoca]] — EMOCA expression reconstruction
- [[papers/zielonka-2022-mica]] — MICA metrical identity prior
- [[papers/li-2017-flame]] — FLAME model central to neural reconstruction survey coverage
- [[papers/epic-2021-metahuman-rig]] — MetaHuman as reference production rig system

## Implementation Notes
- The survey's capture hardware comparison table is particularly useful for studio pipeline decisions (cost, framerate, accuracy, setup complexity)
- The FACS-to-rig section discusses the "AU detection → blendshape weight transfer" step that bridges vision-side and rigging-side, useful context for [[papers/faceit-diaz-barros]] and [[papers/jtdp-2003-blendshape-fitting]]
