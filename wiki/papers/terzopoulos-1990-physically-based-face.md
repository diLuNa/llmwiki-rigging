---
title: "Physically-Based Facial Modelling, Analysis, and Animation"
authors: [Terzopoulos, Demetri; Waters, Keith]
venue: Journal of Visualization and Computer Animation 1(2)
year: 1990
tags: [muscles, simulation, digital-human]
source: raw/papers/terzopoulos-1990-physically-based-face.pdf
---

## Summary
First physically-based facial animation system, combining Waters' (1987) muscle actuators with a multi-layer viscoelastic tissue model. The face is modeled as three deformable layers—epidermis, dermis, and hypodermis (fat)—connected by springs and sitting on a rigid skull scaffold. Muscle forces act on the dermis layer; spring networks propagate deformation outward through the skin, producing tissue resistance, sliding, and wrinkle formation not possible with pure displacement models.

## Problem
Waters (1987) produced deformation by directly displacing mesh vertices—no tissue physics, no material resistance, no sliding. Real facial skin deforms nonlinearly (wrinkles, bulging, sliding over subcutaneous fat), and the simple displacement model could not capture this complexity.

## Method
**Three-layer tissue model:**
- **Epidermis** (outer surface) — what is rendered
- **Dermis** (middle) — where muscles attach their forces
- **Hypodermis** (fat/connective tissue) — loose coupling to skull

Each layer is a triangulated mesh. Layers are coupled by **vertical springs** (tissue bonding); each layer has internal **elastic + viscous springs** along edges.

**Spring model per edge:**
```math
\mathbf{F}_{spring} = (k_e \cdot \Delta\ell + k_d \cdot \dot{\ell}) \hat{n}
```
where $k_e$ is elastic stiffness, $k_d$ is viscous damping, $\Delta\ell$ is stretch from rest length.

**Muscle actuators** from Waters (1987): linear + sphincter forces applied to dermis vertices. ~20 muscle pairs over the full face.

**Integration:** explicit Euler finite differences; each layer treated as a mass-spring system with per-vertex mass, damping, and spring restoration forces.

## Key Results
First physically-based facial animation. Demonstrated sliding and wrinkling behavior (skin slides over fat layer) not achievable with displacement-only models. Also demonstrated an analysis pipeline: fitting the model to tracked feature points from image sequences to recover muscle activation parameters. Journal of Visualization and Computer Animation 1(2), 1990.

## Limitations
Mass-spring approximation of continuum mechanics: stiffness matrix is not physically grounded (versus FEM). Parameters (spring constants, masses) require hand-tuning. No closed-form solution for material properties. Limited mesh resolution of 1990s hardware. Explicit Euler integration requires small time steps.

## Connections
- [[papers/waters-1987-muscle-model]] — muscle actuator definition used here
- [[papers/terzopoulos-1993-facial-analysis]] — follow-up: automated fitting (analysis) from image sequences
- [[papers/lee-1995-realistic-face-modeling]] — extends pipeline to subject-specific models from laser scans
- [[papers/teran-2005-quasistatic-flesh]] — replaces spring-mass with proper FEM; production-quality quasistatics
- [[papers/ichim-2017-phace]] — modern equivalent: physics face model per subject from expression scans
- [[concepts/muscles]] — foundational spring-mass + muscle tissue framework
- [[authors/terzopoulos-demetri]]
- [[authors/waters-keith]]

## Implementation Notes
The three-layer spring network is conceptually simple but the stiffness tuning is extremely tedious. In practice, the epidermis can be treated as a passive follower of the dermis (rigid coupling) to reduce parameters. The key physical behavior — skin sliding over fat — emerges from the relatively loose spring between dermis and hypodermis layers.
