---
title: "Motion Synthesis"
tags: [motion-synthesis, animation, neural, reinforcement-learning, crowd]
---

## Definition
Motion synthesis is the automated generation of character motion — joint trajectories, poses, or full-body animations — from control signals such as user input, task goals, speech, or physical constraints. Distinct from motion capture (which records real motion) and motion editing (which modifies existing clips); synthesis creates plausible motion from scratch or from sparse constraints.

## Variants / Taxonomy

### Physics-Based Synthesis
Characters are simulated bodies governed by equations of motion; a controller outputs joint torques to achieve a task. Enforces physical plausibility (no foot sliding, realistic mass distribution) at the cost of simulation complexity.
- **Reinforcement learning**: train a policy to apply torques by maximizing a reward signal. [[papers/peng-2021-amp]] uses adversarial motion priors to match reference motions while satisfying task objectives.

### Data-Driven / Statistical Synthesis
Learns a mapping from context (phase, style, goal) to motion from a large corpus of mocap data.
- Phase-functioned neural networks, motion graphs, motion matching (no wiki paper yet)
- Style transfer across characters: [[papers/aberman-2020-unpaired-motion-style]]

### Neural Generative Synthesis
Uses generative models (VAEs, diffusion, transformers) to sample diverse, plausible motions.
- Diffusion-based: [[papers/zheng-2025-autokeyframe]]
- Transformer-based: [[papers/chen-2024-taming-diffusion]]

### Retargeting-Based Synthesis
Takes motion from one character and maps it to a differently-proportioned target while preserving style and contacts.
- [[papers/aberman-2020-skeleton-aware-retargeting]] — skeleton-aware retargeting

### Crowd / Locomotion Synthesis
Generates motion for many characters simultaneously, often using parameterized gaits or state machines.
- [[papers/nam-2023-bidirectional-gaitnet]] — bidirectional gait blending

### Speech-Driven Synthesis
Generates facial or full-body animation from audio input.
- [[papers/peng-2023-emotalk]] — emotion-driven talking head

## Key Papers
- [[papers/peng-2021-amp]] — adversarial motion priors for physics-based synthesis
- [[papers/aberman-2020-unpaired-motion-style]] — unpaired motion style transfer
- [[papers/aberman-2020-skeleton-aware-retargeting]] — skeleton-aware retargeting
- [[papers/nam-2023-bidirectional-gaitnet]] — bidirectional gait networks
- [[papers/chen-2024-taming-diffusion]] — diffusion-based motion generation
- [[papers/zheng-2025-autokeyframe]] — automatic keyframe generation
- [[papers/tang-2024-decoupling-contact]] — decoupling contact for synthesis

## Connections
- [[concepts/rig-inversion]] — motion synthesis outputs skeleton poses; rig inversion maps these back to rig parameter space for hero character polish
- [[concepts/skinning]] — synthesized poses must be skinned to produce surface deformation
- [[concepts/blendshapes]] — facial motion synthesis often targets blendshape weight vectors

## Notes
Motion synthesis and rig inversion are tightly coupled in production: crowd systems synthesize motion in skeleton space, then rig inversion converts to rig parameters for close-up shots requiring full-rig deformation. See [[techniques/inverse-rig-mapping]].
