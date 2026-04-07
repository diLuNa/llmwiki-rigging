# Wiki Log

Append-only chronological record of all wiki activity.

Format: `## [YYYY-MM-DD] <operation> | <title>`

---

## [2026-04-05] init | Wiki initialized

Created directory structure, CLAUDE.md schema, index.md, log.md, overview.md, and stub pages for seed papers and concepts from prior work. Sources in scope: de Goes 2020, Lewis 2000, Kavan 2007, Jacobson 2011.

## [2026-04-05] vex | Kelvinlets VEX snippets extracted

Created wiki/vex/ directory with 7 Houdini VEX snippets covering all algorithms
from the Regularized Kelvinlets (2018) and Sharp Kelvinlets (2019) papers:
- kelvinlet-grab.vex        — core grab brush, single-scale (Eq. 6–7)
- kelvinlet-multiscale.vex  — bi-scale / tri-scale extrapolation (Eq. 8–11)
- kelvinlet-affine.vex      — twist / scale / pinch brushes (Eq. 14–17)
- kelvinlet-constrained.vex — multi-point constrained deformation + Python solver (Eq. 18)
- kelvinlet-cusped.vex      — cusped (spiky) Kelvinlet profile (Eq. 10)
- kelvinlet-laplacian.vex   — Laplacian & Bi-Laplacian Kelvinlets (Eq. 15–16)
- kelvinlet-sharp.vex       — Cusped Laplacian & Cusped Bi-Laplacian (Eq. 17–18)
Created wiki/vex/index.md with parameter guide, quick-start formulas, and health summary.

## [2026-04-05] ingest | Referenced papers from all ingested PDFs (14 papers)

Extracted reference sections from all 24 PDFs and ingested relevant papers not yet in the wiki:
- Dynamic Kelvinlets (de Goes & James, SIGGRAPH 2018)
- Exoskeleton: Curve Network Abstraction (de Goes et al., C&G 2011)
- Deformation Transfer for Triangle Meshes (Sumner & Popovic, SIGGRAPH 2004)
- Delta Mush (Mancewicz et al., DigiPro 2014)
- AutoSpline (Hessler & Talbot, SIGGRAPH Talks 2016)
- Learning an Inverse Rig Mapping (Holden et al., SCA 2015)
- Fast and Deep Deformation Approximations (Bailey et al., SIGGRAPH 2018)
- Efficient Elasticity for Character Skinning (McAdams et al., SIGGRAPH 2011)
- Projective Dynamics (Bouaziz et al., SIGGRAPH 2014)
- Direct Delta Mush Skinning (Le & Lewis, SIGGRAPH 2019)
- Fast Automatic Skinning Transformations (Jacobson et al., SIGGRAPH 2012)
- Skinning Course (Jacobson et al., SIGGRAPH Course 2014)
- Go Green: General Regularized Green's Functions (Chen & Desbrun, SIGGRAPH 2022)
- Revamping the Cloth Tailoring Pipeline at Pixar (Waggoner & de Goes, SIGGRAPH Talks 2022)
New concept: delta-mush. New authors: sumner-robert, le-binh, holden-daniel, bouaziz-sofien, hessler-mark, talbot-jeremie, sifakis-eftychios.

## [2026-04-05] ingest | Referenced papers from Kelvinlets bibliography (5 papers)

Created pages from knowledge (no local PDFs) for 5 key papers cited in the Kelvinlets paper:
- Harmonic Coordinates for Character Articulation (Joshi et al., SIGGRAPH 2007)
- Green Coordinates (Lipman et al., SIGGRAPH 2008)
- As-Rigid-As-Possible Surface Modeling (Sorkine & Alexa, SGP 2007)
- Elasticity-Inspired Deformers for Character Articulation (Kavan & Sorkine, ACM ToG 2012)
- Rig-Space Physics (Hahn et al., SIGGRAPH 2012)
Added authors: lipman-yaron, sorkine-olga. Updated: kavan-ladislav, cage-deformation concept, index.

