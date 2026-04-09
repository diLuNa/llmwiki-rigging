---
title: "Anatomically-Constrained Implicit Face Models"
authors: [Chandran, Prashanth; Zoss, Gaspard; Beeler, Thabo; Gotardo, Paulo; Bradley, Derek]
venue: ACM Transactions on Graphics (SIGGRAPH 2024)
year: 2024
tags: [muscles, simulation, digital-human, neural, implicit-surfaces]
source: raw/papers/chandran-2024-anatomically-constrained-face.pdf
---

## Summary
Proposes an **implicit face model** that is explicitly constrained by anatomical structures — skull, muscles, and skin layers — encoded as continuous neural fields rather than discrete meshes. Unlike prior implicit face models that learn deformation from data alone, this approach hard-codes anatomical topology: the skull is a fixed rigid implicit surface; muscles are implicit tubes with fiber directions; skin is a second SDF layer above the skull. Muscle activations deform the skin layer via constrained neural fields trained to satisfy mechanical equilibrium. Disney Research Zürich. SIGGRAPH 2024.

## Problem
Previous implicit face models (Yang et al. 2023, 2024) learn from FEM simulation data but have no explicit anatomical structure — the learned implicit representation has no concept of skull, muscles, or fat. This makes them hard to interpret, constrains generalization, and prevents artist-directed anatomical control (e.g., move this muscle fiber, adjust skull shape).

## Method
**Multi-layer implicit anatomy:**
- **Skull layer:** rigid SDF $d_{skull}(\mathbf{x})$ from skull geometry (from MRI or template)
- **Muscle layer:** implicit muscle fibers as oriented tubes with activation-driven contraction; fiber SDF $d_{muscle}(\mathbf{x}, \mathbf{a})$ deforms toward origin with activation $\mathbf{a}$
- **Skin layer:** outer SDF $d_{skin}(\mathbf{x}, \mathbf{a})$ — must remain outside skull and satisfy contact constraint with muscle layer

**Physical constraints:**
- Non-penetration: $d_{skin} \geq d_{skull}$ enforced as hard constraint (signed distance inequality)
- Elastic equilibrium: skin deformation minimizes elastic energy given muscle forces; encoded via a neural implicit elastic energy $E_\theta(\mathbf{x})$ trained on FEM data

**Training:** multi-task learning — fit expression scans, satisfy anatomical constraints, minimize FEM-derived energy residuals.

**Controllability:** artists can adjust skull shape (rigid deformation of $d_{skull}$), modify muscle fiber paths (editing the implicit tube fields), or change material properties (scale the energy field coefficients).

## Key Results
Demonstrated on real human subjects. Anatomical constraints prevent implausible self-intersections (skin penetrating skull) that occur in unconstrained models. Artist-editable anatomy. Competitive with unconstrained implicit models in reconstruction accuracy. SIGGRAPH 2024.

## Limitations
Requires skull geometry per subject (from MRI or fitting). Muscle anatomy still template-based (not subject-specific fiber tractography). Training complexity is higher than unconstrained models. No dynamic effects: quasistatic.

## Connections
- [[papers/yang-2023-implicit-physical-face]] — same group; unconstrained predecessor
- [[papers/yang-2024-generalized-physical-face]] — parallel Disney Research generalized model
- [[papers/zoss-2020-secondary-dynamics-capture]] — same group; secondary dynamics capture
- [[papers/cong-2015-anatomy-pipeline]] — ILM's explicit anatomical pipeline (vs. implicit here)
- [[papers/teran-2005-quasistatic-flesh]] — FEM supervision source for training
- [[concepts/muscles]] — implicit anatomical face model with explicit muscle constraints
- [[concepts/implicit-surfaces]] — SDF + anatomical constraint layers
- [[authors/chandran-prashanth]]
- [[authors/zoss-gaspard]]
- [[authors/beeler-thabo]]
