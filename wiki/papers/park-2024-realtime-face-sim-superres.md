---
title: "Real-Time Physics-Based Facial Animation via Super-Resolution"
authors: [Park, Hyojoon; Kim, Woojong; Kim, Chul-Ho; Park, Minseok]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [simulation, digital-human, blendshapes, neural, real-time]
source: raw/papers/park-2024-realtime-face-sim-superres.pdf
---

## Summary
Proposes a **neural super-resolution** approach to enable real-time physics-based facial simulation. A coarse physics simulation runs in real-time at low resolution; a neural network trained on high-resolution FEM simulation data upsamples the coarse result to production-quality geometry. This separates the real-time component (coarse physics) from the high-quality component (learned upsampling), achieving fast inference without sacrificing visual quality. SIGGRAPH 2024.

## Problem
High-resolution FEM face simulation (production quality) is too slow for real-time applications (~minutes per frame). Low-resolution simulation runs faster but lacks surface detail (fine wrinkles, pores, thin features). A neural bridge from low-res to high-res simulation would unlock real-time physics-quality face animation.

## Method
**System:**
1. **Coarse simulation:** low-resolution FEM face mesh (e.g., ~1K triangles) runs at real-time rates (>30 fps)
2. **Neural super-resolution network:** U-Net or transformer architecture; maps coarse mesh deformation → high-resolution surface prediction
3. **Training data:** pairs of (coarse simulation output, corresponding high-resolution FEM simulation) generated offline
4. **Input features:** coarse vertex positions, velocities, mesh connectivity; optional: muscle activation values
5. **Output:** high-resolution vertex displacements on a fixed high-resolution template mesh (~100K triangles)

**Network design:** operates on mesh surfaces using graph convolution or UV-mapped features; trained to predict fine-scale wrinkles and deformation details conditioned on the coarse physics state.

## Key Results
Demonstrated real-time (>30fps) inference with visual quality close to high-resolution FEM ground truth. Fine wrinkles, pores, and skin deformation details recovered by the super-resolution step. Significant speed improvement over direct high-resolution simulation. SIGGRAPH 2024.

## Limitations
Super-resolution is a learned approximation — can hallucinate high-frequency details not present in the coarse simulation. Training data must cover the target character and expression range. Not a true physics simulation: does not conserve energy or respect material constraints beyond what the coarse model approximates.

## Connections
- [[papers/teran-2005-quasistatic-flesh]] — FEM simulation providing training targets
- [[papers/wagner-2023-softdeca]] — related: adding physics to neural face fitting
- [[papers/ichim-2017-phace]] — full physics face model (offline)
- [[papers/yang-2023-implicit-physical-face]] — related: implicit face model with physics
- [[concepts/muscles]] — context: real-time physics simulation for muscle-driven face animation
- [[authors/park-hyojoon]]