## [2026-04-05] ingest | Bulk ingest of raw/papers/*.pdf (22 papers)

Ingested all 24 PDFs from raw/papers/ (2 were the Somigliana supplement and the pre-existing sculpt paper, already handled). Created 22 new paper pages, 7 new concept pages, and 13 new/updated author pages. Fixed degoes-2020-sculpt.md authors (were wrong). Updated index.md.

Papers ingested:
- Regularized Kelvinlets (de Goes & James, SIGGRAPH 2018)
- Stable Neo-Hookean Flesh Simulation (Smith, de Goes, Kim — SIGGRAPH 2018)
- Patch-based Surface Relaxation (de Goes et al., SIGGRAPH Talks 2018)
- Sharp Kelvinlets (de Goes & James, ACM ToG 2019)
- Mesh Wrap based on Affine-Invariant Coordinates (de Goes & Martinez, SIGGRAPH Talks 2019)
- Holding the Shape in Hair Simulation (Iben et al., SIGGRAPH Talks 2019)
- Discrete Differential Operators on Polygonal Meshes (de Goes et al., SIGGRAPH 2020)
- Phong Deformation (James, SIGGRAPH 2020)
- Garment Refitting for Digital Characters (de Goes et al., SIGGRAPH Talks 2020)
- Analytically Learning an Inverse Rig Mapping (Gustafson et al., SIGGRAPH Talks 2020)
- FaceBaker: Baking Character Facial Rigs with ML (Radzihovsky et al., SIGGRAPH Talks 2020)
- Dynamic Deformables course (Kim & Eberle, SIGGRAPH Course 2022)
- Character Articulation through Profile Curves (de Goes et al., SIGGRAPH 2022)
- CurveCrafter (Willett et al., SIGGRAPH 2023)
- Somigliana Coordinates (Chen et al., SIGGRAPH 2023)
- Shaping the Elements: Curvenet Controls in Elemental (Nguyen et al., SIGGRAPH Talks 2023)
- Stochastic Computation of Barycentric Coordinates (de Goes & Desbrun, SIGGRAPH 2024)
- Controllable Neural Style Transfer for Dynamic Meshes (Haetinger et al., SIGGRAPH 2024)
- Pixar's Inside Out 2: Rig Challenges (Hoffman et al., SIGGRAPH Talks 2024)
- Directing Cloth Draping through Blended UVs (Olmos et al., SIGGRAPH Talks 2025)
- Crafting Expressive Non-Humanoid Alien Characters (Singleton et al., SIGGRAPH Talks 2025)
- Metaball Madness: Rigging an Implicit Surface Character (Lykkegaard et al., SIGGRAPH Talks 2025)

## [2026-04-05] vex | Curvenet VEX snippets extracted

Created 3 Houdini VEX snippets from Character Articulation through Profile Curves (de Goes, Sheffler & Fleischer, SIGGRAPH 2022):
- curvenet-frames.vex         — scaled frame construction + deformation gradient per segment (§3, Eq. 1)
- curvenet-polygon-laplacian.vex — cut-aware polygonal Laplacian L_f (Appendix, Eq. 7–10)
- curvenet-deform.vex         — surface deformation evaluation: adjusted constraints xc, face transforms yh, Python Poisson solve (§4.3, Eq. 5–6)
Updated wiki/vex/index.md with new entries, parameter guide, and key formulas.

## [2026-04-05] vex | Cage deformation VEX snippets extracted

Created 3 Houdini VEX snippets covering cage deformation:
- cage-green-coords.vex       — Green Coordinates face weights ψ_f (solid angle) + deformation eval (Lipman 2008); vertex weights φ_i reference Python BEM
- cage-somigliana-kernels.vex — Kelvinlet K and traction T kernels (Eq. 3-4) + quadrature precomputation of T_i and K_j per query point (Chen et al. 2023, Eq. 8)
- cage-somigliana-deform.vex  — Corotational deformation (Eq. 11): per-face polar decomp, bulging β/η, traction force balance (Eq. 15), final invert(T_sum)*rhs solve
Updated wiki/vex/index.md with cage deformation section and health summary.

