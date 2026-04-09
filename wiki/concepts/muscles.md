---
title: "Muscles & Soft Tissue Simulation"
tags: [muscles, simulation, volumes, skinning, rig-generation, digital-human]
---

## Definition
Muscle and soft tissue systems in character rigging encompass two related but distinct problems:

1. **Muscle as rig control** — anatomically-inspired virtual muscles whose contraction drives skin deformation, providing a physiologically meaningful parameterization of facial or body animation controls.
2. **Soft tissue as simulation** — volumetric FEM (or proxy) simulation of flesh, fat, and skin responding to skeletal motion, producing physically plausible secondary deformation (jiggle, compression, stretch).

The two can coexist in a pipeline: muscles drive the skeleton; soft tissue simulation responds to skeletal + muscular motion to produce the final surface deformation.

---

## Variants / Taxonomy

### Foundational Muscle Models (1987–1995)

The computational muscle model lineage originates with Waters (1987) and culminates in the automated anatomy construction pipelines of the 2000s.

- [[papers/waters-1987-muscle-model]] **(SIGGRAPH 1987)** — canonical muscle type definitions: **linear** (pull toward insertion) and **sphincter** (radial contraction). Influence zone with linear falloff. ~20 muscle pairs → FACS AUs. All later muscle models descend from this parameterization.
- [[papers/terzopoulos-1990-physically-based-face]] **(JVCA 1990)** — adds multi-layer viscoelastic tissue (epidermis/dermis/hypodermis spring network); muscle forces act on dermis layer; first physically-based facial animation; skin sliding emergent from layered spring coupling
- [[papers/terzopoulos-1993-facial-analysis]] **(IEEE TPAMI 1993)** — adds analysis direction: tracking facial features → inverse solve for muscle activations from images; first physics-model-based performance capture; expression retargeting demonstrated
- [[papers/lee-1995-realistic-face-modeling]] **(SIGGRAPH 1995)** — first **automatic** subject-specific model from laser scan; 26 muscle pairs auto-placed from anatomical landmarks; includes jaw, eyelid, eye articulation

### Production Facial Muscle Control Systems

Anatomy-inspired virtual muscles as rig controls for facial animation. Replaces or underlies FACS blendshapes with muscle fiber activations.

- [[papers/pdi-1998-facial-antz]] — first major production deployment; 300+ virtual muscles layered into high-level FACS controls; soft/hard area deformation per muscle; PDI/DreamWorks ANTZ (1998)
- [[papers/modesto-2014-dwa-face-system]] — DWA face system evolution ANTZ→Shrek→Mr. Peabody; muscle parameterization scaling over 16 years of production
- [[papers/choi-2022-animatomy]] — Weta FX / Avatar: The Way of Water; contractile fiber curves; strain $\gamma = (s - \bar{s})/\bar{s}$ per fiber → blendshape weights; FLAME-style correctives; fully transferable across identity
- [[papers/zoss-2018-jaw-rig]] — data-driven jaw anatomy rig; 6-DOF mandibular motion → 3-DOF Possell's Envelope; physiologically constrained; retargetable
- [[papers/zhu-2024-fabrig]] — anatomy-inspired muscle + fat patches driven by cloth simulation; topology-agnostic
- [[papers/lan-2017-digipro]] — DWA production approach: physics-augmented blendshapes; physically-inspired sculpting of AU targets; secondary dynamics as post-process

### ILM/Fedkiw FEM Anatomy Pipeline (2005–2019)

Tightly coupled FEM simulation pipeline from MRI scan to production-ready anatomical face model. The dominant production physics-face pipeline of the 2010s.

- [[papers/teran-2005-quasistatic-flesh]] **(SCA 2005)** — **FEM engine**: quasistatic Neo-Hookean flesh, invertible element handling via SVD diagonalization, modified Newton-Raphson. Foundation for the entire ILM pipeline.
- [[papers/sifakis-2005-anatomy-muscles]] **(SIGGRAPH 2005)** — **Inverse problem**: MRI anatomy model + FEM; recover muscle activations from sparse mocap markers via constrained optimization; differentiates through quasistatic solve
- [[papers/sifakis-2006-speech-muscle]] **(SIGGRAPH 2006)** — **Tongue biomechanics**: 8 intrinsic/extrinsic muscle bundles in an incompressible volumetric tongue model; full articulation range for speech phonemes; muscular hydrostat
- [[papers/cong-2015-anatomy-pipeline]] **(SIGGRAPH 2015)** — **Automatic anatomy from MRI**: tissue segmentation, tet mesh generation, muscle atlas registration; fully automated from scan to simulation-ready model
- [[papers/cong-2016-art-directed-blendshapes]] **(SIGGRAPH 2016)** — **Simulation → blendshapes**: bake FEM simulation results into FACS blendshape targets; combination shapes capture tissue interaction; art-directable on top; production-speed runtime
- [[papers/cong-2017-kong-muscle-talk]] **(SIGGRAPH Talks 2017)** — **Production deployment** on King Kong (*Kong: Skull Island*); workflow, practical challenges, animator integration
- [[papers/bao-2019-face-capture-muscles]] **(CVPR 2019)** — **Muscle activation capture**: CNN maps video → muscle activations; anatomical prior enforces co-activation patterns; FEM forward model in training loop

