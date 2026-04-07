---
title: "CANRIG: Cross-Attention Neural Face Rigging with Variable Local Control"
authors: [Arad, Eran; (ETH Zürich; Disney Research — equal contribution authors)]
venue: Eurographics 2026 (Computer Graphics Forum)
year: 2026
tags: [neural, rig-generation, blendshapes, digital-human, skinning]
source: raw/papers/CANRIG-Cross-Attention-Neural-Face-Rigging-with-Variable-Local-Control-Paper.pdf
---

## Summary
CANRIG is a neural face rigging system that uses cross-attention to learn spatially localized face rig control — allowing variable levels of local vs. global deformation influence per control. The key innovation is conditioning the deformation prediction on both the rig control values and spatial attention masks, so each control acts locally in some regions and globally in others without manual specification of influence regions.

## Problem
Classical face rigs define explicit influence regions per control (e.g. the left-lip raiser only affects the left upper lip). This requires manual setup and limits expressiveness. Neural face rigs (e.g. CANRIG's predecessors) tend to be either fully global (all controls influence all vertices) or require manually specified locality. An automatic way to learn the right level of locality per control — from data — would reduce rigging labor and improve quality.

## Method
CANRIG's core idea: use **cross-attention** between rig control values and mesh vertex positions to dynamically determine which controls influence which vertices.

**Architecture overview:**
- Input: rig control vector $c \in \mathbb{R}^C$ (blendshape weights or joint angles); mesh geometry.
- **Control encoder**: maps each control $c_i$ to a key-value pair in the attention mechanism.
- **Vertex encoder**: maps each vertex (position + local geometry features) to a query vector.
- **Cross-attention layer**: each vertex query attends to all control keys; attention weights determine how much each control influences each vertex.
  - High attention weight → strong local influence
  - Near-zero attention → control has no effect at this vertex
- **Decoder**: per-vertex displacement from the attended control features.
- **Final deformation**: $\Delta V = \text{decoder}(\text{cross\_attention}(V_\text{query}, C_\text{key}, C_\text{value}))$

**Variable local control:**
The attention weights are not manually specified — they are learned from training data (posed mesh sequences). Some controls will learn to have narrow, localized attention patterns; others will be global.

**Conditioning:**
The system does NOT sacrifice global conditioning: by allowing cross-attention to span all vertices and all controls, global effects (head rotation, jaw open that moves the whole face) are naturally captured alongside local effects (individual muscle activations).

## Key Results
- Learns spatially correct influence regions per control without manual specification.
- Outperforms baseline MLP rigs on localized expression quality.
- Global and local effects are naturally separated — interpretable attention maps.
- Demonstrated on high-resolution face rigs (ETH Disney-style digital human meshes).

## Limitations
- Requires a dataset of rig evaluations (posed meshes at various control values) for training.
- Inference speed depends on mesh size and number of controls (quadratic attention).
- Attention masks are emergent — may not perfectly align with artist intuition for every control.

## Connections
- [[papers/li-2021-neural-blend-shapes]] — similar goal (automate blend shape learning); CANRIG is face-specific with explicit rig control structure
- [[papers/choi-2022-animatomy]] — production face rig architecture that CANRIG could improve or replace
- [[papers/radzihovsky-2020-facebaker]] — FaceBaker bakes a face rig to a neural function; CANRIG provides the learned rig itself
- [[papers/bailey-2018-deep-deformation]] — neural approximation of character rigs; CANRIG targets face-specific controllability
- [[concepts/blendshapes]] — rig controls $c_i$ are blendshape-style weights driving the cross-attention
- [[concepts/rig-inversion]] — CANRIG's inverse would map target mesh → control values
- [[authors/black-michael]] — Disney Research affiliation in the author list connects to MPI-IS body model work