## [2026-04-06] ingest | New raw/papers PDFs ingested (10 papers)

Identified 10 new PDFs in raw/papers/ added since previous session. All ingested. Scope expanded.

Papers ingested:
- Generating 3D Faces using Convolutional Mesh Autoencoders / CoMA (Ranjan et al., ECCV 2018) — Chebyshev spectral graph convolution + hierarchical mesh pooling for nonlinear face VAE
- ImFace: A Nonlinear 3D Morphable Face Model With Implicit Neural Representations (Zheng et al., CVPR 2022) — dual SDF deformation fields for identity/expression
- ImFace++ (Zheng et al., TPAMI 2024) — RDF space model, two-stage deformation, ear-to-ear reconstruction
- Nonlinear 3D Face Morphable Model (Tran & Liu, CVPR 2018) — CNN encoder-decoder trained on 2D images via differentiable rendering
- CANRIG: Cross-Attention Neural Face Rigging with Variable Local Control (ETH/Disney, EG 2026) — cross-attention for learned local rig control
- State of the Art Report: Facial Blendshape Animation (Lewis, Anjyo et al., EG 2014) — comprehensive blendshape survey, production conventions
- FACEIT (Díaz Barros et al., DFKI ~2020) — real-time performance-driven face animation via NLLS blendshape weight solving from RGB video
- DiffusionRig (Ding et al., CVPR 2023) — personalized diffusion model conditioned on FLAME rig for face appearance editing
- Mesh VAE with RIMD Features (arXiv 1709.04307, 2017) — rigid-motion-invariant mesh VAE for 3D face synthesis
- Blendshape Weight Estimation from Markers (JTDP03, ~2003) — foundational marker-to-blendshape inverse solve formulation

CLAUDE.md scope updated: added nonlinear 3D morphable face models, performance-driven facial animation, diffusion-based facial appearance editing.
Updated: concepts/blendshapes (added STAR + JTDP03 + neural blend shapes). sorkine-olga author page updated previously.

## [2026-04-06] ingest | New raw/papers PDFs ingested (3 papers)

Identified 6 previously un-ingested PDFs in raw/papers/. Ingested 3 in-scope, noted 3 out-of-scope.

Papers ingested:
- Learning Neural Blend Shapes for Character Animation (Li, Aberman, Hanocka, Liu, Sorkine-Hornung, Liu — SIGGRAPH 2021)
  - Learns pose-dependent corrective blend shapes + skinning weights jointly from data; residual over LBS; K=8 neural basis vectors; no manual sculpts
- A New Blendshape-Based Retargeting for 3D Facial Expression (Sol et al., Omotion — International Journal 2025)
  - VAE-based cross-identity facial expression retargeting; mask-based robustness; 3D blendshape weight prediction
- Learning Mesh-Based Simulation with Graph Networks / MeshGraphNets (Pfaff et al., ICLR 2021)
  - GNN framework for learned physics on arbitrary mesh topologies; cloth, rigid, fluid; Encoder-Processor-Decoder with mesh+world edge graph

Papers NOT ingested (out of scope):
- 2002.09405v2.pdf → "Learning to Simulate" (Sanchez-Gonzalez, ICML 2020) — general particle simulation GNN, not character deformation
- Blendshape-Based_Facial_Animation_Using_OPF_and_Random_Forest.pdf → IEEE TAC affective computing paper, facial expression recognition from video
- 2010.03409v4.pdf → ingested as pfaff-2021-meshgraphnets (corrected: same file)

Wait — 2010.03409v4.pdf IS the MeshGraphNets paper. All 6 unrecognized files accounted for.

New authors: aberman-kfir. Updated: sorkine-olga. CLAUDE.md scope updated with neural blend shapes and mesh graph nets.

