---
title: "Anymate: A Dataset and Baselines for Learning 3D Object Rigging"
authors: [Deng, Yufan; Zhang, Yuhao; Geng, Chen; Wu, Shangzhe; Wu, Jiajun]
venue: ACM Transactions on Graphics (SIGGRAPH 2025)
year: 2025
tags: [dataset, rig-generation, auto-rigging, skinning, 3D-objects]
source: arXiv:2505.06227
doi: 10.1145/3721238.3730743
---

## Summary
Anymate: large-scale dataset of 230K 3D objects with expert-crafted rigging (skeletal structure and skinning weights). 70× larger than prior rigging datasets. Enables training of neural rigging models on diverse object categories beyond characters. Includes baselines for skeleton prediction and weight learning.

## Problem
Prior rigging datasets focus on humanoid characters. 3D object rigging (furniture, mechanical parts, animals) lacks large-scale annotated data. Scaling to diverse object types requires massive dataset of professional-quality rigs.

## Method
- **Data curation**: 230K objects with expert rigging annotations
- **Annotations**: Joint positions, hierarchy, skinning weights
- **Baselines**: Neural models for skeleton prediction and weight estimation
- **Evaluation**: Benchmark metrics for rig quality

## Key Results
- Largest rigging dataset to date (230K objects)
- Demonstrates feasibility of learning on diverse non-character objects
- Baseline models achieve reasonable generalization

## Limitations
- Annotation cost was significant (limits further scaling)
- Quality varies across object categories
- Some specialized objects (very asymmetric, high-articulation) underrepresented

## Connections
- [[papers/xu-2020-rignet]] — neural rigging for characters
- [[papers/ma-2025-riganyface]] — character-specific neural rigging
- [[concepts/auto-rigging]] — automated rig generation and datasets
- [[papers/zhang-2025-unirig]] — diverse topology rigging (humans + creatures)

## External References
- arXiv: [arxiv.org/abs/2505.06227](https://arxiv.org/abs/2505.06227)
- ACM DL: [doi.org/10.1145/3721238.3730743](https://doi.org/10.1145/3721238.3730743)