### Physics Face Models (Person-Specific, Without Full MRI)

- [[papers/ichim-2017-phace]] **(SIGGRAPH 2017)** — **Phace**: build physics face model from expression scans without MRI; alternating optimization of activations + material parameters; Neo-Hookean tissue + Waters-style muscle actuators; generative model for novel expressions
- [[papers/kadlecek-2019-physics-face-data]] **(PACMCGIT 2019)** — **Data-driven material calibration**: gravity-varied scans + EMG → calibrate per-region elastic moduli; adjoint sensitivity for gradient through quasistatic solve; 15–30% lower surface error vs. literature values

### Disney Research Zürich Physics Face Cluster (2020–2024)

Consistent group (Zoss, Chandran, Yang, Beeler, Gotardo, Bradley) producing a coherent evolution from secondary dynamics to implicit physics models.

- [[papers/zoss-2020-secondary-dynamics-capture]] **(SIGGRAPH 2020)** — **Empirical secondary dynamics**: fit per-region damped spring $(m, c, k)$ to residual video motion; transfer fitted dynamics to new animation sequences
- [[papers/yang-2023-implicit-physical-face]] **(SIGGRAPH 2023)** — **Implicit physical face**: neural SDF + material field encoding elastic properties; trained on FEM data; amortized fast inference; physics-consistency regularizer
- [[papers/yang-2024-generalized-physical-face]] **(SIGGRAPH 2024)** — **Generalized implicit model**: population-level implicit model with identity latent codes; few-shot adaptation from 5–20 scans; material style transfer between subjects
- [[papers/chandran-2024-anatomically-constrained-face]] **(SIGGRAPH 2024)** — **Anatomically constrained**: explicit skull SDF, implicit muscle tubes, skin SDF layer; hard non-penetration constraints; artist-editable anatomy within the implicit framework

### Realtime & Neural Physics (2021–2024)

- [[papers/zeng-2021-neuromuscular-face]] **(SIGGRAPH 2021)** — **Learned neuromuscular controller**: LSTM/RL controller maps target expression → muscle activation sequence; biomechanical co-activation constraints; physiologically plausible transitions
- [[papers/wagner-2023-softdeca]] **(SIGGRAPH 2023)** — **SoftDECA**: differentiable elastic shell on top of DECA; material parameters learned jointly from image sequences; secondary skin dynamics from neural face fitting
- [[papers/park-2024-realtime-face-sim-superres]] **(SIGGRAPH 2024)** — **Neural super-resolution**: coarse real-time FEM + neural upsampling to high-res simulation quality; >30fps with production-detail surface

### Full Musculoskeletal Simulation

Physics-based simulation of the complete anatomical stack: bones → muscles/tendons → fat → skin.

- [[papers/murai-2016-musculoskeletal-skin]] — complete layered stack (bone → muscle → fat → skin); validated against real subjects; physically correct jiggling and compression

### Soft Tissue / Flesh FEM (General)

Volumetric elastic simulation of flesh without explicitly modeling individual muscle fibers.

- [[papers/smith-2018-neo-hookean]] — stable Neo-Hookean; robust volume preservation at $\nu \approx 0.5$; used in Pixar's Fizz
- [[papers/mcadams-2011-elasticity-skinning]] — efficient corotational FEM for character skin; multigrid solver; production scale
- [[papers/kim-2022-dynamic-deformables]] — production course (Pixar Fizz); Neo-Hookean formulation, Hessian, collision, two-way coupling
- [[papers/bouaziz-2014-projective-dynamics]] — local constraint projections + global sparse solve; stable, fast, suitable for soft bodies at interactive rates

### Physics-Enriched Rigs (Rig ↔ Physics Coupling)

- [[papers/coros-2012-deformable-objects-alive]] — rig parameter space defines target shapes; FEM adds physical dynamics while respecting animator intent
- [[papers/hahn-2012-rig-space-physics]] — physics in reduced rig parameter space; forces projected through rig Jacobian; secondary motion within rig DOFs
- [[papers/bradley-2017-blendshape-physics]] — blendshape rig as kinematic target; co-rotational FEM drives mesh with volume preservation, inertia, damping