## [2026-04-06] ingest | Missing papers added (5 papers from knowledge)

Added 5 papers flagged during lint as notable gaps:
- SMPL: A Skinned Multi-Person Linear Model (Loper et al., SIGGRAPH Asia 2015) — foundational parametric body model; learned LBS weights + pose PSD correctives
- Learning a Model of Facial Shape and Expression from 4D Scans / FLAME (Li et al., SIGGRAPH Asia 2017) — face equivalent of SMPL; pose corrective formulation used by Animatomy
- Smooth Skinning Decomposition with Rigid Bones / SSDR (Le & Deng, SIGGRAPH Asia 2012) — auto-extracts LBS rig from mesh animation sequence
- Linear Subspace Design for Real-Time Shape Deformation (Wang et al., SIGGRAPH 2015) — optimizes localized linear deformation basis from rig samples
- Sparse Localized Deformation Components (Neumann et al., SIGGRAPH Asia 2013) — dictionary learning on mesh sequences → interpretable localized blendshapes

New author: black-michael (MPI-IS). Updated: le-binh (added SSDR), concepts/blendshapes, concepts/linear-blend-skinning, index.md.
All pages from knowledge — no local PDFs.

## [2026-04-06] lint | Wiki lint pass

Fixed 6 broken wiki links:
- vex/index.md: `papers/degoes-2022-curvenet` → `papers/degoes-2022-profile-curves`
- bailey-2018-deep-deformation.md: `authors/obrien-james` → plain text (no author page)
- jain-2010-hand-secondary.md: `concepts/correctives` → `concepts/pose-space-deformation`
- iben-2019-hair-shape.md: `concepts/secondary-motion` now valid (concept page created)
- zhu-2024-fabrig.md: `concepts/simulation` → `concepts/neo-hookean-simulation`
- zoss-2018-jaw-rig.md: `concepts/rig-generation` → `concepts/rig-inversion`

Created: wiki/concepts/secondary-motion.md (20 concepts total).
Fixed: vex/index.md missing Animatomy section (5 snippets now indexed, 34 total).
Updated: index.md with new concept; health summary in vex/index.md.

Orphans: none — all 71 papers, 20 concepts, 28 authors have inbound links from index.md or cross-links.
Contradictions: none identified.
Missing papers suggested (see lint report in log).

## [2026-04-06] vex | Sliding Deformation VEX snippets extracted

Created 3 Houdini VEX snippets from Pinskiy, Eurographics 2010:
- sliding-tangent-basis.vex          — local {b1,b2,N} frame + per-neighbour exponential map in ΨP (§3.1)
- sliding-direction-propagate.vex    — BFS parallel transport of {a1,a2} via dihedral() (§3.2, Eq. 4)
- sliding-displace.vex               — cubic falloff tangential dp + xyzdist() surface re-projection (§3.3)
Updated wiki/vex/index.md with Sliding Deformation section.

## [2026-04-06] vex | Mesh Wrap VEX snippets extracted

Created 4 Houdini VEX snippets from de Goes & Martinez, SIGGRAPH Talks 2019:
- mesh-wrap-affine-coords.vex      — stencil dYi assembly; Python builds Wi = null(dYi) + sparse L (§4)
- mesh-wrap-project-score.vex      — xyzdist() projection pi + score mi = 1/(1+µ‖pi−xi‖²) (§3)
- mesh-wrap-distortion-energy.vex  — per-vertex ‖dXi Wi‖²_F distortion diagnostic (§4)
- mesh-wrap-solve.vex              — apply solved X; full Python Cholesky solve in comments (§5, Eq. 2)
Updated wiki/vex/index.md with Mesh Wrap section.

## [2026-04-06] vex | Animatomy VEX snippets extracted

