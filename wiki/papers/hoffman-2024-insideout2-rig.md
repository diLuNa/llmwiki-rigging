---
title: "Pixar's Inside Out 2: Character Rig Challenges and Techniques"
authors: [Hoffman, Christian; Nieves, Michael; Speirs, Jacob; Zhang, Brenda Lin]
venue: SIGGRAPH Talks 2024
year: 2024
tags: [rig-generation, correctives, skinning]
source: raw/papers/2024.SiggraphTalks.HNSZ.pdf
---

## Summary
Production talk sharing specific technical challenges and solutions from rigging the characters of *Inside Out 2* (Pixar, 2024), including Joy's four-corner eyelid system, auto gaze correction, and other character-specific rig innovations.

## Problem
*Inside Out 2* required extending and improving character rigs from the original film while handling stylized anatomy (Joy's oversized eyes) that causes conventional rig setups to fail visually.

## Method
Key techniques presented:
- **Joy's four-corner eyelid system**: conventional eyelids have two corners (inner/outer). Joy's large eyes made halfway-open lids look smaller rather than partially shut. Solution: four lid corners (two per upper/lower lid), with an algorithm that lets animation choose any point along the lid topology as the corner position.
- **Eye auto gaze correction**: corrective system to maintain plausible gaze direction under large eye rotations.
- Additional character-specific rig challenges (detailed in the full 3-page talk paper).

## Key Results
- Solved the "eye appears smaller when half-open" issue on Joy.
- Gave Animation flexible control over lid corner position.
- Production-validated on the full cast of *Inside Out 2*.

## Limitations
- Highly character-specific solutions; limited direct generalizability.
- 3-page Talks paper; implementation details are high-level.

## Connections
- [[concepts/pose-space-deformation]] — corrective shapes used for gaze and lid corrections
- [[papers/singleton-2025-alien-rigs]] — later Pixar rig challenges paper
- [[authors/speirs-jacob]]

## Implementation Notes
The four-corner lid system is essentially a parameterized topology selector: instead of fixed corner vertices, the corner position is a continuous parameter along the lid edge loop. In practice this can be implemented as a weighted blend between adjacent corner positions.
