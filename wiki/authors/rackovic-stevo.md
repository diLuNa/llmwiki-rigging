---
name: "Stevo Rackovic"
affiliation: Instituto Superior Técnico, Lisbon (as of 2024)
---

## Papers in Wiki
- [[papers/rackovic-2023-highfidelity-inverse-rig]] (arXiv 2023)
- [[papers/rackovic-2023-accurate-interpretable-inverse-rig]] (arXiv 2023)
- [[papers/rackovic-2023-distributed-rig-inversion]] (SIGGRAPH Asia 2023 Technical Communications)
- [[papers/an-2024-refined-inverse-rigging]] (SIGGRAPH Asia 2024)

## Research Themes
Blendshape rig inversion: formulating the inverse rig problem as regularized optimization over quartic/quadratic corrective blendshape models. Recurring focus on:
- **Sparsity**: reducing weight vector cardinality for artist interpretability
- **Temporal smoothness**: sequence-level joint optimization with roughness penalties
- **Scalability**: distributed ADMM approaches for large blendshape models
- **Accuracy**: up to 45% RMSE improvement over prior SOTA via MM/SQP formulations

## Collaborators
- Cláudia Soares (NOVA School of Science and Technology) — all papers
- Dušan Jakovetić (Faculty of Sciences, Novi Sad) — all papers
- Zoranka Desnica — 2023 quartic/quadratic papers

## Notes
Primary contributor to the line of work on principled convex/coordinate-descent solvers for the blendshape inverse rig problem 2023–2024. Work is closely coupled with MetaHuman's blendshape architecture (80 base + 400+ correctives, ~10,000 vertices).
