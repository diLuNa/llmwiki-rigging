---
title: "AnyTop: Character Animation Diffusion with Any Topology"
authors: [Gat, Inbar; Raab, Sigal; Tevet, Guy; Reshef, Yuval; Bermano, Amit H.; Cohen-Or, Daniel]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [neural, motion-synthesis, diffusion, animation, topology-agnostic]
source: arXiv:2502.17327
doi: 10.1145/3721238.3730621
---

## Summary
Diffusion model for motion synthesis across diverse skeletal topologies. Uses topology-agnostic skeleton representation and transformer-based denoising to generate animations for humans, quadrupeds, and arbitrary rigs from text or partial motion. Key contribution: generalization across skeleton types without retraining.

## Problem
Motion synthesis models typically assume fixed skeletal structure. Retraining for each new topology is impractical. Need a unified architecture supporting arbitrary topologies while maintaining motion quality.

## Method
- **Topology-agnostic representation**: Graph-based skeleton encoding invariant to joint count/structure
- **Diffusion decoder**: Transformer-based denoising of motion in latent space
- **Conditioning**: Text, partial motion, or semantic controls

## Key Results
- Generates quality animations for diverse topologies (human, quadruped, custom)
- Text-to-motion, motion inpainting, style control all topology-agnostic
- Comparable quality to topology-specific baselines

## Limitations
- Training requires diverse motion data across topologies (data burden)
- Latent space may not capture all topology-specific nuances
- Inference slower than non-diffusion alternatives

## Connections
- [[papers/zhou-2017-mesh-vae]] — related topology-agnostic mesh learning
- [[papers/taylor-2017-speech-animation]] — speech-driven motion synthesis
- [[papers/li-2021-neural-blend-shapes]] — motion-based shape learning
- [[concepts/auto-rigging]] — downstream rigging for generated motions
- [[concepts/secondary-motion]] — enriching motion with details

## External References
- arXiv: [arxiv.org/abs/2502.17327](https://arxiv.org/abs/2502.17327)
- ACM DL: [doi.org/10.1145/3721238.3730621](https://doi.org/10.1145/3721238.3730621)