Created 5 Houdini VEX snippets from Choi et al. SIGGRAPH Asia 2022:
- animatomy-muscle-strain.vex     — strain γ = (s - s̄)/s̄ per muscle fiber curve (§5.1)
- animatomy-strain-blendshapes.vex — B_E = E·γ strain-to-skin deformation matrix (§5.3)
- animatomy-pose-correctives.vex  — B_P = Σ(R_k − R*_k)P_k FLAME-style pose correctives (§5.2)
- animatomy-jaw-rbf.vex           — jaw proxy RBF χ(p) = Σψᵢgᵢ/Σgᵢ, Gaussian kernel (§5.5)
- animatomy-full-model.vex        — full forward M(θ,γ) = W(T + B_P + B_E, J, θ, W) (§5)
Includes Python AE forward-pass reference and packing helpers throughout.

## [2026-04-06] vex | Wrinkle systems VEX snippets extracted

Created 5 Houdini VEX snippets from Cutler et al. C&G 2007 and Raman et al. CVPR 2022:
- wrinkle-stress-vector.vex       — 16-component stress vector (8 edge lengths + 8 angle cosines, §5 Fig. 6)
- wrinkle-proximity-metric.vex    — proximity metric m*_j + box filter + persistence function (Eq. 1–2)
- wrinkle-curve-displacement.vex  — Gaussian displacement field from artist wrinkle curves (§4)
- wrinkle-blend.vex               — weighted displacement blend d* = Σ w_j · d_j (Eq. 3)
- wrinkle-mesh-tension.vex        — mesh tension scalar (compression/expansion, softmax; Raman 2022 §4)
Updated wiki/vex/index.md with Wrinkle Systems section, full pipeline diagram, and key formulas.

## [2026-04-06] vex | Bounded Biharmonic Weights VEX snippets extracted

Created 4 Houdini VEX snippets from Jacobson et al. SIGGRAPH 2011 (from knowledge — no local PDF):
- bbw-cotan-laplacian.vex  — cotangent Laplacian assembly; sparse (row,col,val) triplets + full Python QP solve
- bbw-mass-matrix.vex      — lumped mass M_i per vertex (1/3 × incident triangle areas)
- bbw-lbs-apply.vex        — runtime LBS deformation with stored BBW weight attributes
- bbw-harmonic-weights.vex — harmonic weight diffusion (linear baseline, Laplacian smoother)
Updated wiki/vex/index.md with BBW section, parameter guide, and key formulas.

## [2026-04-06] ingest | Disney Research animation publications (9 papers)

Scraped https://la.disneyresearch.com/publication (Animation facet, 6 pages). Ingested relevant papers not already in wiki:
- Real-time Skeletal Skinning with Optimized Centers of Rotation (Le & Hodgins, SIGGRAPH 2016) — CoR skinning
- Efficient Simulation of Secondary Motion in Rig-Space (Hahn et al., SCA 2013)
- A Deep Learning Approach for Generalized Speech Animation (Taylor et al., SIGGRAPH 2017)
- Enriching Facial Blendshape Rigs with Physical Simulation (Bradley et al., Eurographics 2017)
- Subspace Clothing Simulation Using Adaptive Bases (Hahn et al., SIGGRAPH 2014)
- Deformable Objects Alive (Coros et al., SIGGRAPH 2012)
- Facial Performance Enhancement Using Dynamic Shape Space Analysis (Bermano et al., ACM TOG 2013)
- Dynamic Skin Deformation Simulation Using Musculoskeletal Model (Murai et al., Pacific Graphics 2016)
- Augmenting Hand Animation with Three-Dimensional Secondary Motion (Jain et al., SCA 2010)

Already in wiki (skipped): Rig-Space Physics (Hahn 2012), Efficient Elasticity for Character Skinning (McAdams 2011).
Out of scope (not ingested): robotics papers, HCI/AR interaction, narrative systems, terrain editing, 2D animation stylization, crowd AI.

## [2026-04-06] ingest | Expanded-scope ingest: appearance, hand, speech, crowd, facial rig (11 papers)

Ingested all previously skipped "out of scope" PDFs and expanded wiki scope to cover adjacent areas.

