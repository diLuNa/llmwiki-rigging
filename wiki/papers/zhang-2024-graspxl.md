---
title: "GraspXL: Generating Grasping Motions for Diverse Objects at Scale"
authors: [Zhang, Hui; Christen, Sammy; Fan, Zicong; Hilliges, Otmar; Song, Jie]
venue: ECCV 2024
year: 2024
tags: [hand-animation, neural, motion-synthesis]
source: raw/papers/GraspXL.pdf
---

## Summary
A reinforcement learning policy framework that synthesizes physically plausible, dexterous hand-object grasping motions across diverse object shapes and morphologies — without requiring 3D hand-object interaction data at training or inference time. A single policy trained on 58 objects generalizes to 500k+ unseen shapes at 82.2% success rate.

## Problem
Existing grasp synthesis methods require expensive 3D hand-object datasets and often train object-specific models. Generalizing to unseen object shapes while adhering to multiple motion objectives (approach direction, grasping area, wrist orientation, hand position) remains open.

## Method
**Policy learning:** RL policy (unspecified backbone, likely PPO) takes object geometry + multi-objective specification as input; outputs joint-level hand control.

**No 3D interaction data:** Policy relies only on object surface geometry (SDF or mesh) and reward shaping; no paired grasp annotations needed.

**Multi-objective:** Objectives compose — graspable area, heading direction, wrist rotation, hand position — enabling diverse grasps per object.

**Morphology generalization:** Same framework works for different dexterous hand morphologies (humanoid, robotic).

## Key Results
- 82.2% success rate on 500k+ unseen objects.
- Adherence to user-specified motion objectives (approach direction, grip area).
- Transfers to reconstructed or AI-generated objects.

## Limitations
- Static grasps, not in-hand manipulation.
- Policy success rate degrades on extreme geometries (very thin, highly concave).
- No contact-force modeling — physically correct but not contact-dynamics accurate.

## Connections
- [[papers/cao-2024-multimodal-grasp]] — complementary static grasp generation approach
- [[concepts/hand-animation]] — parent concept

