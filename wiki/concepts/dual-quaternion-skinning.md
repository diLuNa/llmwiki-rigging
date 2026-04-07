---
title: "Dual Quaternion Skinning (DQS)"
tags: [skinning, dqs, lbs, dual-quaternion]
---

## Definition
A skinning algorithm that blends bone transforms as dual quaternions rather than matrices. A dual quaternion $\hat{q} = q_0 + \epsilon q_e$ encodes both rotation ($q_0$) and translation ($q_e$) as a single algebraic object.

## How it fixes candy-wrapper
Matrix blending can produce non-rigid results because the average of rotation matrices is not a rotation matrix. Dual quaternion blending stays on the rigid transform manifold (after normalization), so volume is preserved.

## Bulging artifact
DQS introduces its own artifact: unnatural volume addition at certain joint configurations. This is generally less objectionable than candy-wrapper but noticeable at extreme poses.

## Key Papers
- [[papers/kavan-2007-dqs]] — original formulation

## Connections
- [[concepts/linear-blend-skinning]]

## Notes
Sign flip: before blending, ensure all dual quaternions are in the same hemisphere (flip if dot product with the dominant quaternion is negative).