Papers ingested:
- Analysis of Human Faces using Measurement-Based Skin Reflectance (Weyrich et al., SIGGRAPH 2006)
- Modeling Facial Geometry using Compositional VAEs (Bagautdinov et al., CVPR 2018)
- GANtlitz: Ultra High Resolution Generative Model for Multi-Modal Face Textures (Gruber et al. incl. Prasso, Eurographics 2024)
- GraspXL: Generating Grasping Motions for Diverse Objects at Scale (Zhang et al., ECCV 2024)
- Speech Driven Tongue Animation (Medina et al., CVPR 2022)
- Multi-Modal Diffusion for Hand-Object Grasp Generation (Cao et al., Adobe 2024)
- Realistic Wrinkle Generation for 3D Face Modeling Based on Curves (Li et al., C&G 2010)
- The PDI Crowd System for ANTZ (PDI/DreamWorks, SIGGRAPH Sketches 1998)
- The PDI Facial Animation System for ANTZ (PDI/DreamWorks, SIGGRAPH Sketches 1998)
- A Beginners Guide to Dual-Quaternions (Kenwright, WSCG 2012)

New concepts: digital-human-appearance, hand-animation, speech-driven-animation.
Scope updated in CLAUDE.md to include appearance, hand, speech, and crowd animation.

## [2026-04-06] ingest | Bulk ingest of new raw/papers/*.pdf (7 papers)

New PDFs identified in raw/papers/ not previously ingested. Created 7 paper pages, 1 new concept page, 3 new author pages.

Papers ingested:
- An art-directed wrinkle system for CG character clothing and skin (Cutler et al. incl. Prasso, C&G 2007)
- Animatomy: Anatomy-inspired facial rig system (Choi et al., Weta FX, SIGGRAPH Asia 2022)
- An Empirical Rig for Jaw Animation (Zoss, Bradley, Bérard, Beeler — Disney Research, SIGGRAPH 2018)
- Sliding Deformation: Shape Preserving Per-Vertex Displacement (Pinskiy, Disney, Eurographics 2010)
- Mesh-Tension Driven Expression-Based Wrinkles for Synthetic Faces (Raman et al., Microsoft, CVPR 2022)
- Fabrig: Cloth-Simulated Transferable 3D Face Parameterization (Zhu & Joslin, ACM 2024)
- DreamWorks Animation's Face System, a Historical Perspective (Modesto & Walsh, SIGGRAPH Talks 2014)

New concept: wrinkle-systems. New authors: prasso-luca, beeler-thabo, singh-karan.

PDFs NOT ingested (out of scope or adjacent only):
- AnalysisOfHumanFaces.pdf — skin reflectance/appearance, not deformation
- Bagautdinov CVPR 2018 — VAE face geometry, not rigging
- GANtlitz Eurographics 2024 — face textures/appearance
- GraspXL / MultiModalGraspObject — hand grasping, out of scope
- Medina tongue animation CVPR 2022 — speech/tongue, out of scope
- RealisticWrinkleGenerationFor3DFaceModeling — older academic wrinkle paper, lower priority
- ThePDICrowdSystemforANTZ — crowd system, not rigging
- dual-quaternion.pdf — Kenwright tutorial (not research), companion to kavan-2007-dqs.md

## [2026-04-07] ingest | New raw/papers PDFs ingested (6 papers)

Identified 8 new PDFs in raw/papers/. Ingested 6 in-scope papers. Updated FLAME source field.

Papers ingested:
- RigNet: Neural Rigging for Articulated Characters (Xu, Zhou, Kalogerakis, Landreth, Singh — SIGGRAPH 2020)
  — End-to-end GMEdgeNet skeleton + skinning weight prediction from bare mesh; 2,703 character training set
- DECA: Learning an Animatable Detailed 3D Face Model from In-The-Wild Images (Feng, Black, Bolkart — SIGGRAPH 2021)
  — FLAME + neural detail displacement conditioned on identity + expression; trains on in-the-wild images
