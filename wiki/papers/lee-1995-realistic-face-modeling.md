---
title: "Realistic Modeling for Facial Animation"
authors: [Lee, Yuencheng; Terzopoulos, Demetri; Waters, Keith]
venue: SIGGRAPH 1995
year: 1995
tags: [muscles, digital-human, simulation]
source: raw/papers/lee-1995-realistic-face-modeling.pdf
---

## Summary
Automated construction of a subject-specific physically-based face model from **laser range scan** data. The pipeline segments the scan to locate anatomical landmarks; 26 muscle pairs are placed automatically from these landmarks; the multi-layer spring-mass tissue model is initialized from scan geometry. Includes articulated jaw, teeth, eyelids, and eye muscles. The first fully automatic subject-specific face model construction pipeline from a real person's scan. SIGGRAPH 1995.

## Problem
Earlier work (Terzopoulos & Waters 1990, 1993) required manual placement of muscles and manual initialization of tissue geometry on a generic head. Automatic, subject-specific construction from scan data was needed to make the approach practical.

## Method
**Pipeline:**
1. **Laser range scan** → 3D point cloud of subject's head
2. **Mesh fitting:** wrap a template mesh topology onto the scan
3. **Landmark detection:** automatically locate ~50 anatomical feature points (eye corners, lip corners, nose bridge, cheekbones, jaw margin) from scan curvature
4. **Muscle placement:** 26 muscle pairs with origins/insertions determined from landmark positions using an anatomical atlas
5. **Tissue initialization:** three-layer spring-mass model (epidermis, dermis, hypodermis) fitted to scan surface
6. **Articulation:** rigid jaw (temporomandibular joint), rigid skull, eyelid curves, eye muscles (rectus/oblique)

The 26 muscle pairs include: frontalis, corrugator, zygomaticus major/minor, orbicularis oculi, levator labii, depressor labii, orbicularis oris, mentalis, buccinator, and lateral pterygoid (jaw).

## Key Results
First fully automatic subject-specific face model pipeline from laser scan. Demonstrated on several real human subjects. Larger and more anatomically complete muscle set (26 pairs) vs. ~20 in prior work. Included jaw + eye articulation for complete face performance. Rendered with subsurface scattering approximation for skin appearance.

## Limitations
Pipeline relies on accurate landmark detection from scan data — fails on very low resolution or noisy scans. Spring-mass tissue, not FEM. No validation of muscle placement accuracy vs. true anatomy (e.g., MRI). Computationally expensive for 1995 hardware. Wrinkle formation is emergent from spring dynamics but not artistically directable.

## Connections
- [[papers/terzopoulos-1990-physically-based-face]] — tissue model and muscle actuator basis
- [[papers/terzopoulos-1993-facial-analysis]] — analysis-synthesis framework
- [[papers/cong-2015-anatomy-pipeline]] — ILM's modern equivalent: MRI → FEM anatomy → automatic muscle placement
- [[papers/sifakis-2005-anatomy-muscles]] — uses proper FEM flesh simulation (vs. spring-mass here)
- [[concepts/muscles]] — automatic landmark-based muscle placement; 26-muscle anatomy model
- [[authors/terzopoulos-demetri]]
- [[authors/waters-keith]]

## Implementation Notes
The landmark detection uses principal curvature analysis of the range scan surface — eyes appear as negative Gaussian curvature pockets; nose bridge as a saddle. Modern implementations would use deep landmark detectors on depth images. The muscle placement from landmark positions is a template lookup: each muscle pair has a fixed offset (in normalized head coordinates) from its anchor landmarks.
