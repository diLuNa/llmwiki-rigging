---
title: "A Muscle Model for Animating Three-Dimensional Facial Expression"
authors: [Waters, Keith]
venue: SIGGRAPH 1987
year: 1987
tags: [muscles, blendshapes, digital-human, rig-generation]
source: knowledge
---

## Summary
Introduced the first computational model using anatomically-inspired muscle actuators to drive facial animation. Waters defined two muscle types—**linear** and **sphincter (orbicular)**—that apply a parameterized vector-field force to a facial mesh based on geometric influence zones. Approximately 20 muscle pairs span the face, mapping directly to FACS action units. This compact, physiologically motivated control space became the foundational architecture for muscle-based facial rigs used in production for decades.

## Problem
Prior to 1987, facial animation required manual keyframing of individual mesh vertices or ad-hoc blendshape interpolation. There was no parametric model connecting facial anatomy (muscles) to expressive deformation, and no principled way to generate diverse expressions from a small parameter set.

## Method
Two muscle types:

**Linear muscle** — applies a directed pull force toward an insertion point. Force on vertex $\mathbf{p}$:
```math
\mathbf{F}(\mathbf{p}) = a \cdot \left(1 - \frac{r}{d}\right) \cdot \hat{e}
```
where $a$ is activation level, $r$ is vertex distance from origin, $d$ is influence radius, $\hat{e}$ is pull direction toward insertion.

**Sphincter (ring) muscle** — radial contraction toward a center point $\mathbf{c}$ with ring radius $R$:
```math
\mathbf{F}(\mathbf{p}) = a \cdot \left(1 - \frac{|r - R|}{d}\right) \cdot \hat{e}_{radial}
```
Used for orbicularis oculi (eye ring), orbicularis oris (lip ring).

~20 muscle pairs total, each with: origin, insertion/center, influence zone, and scalar activation parameter. Mesh deformation: each vertex inside the influence zone is displaced proportionally to activation × falloff × pull direction.

## Key Results
Demonstrated plausible expression generation on a simple polygonal face mesh using a small number of muscle parameters. Qualitative results showing anger, fear, happiness, surprise, and disgust. Showed that physiological muscle groupings map naturally to FACS action units, providing a basis for anatomy-driven expression parameterization.

## Limitations
Simple linear force model ignores tissue mechanics (no physics, no volume preservation). No skin sliding. Single-layer mesh (no dermis/hypodermis/fat layers). Muscle placement is manual. Influence zones are spherical and do not model actual muscle fiber geometry.

## Connections
- [[papers/terzopoulos-1990-physically-based-face]] — extends this model with multi-layer physical tissue simulation
- [[papers/terzopoulos-1993-facial-analysis]] — adds analysis-by-fitting to recover activations from images
- [[papers/pdi-1998-facial-antz]] — PDI/DreamWorks muscle rig architecture descended from this work
- [[papers/choi-2022-animatomy]] — modern anatomy-inspired rig using explicit muscle fiber curves
- [[concepts/muscles]] — this paper defined the canonical linear + sphincter muscle types used for 3+ decades
- [[authors/waters-keith]]

## Implementation Notes
The linear muscle falloff is simply a tent function over distance — trivially implementable in any mesh deformer. The sphincter force can be implemented as a radial displacement field: project each vertex onto the ring plane, compute distance to the ring circle, apply falloff. Both are O(n) in mesh vertices per muscle evaluation.

## Quotes
> "The model employs two kinds of muscle: linear muscles, which contract in a straight line between origin and insertion points, and sphincter muscles, which contract circularly." (Waters 1987)
