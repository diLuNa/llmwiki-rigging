---
title: "Hand Animation"
tags: [hand-animation, neural, motion-synthesis]
---

## Definition
Techniques for animating and synthesizing dexterous hand motion — including finger articulation, grasping interaction with objects, and hand deformation. Spans traditional keyframe rigging, motion capture retargeting, data-driven synthesis, and reinforcement learning.

## Variants / Taxonomy

### Keyframe / Rig-Based
Traditional animator-driven approach. Hand rigs typically use FK/IK hierarchies on 15–20 joints with corrective shapes for knuckle volumes. Not covered deeply in this wiki.

### Motion Capture Retargeting
Optical/glove-based capture; retargeting to character hand topology. Requires careful skeleton proportioning.

### Data-Driven Grasp Synthesis
Learn grasp pose distributions from datasets; at inference time, generate plausible grasps given an object.
- Key paper: [[papers/cao-2024-multimodal-grasp]] — diffusion model for hand+object grasp generation

### RL-Based Motion Synthesis
Reinforcement learning policies synthesize full approach + grasp motion, generalizing to unseen objects without 3D interaction data.
- Key paper: [[papers/zhang-2024-graspxl]] — GraspXL, 500k+ object generalization at 82.2% success

### Hand Parametric Models
MANO — blend skinning model of the hand with non-rigid per-subject shape; standard in grasp datasets and neural methods. Related to SMPL body model.

## Key Papers
- [[papers/zhang-2024-graspxl]] — RL policy for grasping diverse objects at scale
- [[papers/cao-2024-multimodal-grasp]] — multi-modal diffusion for hand-object grasp generation

## Connections
- [[concepts/linear-blend-skinning]] — underlying deformation for most hand rigs
- [[concepts/blendshapes]] — corrective shapes for hand knuckle volumes

## Notes
Hand animation is a distinct sub-field from body/face rigging. The MANO model is the de facto parametric hand representation in the machine learning community (analogous to FLAME for faces or SMPL for bodies). Production hand rigs are typically proprietary and rely heavily on corrective blendshapes at joint extremes.