- Neural Face Rigging / NFR (Qin, Saito, Aigerman, Groueix, Komura — SIGGRAPH 2023)
  — Triangulation-agnostic FACS auto-rigging via DiffusionNet + NJF decoder; FACS-regularized latent
- RigAnyFace (Ma, Kneubuehler et al. — NeurIPS 2025)
  — Extends NFR: disconnected components (global encoder), 2D optical-flow supervision on unlabeled data
- MeshGraphNetRP (Libao et al. — ACM MIG 2023)
  — Extends MeshGraphNets with GRU encoder + physics-informed losses for cloth simulation
- Neutral Facial Rigging from Limited Spatiotemporal Meshes (Hou et al. — Electronics 2024)
  — MLP-based bidirectional rig gen + recognition from limited mesh data

Updated: li-2017-flame.md source → raw/papers/flame_paper.pdf (local PDF now available)
New concept: auto-rigging. New authors: kalogerakis-evangelos, saito-jun. Updated: singh-karan.

## [2026-04-07] python | Kelvinlets Python modules extracted

Created 4 NumPy Python modules covering all Kelvinlet algorithms:
- kelvinlet_core.py         — grab brush: single-scale, bi-scale, tri-scale (Eq. 6–11); vectorized over N points
- kelvinlet_affine.py       — twist, scale, pinch brushes (Eq. 14–17); includes volume-preservation check
- kelvinlet_constrained.py  — constrained solve: 3n×3n linear system (Phase 1) + superposed eval (Phase 2) (Eq. 18/§5)
- kelvinlet_sharp.py        — full Sharp Kelvinlets family: Laplacian, Bi-Laplacian, Cusped Laplacian, Cusped Bi-Laplacian, blended (Eq. 15–18)
Created wiki/python/index.md with quick-start guide and parameter table.
Updated wiki/index.md with Python Snippets section.
Total: 4 modules, 13 functions, all with runnable __main__ examples. NumPy only.

## [2026-04-07] ingest | MeshGraphNets-related papers (4 papers)

Downloaded and ingested 4 papers extending MeshGraphNets for cloth/character simulation:
- MultiScale MeshGraphNets (Fortunato, Pfaff et al. — ICML AI4Science 2022)
  — Two-level V-cycle hierarchy (fine + coarse mesh); achieves spatial convergence; high-accuracy label training
- HOOD: Hierarchical Graphs for Generalized Clothing Dynamics (Grigorev, Black et al. — CVPR 2023)
  — Hierarchical message passing; self-supervised physics loss; single model for all garment types; handles topology changes
- N-Cloth: Predicting 3D Cloth Deformation with Mesh-Based Networks (Li, Manocha et al. — EG 2022)
  — Graph conv on arbitrary-topology meshes; 100K triangles at 30-45fps; SMPL + non-SMPL bodies
- Neural Cloth Simulation (Bertiche, Madadi, Escalera — ACM TOG SIGGRAPH Asia 2022)
  — First self-supervised cloth dynamics; disentangled static/dynamic encoder; inertia loss; motion intensity control

## [2026-04-07] vex | Blendshape Fitting VEX snippets extracted

Created 5 Houdini VEX snippets from JTDP03, FACEIT, and Lewis 2014 STAR (blendshape survey):
- blendshape-eval.vex           — delta (additive) and replacement forward pass (Lewis 2014, Eq. 1–4)
- blendshape-marker-softmax.vex — softmax marker-to-vertex correspondence R(P_j) (JTDP03)
- blendshape-qp-fit.vex         — QP weight solve from 3D markers: Python SLSQP + VEX apply (JTDP03)
- blendshape-nlls-faceit.vex    — 2D landmark projection (VEX) + NLLS LM weight solve (Python) (FACEIT)
- blendshape-corrective-psd.vex — corrective weight evaluation: product, min, Gaussian RBF (Lewis 2014 §3; Lewis 2000 PSD)
Updated wiki/vex/index.md with Blendshape Fitting section (39 total snippets across 11 papers).
