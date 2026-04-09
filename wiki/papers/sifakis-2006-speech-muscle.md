---
title: "Simulating the Musculotendon Mechanics of the Human Tongue"
authors: [Sifakis, Eftychios; Shinar, Tamar; Irving, Geoffrey; Fedkiw, Ronald]
venue: SIGGRAPH 2006 (ACM Transactions on Graphics 25(3))
year: 2006
tags: [muscles, simulation, speech-driven-animation, digital-human]
source: raw/papers/sifakis-2006-speech-muscle.pdf
---

## Summary
The first biomechanically accurate simulation of the **human tongue** as a muscular hydrostat — a structure that maintains volume by coordinating multiple intrinsic and extrinsic muscle groups. The tongue is modeled as an incompressible, hyperelastic, volumetric solid with 8 transversely isotropic muscle fiber bundles (genioglossus, styloglossus, hyoglossus, intrinsic longitudinals, transversalis, verticalis). Activating subsets of muscles produces the full range of tongue shapes critical for speech articulation. SIGGRAPH 2006.

## Problem
The tongue is nearly impossible to capture optically (it is inside the mouth). Electromagnetic articulography (EMA) captures sparse tongue body points but not surface shape. A physics-based forward model of tongue musculature can bridge the gap: given muscle activation inputs, generate full volumetric tongue deformation for animation and speech synthesis.

## Method
**Anatomy model:**
- Volumetric tetrahedral mesh from MRI segmentation
- 8 muscle fiber bundles with distinct fiber directions from MRI
- Incompressibility constraint (tongue is ~96% water): enforced via multiplicative decomposition $\mathbf{F} = J^{1/3} \bar{\mathbf{F}}$, penalizing $J = \det(\mathbf{F}) \neq 1$

**Material model per muscle:**
```math
\Psi = \Psi_{passive}(\bar{\mathbf{F}}) + \kappa(J - 1)^2 + a \cdot \Psi_{fiber}(\lambda_f)
```
where $\kappa$ is bulk modulus (large → near-incompressible), $a \in [0,1]$ activation, $\lambda_f$ fiber stretch.

**Simulation:** Quasistatic nonlinear FEM (Teran et al. 2005 engine) with invertible-element handling. Hyoid bone modeled as rigid anchor for extrinsic muscles.

**Muscle groups modeled:**
- Genioglossus (anterior/posterior) — protrusion, retraction, depression
- Styloglossus — retraction, elevation
- Hyoglossus — depression, retraction
- Verticalis + transversalis + superior/inferior longitudinals — shape changes (broadening, narrowing, curling)

## Key Results
Demonstrated the full range of articulatory positions for English phonemes (bilabial stop, alveolar stop, velar, fricative). Tongue positions validated against EMA data. Showed that 8 muscle activations are sufficient to reproduce measured tongue body positions. Provides a forward model suitable for speech animation without optical capture of the tongue interior.

## Limitations
Quasistatic: no dynamic tongue oscillation or hydrodynamics (saliva). Jaw is rigid in this model (separate simulation needed for full vocal tract). Muscle fiber directions approximated from MRI segmentation — real fiber architecture is more complex. Not yet integrated with real-time rendering.

## Connections
- [[papers/teran-2005-quasistatic-flesh]] — FEM engine and invertible element handling
- [[papers/sifakis-2005-anatomy-muscles]] — same group; face muscle activation recovery
- [[papers/medina-2022-tongue-animation]] — modern neural approach to tongue animation from audio
- [[concepts/muscles]] — muscular hydrostat model; 8-bundle tongue anatomy
- [[concepts/speech-driven-animation]] — this physics model is the anatomical ground truth for speech animators
- [[authors/sifakis-eftychios]]
- [[authors/fedkiw-ronald]]

## Implementation Notes
The incompressibility enforcement via large bulk modulus $\kappa$ works well in practice but couples longitudinal and transverse deformations artificially at finite $\kappa$. True incompressibility (saddle-point formulation with pressure as additional unknown) is more accurate but doubles the unknowns. The Teran 2005 quasistatic solver handles the coupled system via block elimination.
