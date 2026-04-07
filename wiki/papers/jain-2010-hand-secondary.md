---
title: "Augmenting Hand Animation with Three-Dimensional Secondary Motion"
authors: [Jain, Eakta; Sheikh, Yaser; Mahler, Moshe; Hodgins, Jessica]
venue: ACM/Eurographics Symposium on Computer Animation (SCA) 2010
year: 2010
tags: [hand-animation, simulation, secondary-motion, correctives]
source: ~no local PDF~
---

## Summary
Adds physically plausible secondary motion (skin stretch, tendon sliding, soft tissue jiggle) to hand animations automatically, using a data-driven model learned from real hand video. The system transfers secondary motion from reference videos to novel animations, enriching hand rigs without manual sculpting or full simulation.

## Problem
Hand animations in production lack the subtle secondary motion — knuckle deformation, skin stretching over bones, tendon sliding — that makes hands look alive. Full simulation is expensive; manual sculpting correctives for hand motions is impractical at scale.

## Method
**Data capture:** High-speed video of real human hands performing various motions. Secondary motion (surface deformation relative to skeleton) extracted via optical flow + reconstruction.

**Statistical model:** Principal components of secondary motion trajectories learned as a function of skeletal pose and velocity.

**Transfer:** Given a new hand animation (joint angles over time), secondary motion components are predicted from the learned model and added to the base deformation.

**Integration:** Secondary motion expressed as mesh displacements atop the kinematic rig deformation.

## Key Results
- Perceptibly more realistic hand animation with automatic secondary motion.
- User study confirms preference for augmented animations.
- Data-driven model generalizes across hand motions not seen in training.

## Limitations
- Requires capturing reference hand video data.
- Statistical model may not extrapolate well to highly unusual hand configurations.
- Surface-level secondary motion only — no volumetric tissue simulation.

## Connections
- [[concepts/hand-animation]] — parent concept
- [[papers/lewis-2000-psd]] — pose-space deformation is the conceptual predecessor
- [[concepts/pose-space-deformation]] — related technique class (pose-driven corrective shapes)

