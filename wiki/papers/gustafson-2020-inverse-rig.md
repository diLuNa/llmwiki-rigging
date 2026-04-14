---
title: "Analytically Learning an Inverse Rig Mapping"
authors: [Gustafson, Stephen; Lo, Aaron; Kanyuk, Paul]
venue: SIGGRAPH Talks 2020
year: 2020
tags: [rig-generation, neural, pose-space, math]
source: raw/papers/2020.SiggraphTalks.GLK.pdf
---

## Summary
Solves the rig inversion problem — mapping skeleton poses back to high-level rig control parameters — at real-time rates by learning an analytic approximation of the rig's Jacobian offline. Enables crowd systems to apply procedural skeleton edits that transfer cleanly to the full character rig for polish.

## Problem
Motion synthesis and crowd systems operate on skeleton joint angles, but Pixar's hero rigs are controlled by high-level abstract parameters (sliders, blend weights, etc.) that don't map directly to skeleton transforms. Inverting this mapping with iterative least-squares requires an expensive rig Jacobian computation per frame.

## Method
1. Offline: learn an analytic approximation of the rig's mapping $f: \text{rig params} \to \text{skeleton poses}$ using a regression/sampling approach.
2. At runtime: use the analytic approximation to compute the Jacobian cheaply, then run standard iterative least-squares (e.g., Gauss-Newton) to find rig parameters matching a target skeleton pose.
The analytic Jacobian is derived from the learned approximation, making per-frame Jacobian evaluation effectively free.

## Key Results
- Real-time rig inversion on full hero characters.
- Enables crowd department to use procedural skeleton edits close-to-camera with reliable transfer to full-rig polish.
- Outperforms hard-coded heuristic approaches in maintainability and generality.

## Limitations
- Learned approximation introduces error for poses far from the training distribution.
- Requires offline training data collection (rig sampling).

## Connections
- [[papers/holden-2015-inverse-rig]] — seminal prior work; learned direct inverse mapping via MLP
- [[papers/holden-2017-inverse-rig-tvcg]] — extended journal version of Holden 2015; adds GPR
- [[papers/marquis-bolduc-2022-differentiable-rig]] — complementary approach for black-box rigs where operators cannot be classified (uses differentiable rig approximation + mesh loss)
- [[papers/radzihovsky-2020-facebaker]] — related rig approximation via ML
- [[concepts/rig-inversion]]
- [[authors/kanyuk-paul]]

## Implementation Notes
Rig inversion is useful beyond crowds — any system that needs to convert motion-capture or procedurally generated skeletons to rig-control space benefits from this. The offline learning step can be framed as a sparse polynomial or neural network regression.
