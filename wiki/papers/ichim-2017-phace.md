---
title: "Phace: Physics-Based Face Modeling and Animation"
authors: [Ichim, Alexandru Eugen; Kadlecek, Petr; Kavan, Ladislav; Pauly, Mark]
venue: SIGGRAPH 2017 (ACM Transactions on Graphics 36(4))
year: 2017
tags: [muscles, simulation, digital-human, facial-capture]
source: knowledge
---

## Summary
**Phace** constructs a person-specific physics-based face model from a small set of expression scans (no MRI required). The method fits a volumetric FEM model with passive elastic tissue, active muscles, and rigid bones to match a captured subject's expression geometry. The fitted model can then be simulated, retargeted, or used as a generative model for novel expressions. Replaces MRI-based anatomy extraction with shape-from-scan material fitting. SIGGRAPH 2017.

## Problem
MRI-based anatomy pipelines (Cong 2015, Sifakis 2005) require expensive medical imaging. For digital humans where only surface scans are available (e.g., photogrammetry, structured light), an alternative approach is needed that can estimate both geometry and material properties from surface data alone.

## Method
**Model components:**
- **Passive tissue:** Neo-Hookean volumetric mesh representing skin, fat, and connective tissue; initialized from neutral surface scan inflated to 3D
- **Active muscles:** linear and sphincter muscle actuators (Waters 1987 style) embedded in the volumetric mesh; positions initialized from a generic anatomical template registered to the scan
- **Rigid bones:** skull and jaw as kinematic rigid bodies driving the tissue boundary conditions

**Fitting from expression scans:**
1. Collect $N$ expression scans (typically 20–50 distinct expressions)
2. For each expression, solve for muscle activations $\mathbf{a}_n$ and material parameters $\boldsymbol{\theta}$ jointly:
```math
\min_{\mathbf{a}_n, \boldsymbol{\theta}} \sum_n \| \mathbf{x}_{sim}(\mathbf{a}_n, \boldsymbol{\theta}) - \mathbf{x}_{scan_n} \|^2 + \text{regularizers}
```
3. Alternating optimization: fix $\boldsymbol{\theta}$, solve for $\{\mathbf{a}_n\}$; fix $\{\mathbf{a}_n\}$, update $\boldsymbol{\theta}$
4. Parameters $\boldsymbol{\theta}$: per-region Neo-Hookean Young's modulus and Poisson ratio

**Output:** a generative model — given any muscle activation vector $\mathbf{a}$, the FEM simulation produces the corresponding surface expression, potentially interpolating beyond the observed scan set.

## Key Results
Demonstrated on real human subjects with 20–50 expression scans. Fitted models generalize to unseen expressions with reasonable accuracy. Material parameters estimated from scans are within physiological range. Enables expressive retargeting and physics-based interpolation. SIGGRAPH 2017.

## Limitations
Simplified muscle model (Waters-style vector fields, not anatomical fiber bundles). No MRI: muscle positions are from a generic template, not subject-specific anatomy. Fitting requires many expression scans (expensive to acquire). Quasistatic — no secondary dynamics. Material fitting is non-convex; solution depends on initialization.

## Connections
- [[papers/terzopoulos-1990-physically-based-face]] — conceptual ancestor: same passive tissue + muscle actuator framework
- [[papers/teran-2005-quasistatic-flesh]] — FEM engine used
- [[papers/cong-2015-anatomy-pipeline]] — alternative: use MRI instead of expression scans
- [[papers/kadlecek-2019-physics-face-data]] — extends Phace with richer data (gravity scans + EMG)
- [[papers/sifakis-2005-anatomy-muscles]] — MRI-based alternative for the same goal
- [[concepts/muscles]] — scan-based physics face model; material fitting from expression data
- [[authors/ichim-alexandru]]
- [[authors/kadlecek-petr]]
- [[authors/kavan-ladislav]]
- [[authors/pauly-mark]]

## Implementation Notes
The key practical challenge in Phace is the inflation of the 2D surface scan to a 3D volumetric mesh — since real anatomy has varying tissue thickness that is not visible from the scan surface. Phace uses a generic thickness template (registered to the scan) to initialize tissue volumes. The alternating optimization converges reliably if the expression scans provide good coverage of the muscle activation space.
