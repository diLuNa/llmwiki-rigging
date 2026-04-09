---
title: "Neuromuscular Control of the Face"
authors: [Zeng, Xiao; Liu, Minchen; Li, Chenfanfu; Komura, Taku; Wen, Cheng]
venue: ACM Transactions on Graphics (SIGGRAPH 2021)
year: 2021
tags: [muscles, simulation, digital-human, neural]
source: raw/papers/zeng-2021-neuromuscular-face.pdf
---

## Summary
Introduces a **neuromuscular control model** for the human face that integrates neural motor control (how the brain activates muscles) with physics simulation (how muscles deform tissue). A recurrent neural network learns the neuromuscular controller: given a target expression, it outputs a sequence of muscle activation commands that, when applied to an FEM face model, smoothly transitions to the target while respecting biomechanical constraints (activation limits, co-contraction patterns). SIGGRAPH 2021.

## Problem
Existing muscle-driven face simulation models either require hand-specified activation sequences (impractical) or solve inverse problems from markers/video (requires capture equipment). A learned controller could bridge the gap: given a desired expression, automatically compute physiologically plausible muscle activation trajectories.

## Method
**System overview:**
1. **FEM face model:** simplified physics model (Neo-Hookean tissue, transversely isotropic muscles) — serves as the physics environment
2. **Neural controller:** recurrent network (LSTM or similar) maps current face state + target expression → muscle activation increments $\Delta \mathbf{a}(t)$
3. **Training via reinforcement learning or imitation learning:** controller trained to reach target expressions from the expression scan dataset while minimizing control effort, avoiding co-contractions, and respecting activation bounds $\mathbf{a} \in [0,1]^M$

**Biomechanical constraints modeled:**
- Activation bounds: $a_k \in [0, 1]$ per muscle
- Co-activation penalties: penalize simultaneous activation of antagonistic muscles (e.g., cheek raise + cheek depress)
- Temporal smoothness: penalty on rapid activation changes (physiological motor control is smooth)

**Expression targets:** any facial expression (from scan, video, or generated) can be used as target.

## Key Results
Demonstrated smooth, physiologically plausible transitions between arbitrary expression targets without per-target hand-specification of activation sequences. Co-contraction patterns match expected anatomy (synergistic muscles activate together, antagonists anti-correlate). SIGGRAPH 2021.

## Limitations
Simplified FEM model (not full MRI anatomy) for tractability of RL training. RL training is slow and unstable with high-dimensional muscle activation space. No contact modeling. Limited to face (full head including tongue not modeled). Generalization to expressions far from training set is uncertain.

## Connections
- [[papers/teran-2005-quasistatic-flesh]] — FEM engine for physics environment
- [[papers/sifakis-2005-anatomy-muscles]] — manual muscle activation recovery; this work learns a controller instead
- [[papers/bao-2019-face-capture-muscles]] — video-based muscle activation; complementary capture method
- [[papers/ichim-2017-phace]] — physics face model architecture similar to the one used here
- [[concepts/muscles]] — learned neuromuscular face controller
- [[authors/zeng-xiao]]