### Neural / Learned Muscle Surrogates

- [[papers/pfaff-2021-meshgraphnets]] — MeshGraphNets; learns physics simulation on production meshes; neural surrogate for flesh/muscle proxy dynamics

---

## Key Concepts

**Muscle types (Waters 1987):**
- *Linear*: pull force toward insertion point. $\mathbf{F}(\mathbf{p}) = a(1 - r/d)\hat{e}$
- *Sphincter*: radial contraction toward ring center. Used for orbicularis muscles (eyes, lips).

**Multi-layer tissue model (Terzopoulos 1990):**
Epidermis → Dermis (muscle anchor) → Hypodermis (fat) → Skull. Skin slides over fat (loose spring coupling between dermis and hypodermis). Still the conceptual model behind modern systems.

**FEM flesh (Teran 2005):** Invertible-element quasistatic Neo-Hookean with SVD diagonalization. Active muscle fibers via transversely isotropic material:
```math
\Psi = \Psi_{passive}(\mathbf{F}) + a \cdot \Psi_{fiber}(\lambda_f), \quad \lambda_f = \sqrt{\mathbf{f}_0^T \mathbf{C} \mathbf{f}_0}
```

**Simulation → blendshape bridge (Cong 2016):** Run FEM offline per FACS AU, bake surface deformation as blendshape delta. At runtime use standard fast blendshape evaluation. Combination shapes capture tissue interaction. Key production insight: physics quality does not require runtime physics — it can be pre-computed into the rig.

**Animatomy strain parameterization (Choi 2022):**
```math
\gamma_m = \frac{s_m - \bar{s}_m}{\bar{s}_m}, \quad B_E = E \cdot \gamma
```
where $s_m$ is contracted length, $\bar{s}_m$ is rest length, $E$ maps strain to skin displacement. Production-validated anatomy-to-deformation bridge.

**Flesh simulation material models:**
| Model | Volume preservation | Cost | Stability |
|-------|-------------------|------|-----------|
| Co-rotational linear FEM | Poor (large deformation) | Medium | Good |
| Neo-Hookean (Smith 2018) | Strong | Medium-High | Good |
| Projective Dynamics | Constraint-based | Low-Medium | Excellent |
| Position-Based Dynamics | Approximate | Low | Good |

**History of anatomy model construction:**
| Year | Source | Automation | Muscles |
|------|--------|-----------|---------|
| 1990 | Generic template (Terzopoulos) | Manual | ~20 pairs |
| 1995 | Laser scan (Lee) | Semi-auto | 26 pairs |
| 2005 | MRI (Sifakis) | Manual | Full anatomy |
| 2015 | MRI (Cong) | Fully auto | Full anatomy |
| 2017 | Expression scans (Ichim/Phace) | Fitting-based | Waters-style |
| 2019 | Gravity scans + EMG (Kadlecek) | Data-driven | Calibrated |
| 2023+ | Neural implicit (Yang, Chandran) | Train-once | Implicit |

---

## Connections
- [[concepts/neo-hookean-simulation]] — hyperelastic material model underlying most production flesh simulations
- [[concepts/facial-blendshape-rigs]] — muscle systems underlie or replace FACS blendshapes; simulation → blendshape bridge (Cong 2016)
- [[concepts/pose-space-deformation]] — muscle activations drive PSD correctives as an intermediate step
- [[concepts/secondary-motion]] — soft tissue jiggle and dynamic skin response; secondary dynamics capture (Zoss 2020)
- [[concepts/mesh-graph-nets]] — MeshGraphNets as neural surrogate for soft tissue FEM
- [[concepts/rig-inversion]] — mapping surface observations back to muscle activation parameters (Sifakis 2005, Bao 2019)
- [[concepts/implicit-surfaces]] — implicit SDF-based representation for physics face models (Yang 2023, Chandran 2024)
- [[concepts/speech-driven-animation]] — tongue biomechanics (Sifakis 2006) is the anatomical ground truth for speech animation

## Notes

**Production hierarchy:** Most studios don't run full muscle simulation at runtime. The pipeline is: anatomy model → offline simulation → baked blendshapes → fast runtime rig. Direct FEM at runtime appears only in offline VFX (ILM, Weta) or via neural acceleration (Wagner 2023, Park 2024).

**The "muscles" tag in this wiki** covers both uses: facial muscle control systems (Waters, PDI, Animatomy, DWA) and volumetric flesh simulation (Teran, Smith, McAdams, Coros, Bouaziz, Hahn). Both model the same anatomical truth at different abstraction levels and costs.
