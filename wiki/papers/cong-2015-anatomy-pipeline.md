---
title: "Fully Automatic Generation of Anatomical Face Simulation Models"
authors: [Cong, Matthew; Bao, Michael R.; Ben, Jane L.; Bhat, Kiran S.; Fedkiw, Ronald]
venue: SIGGRAPH 2015 (ACM Transactions on Graphics 34(4))
year: 2015
tags: [muscles, simulation, digital-human, rig-generation]
source: knowledge
---

## Summary
Presents a **fully automatic pipeline** for constructing subject-specific anatomical face simulation models from MRI scans. Given an MRI volume, the pipeline automatically segments tissues (bone, fat, muscle, skin), places muscle fiber origins and insertions, builds a volumetric tetrahedral FEM mesh, and assigns material properties. Output is a simulation-ready anatomy model requiring minimal manual intervention. Scales Sifakis et al.'s (2005) approach to production pipeline efficiency at ILM. SIGGRAPH 2015.

## Problem
Sifakis et al. (2005) required extensive manual work to build each subject's anatomy model from MRI. At ILM scale (multiple characters per film), fully manual construction is infeasible. An automated pipeline was needed to go from MRI scan to simulation-ready model.

## Method
**MRI processing:**
1. Acquire MRI volume of subject head at ~1mm resolution
2. **Tissue segmentation:** automated multi-class segmentation using atlas registration — classifies each voxel into: cortical bone, cancellous bone, skin, fat, muscle, teeth, saliva gland
3. **Mesh generation:** adaptive tetrahedral meshing from segmented voxels; finer resolution near facial surface; coarser in skull interior
4. **Muscle placement:** anatomical atlas of muscle origins/insertions (defined in template MRI space) → registered to subject via non-rigid MRI–to–subject deformable registration → muscle fiber directions computed per-tetrahedron

**Material assignment:** tissue-type dependent Neo-Hookean + transversely isotropic parameters (from literature values; later calibrated per-subject by Kadlecek et al. 2019).

**Output:** volumetric tet mesh with per-tetrahedron tissue type, material parameters, and muscle fiber direction. Ready for quasistatic FEM simulation (Teran 2005 engine).

## Key Results
Demonstrated on multiple film characters. Reported significant reduction in manual artist hours compared to Sifakis 2005 pipeline. Anatomy model matches MRI-derived ground truth tissue boundaries. Direct predecessor to the Kong deployment (Cong et al. 2017 SIGGRAPH Talks). SIGGRAPH 2015.

## Limitations
Requires a high-quality MRI scan per subject (expensive, not available for all characters). Atlas-based segmentation can fail in unusual face shapes or pathologies. Muscle fiber directions are from an average anatomical atlas, not subject-specific fiber tractography (requires diffusion MRI). Material parameters are not yet automatically calibrated (requires Kadlecek 2019).

## Connections
- [[papers/teran-2005-quasistatic-flesh]] — FEM simulation engine
- [[papers/sifakis-2005-anatomy-muscles]] — manual predecessor this work automates
- [[papers/cong-2016-art-directed-blendshapes]] — uses this anatomy model as the basis for muscle blendshapes
- [[papers/cong-2017-kong-muscle-talk]] — production deployment on Kong
- [[papers/kadlecek-2019-physics-face-data]] — data-driven calibration of material parameters for models from this pipeline
- [[papers/lee-1995-realistic-face-modeling]] — earlier automatic-placement system (from laser scan, not MRI)
- [[concepts/muscles]] — automated anatomy model construction; muscle atlas registration
- [[authors/cong-matthew]]
- [[authors/fedkiw-ronald]]
