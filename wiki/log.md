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

## [2026-04-07] lint | Wiki lint pass

**Fixed:**
- index.md footer counts corrected: 99 papers (was 100), 32 authors (was 30)
- Added VEX Snippets section to index.md pointing to vex/index.md (39 snippets, not previously in main catalog)
- Flagged missing file: techniques/bandage-smoothing-vex.md (in index but not on disk)

**Orphan pages:**
- authors/aberman-kfir.md — no paper page links to this author; appears in log.md/index.md only. Author was added to wiki but no paper has been ingested for them yet.

**Missing concept pages (suggested):**
- concepts/mesh-graph-nets — 6 papers tagged mesh-graph-nets (pfaff-2021-meshgraphnets, libao-2023-meshgraphnetsrp, fortunato-2022-multiscale-mgn, grigorev-2023-hood, ranjan-2018-coma, li-2022-ncloth) with no dedicated concept page
- concepts/muscles — 6 papers tagged muscles with no dedicated concept page

**No broken wikilinks detected.**
**No contradictions detected.**

## [2026-04-07] concept | mesh-graph-nets

Created wiki/concepts/mesh-graph-nets.md.
Covers: flat MGN, hierarchical/multi-scale variants, production-mesh focus, architectural precursor (CoMA).
Links 6 papers: pfaff-2021-meshgraphnets, fortunato-2022-multiscale-mgn, grigorev-2023-hood, libao-2023-meshgraphnetsrp, li-2022-ncloth, ranjan-2018-coma.
Updated index.md (22 concepts total).

## [2026-04-07] concept | facial-blendshape-rigs + nonlinear-face-models

Created two concept pages covering 24 facial rigging and nonlinear face model papers:

**wiki/concepts/facial-blendshape-rigs.md**
Covers: muscle-based systems (PDI ANTZ, Animatomy), linear FACS rigs (Lewis STAR, DWA, Pixar IO2), PSD correctives, physics-enriched rigs (Bradley), baked rigs (FaceBaker), empirical controls (jaw rig), performance capture & rig inversion (JTDP03, Bermano, FACEIT).
Links 13 papers.

**wiki/concepts/nonlinear-face-models.md**
Covers: mesh autoencoders (CoMA, Compositional VAE, Mesh VAE+RIMD), CNN encoder-decoder (Nonlinear 3DMM), implicit neural (ImFace, ImFace++), neural detail on FLAME (DECA), diffusion appearance (DiffusionRig), neural blend shapes (Li 2021), cross-identity retargeting (sol-2025), neural auto-rigging (NFR, Hou, RigAnyFace, CANRIG).
Links 15 papers.

Updated index.md (24 concepts total).

## [2026-04-07] ingest | 14 nonlinear face model papers (neural search + retrieve)

Searched for and downloaded 14 recent papers on nonlinear facial rigging techniques not previously indexed:

**FLAME reconstruction lineage (MPI-IS):**
- EMOCA: Emotion Driven Monocular Face Capture and Animation (Danecek, Black, Bolkart — CVPR 2022)
- MICA: Towards Metrical Reconstruction of Human Faces (Zielonka, Bolkart, Thies — ECCV 2022)
- SMIRK: 3D Facial Expressions through Analysis-by-Neural-Synthesis (Retsinas et al. — CVPR 2024)

**Neural parametric head models (TUM/Nießner group):**
- NPHM: Learning Neural Parametric Head Models (Giebenhain et al. — CVPR 2023)
- HeadCraft: Modeling High-Detail Shape Variations for Animated 3DMMs (Sevastopolsky et al. — 3DV 2025)

**3D Gaussian avatar lineage:**
- GaussianAvatars: Photorealistic Head Avatars with Rigged 3D Gaussians (Qian et al. — CVPR 2024)
- 3D Gaussian Blendshapes for Head Avatar Animation (Ma et al. — SIGGRAPH 2024)
- NPGA: Neural Parametric Gaussian Avatars (Giebenhain et al. — SIGGRAPH Asia 2024)

**Rig generation from video:**
- High-Quality Mesh Blendshape Generation from Face Videos via Neural Inverse Rendering (Ming et al. — ECCV 2024)

**Diffusion-based shape models:**
- ShapeFusion: A 3D Diffusion Model for Localized Shape Editing (Potamias et al. — ECCV 2024)
- 4D Facial Expression Diffusion Model (Zou et al. — ACM TOMM 2024)

**NeRF-based face models:**
- MoFaNeRF: Morphable Facial Neural Radiance Field (Zhuang et al. — ECCV 2022)
- NOFA: NeRF-based One-shot Facial Avatar Reconstruction (Yu et al. — SIGGRAPH 2023)

**Retargeting:**
- FreeAvatar: Robust 3D Facial Animation Transfer by Learning an Expression Foundation Model (Qiu et al. — SIGGRAPH Asia 2024)

New authors: niessner-matthias (TUM), bolkart-timo (MPI-IS).
All 14 PDFs downloaded to raw/papers/.
Updated: index.md (113 papers, 34 authors), nonlinear-face-models concept page (to be updated separately).

## [2026-04-07] lint | Concept update + full lint pass

**Concept pages updated:**
- nonlinear-face-models.md — major expansion: added FLAME reconstruction lineage (EMOCA, MICA, SMIRK), NPHM/HeadCraft implicit SDF cluster, NeRF-based face models (MoFaNeRF, NOFA), 3DGS avatar cluster (GaussianAvatars, 3D Gaussian Blendshapes, NPGA), diffusion models (ShapeFusion, 4D Expression Diffusion), retargeting (FreeAvatar); representation evolution table; updated connections
- facial-blendshape-rigs.md — added: performance capture section extended (EMOCA, MICA, SMIRK); new "Rig Generation from Video" section (ming-2024); new "Retargeting" section (sol-2025, FreeAvatar)
- auto-rigging.md — added ming-2024-mesh-blendshapes
- digital-human-appearance.md — added neural geometry papers (DECA, EMOCA) and neural avatar rendering section (GaussianAvatars, Gaussian Blendshapes, NPGA, MoFaNeRF, NOFA, DiffusionRig)

**Orphan authors resolved:**
- aberman-kfir — added [[authors/aberman-kfir]] to li-2021-neural-blend-shapes
- bolkart-timo — added [[authors/bolkart-timo]] to danecek-2022-emoca, zielonka-2022-mica, retsinas-2024-smirk

**Missing technique file created:**
- techniques/bandage-smoothing-vex.md — bi-Laplacian bandage smoothing; two-pass Gauss-Seidel + cotangent variant; HDA setup

**Lint results:**
- 0 broken wikilinks
- 0 orphan author pages
- 0 index/filesystem mismatches
- Missing concept pages suggested: `muscles` (14 papers tagged, no page)
- Index footer corrected: 113 papers, 24 concepts, 34 authors, 3 techniques

Health: CLEAN

## [2026-04-07] concept | muscles

Created wiki/concepts/muscles.md.
Covers: facial muscle systems as rig controls (PDI ANTZ, DWA, Animatomy, jaw rig, Fabrig), full musculoskeletal simulation (Murai), soft tissue FEM (Smith Neo-Hookean, McAdams, Kim course, Projective Dynamics), physics-enriched rigs (Coros, Hahn rig-space physics, Bradley blendshape+FEM), neural surrogates (MeshGraphNets).
Links 14 papers. Includes Animatomy strain formula, flesh simulation material model comparison table, rig-space physics description.
Updated index.md (25 concepts total).

## [2026-04-09] vex | RBF (Radial Basis Function) Techniques

Created 6 VEX snippets covering all RBF algorithms referenced in the wiki:
- rbf-kernels.vex — complete kernel library (Gaussian, multiquadric, inv-MQ, TPS, linear, cubic, Wendland C2) with selection guide
- rbf-gram-matrix.vex — offline Gram matrix assembly (single-threaded wrangle) + Python Tikhonov solve (Φλ = F)
- rbf-eval.vex — runtime f(x) = Σλ_i φ(||x−x_i||); supports normalized Animatomy jaw style (rbf_normalize=1)
- rbf-psd-pose.vex — three pose parameterization modes: blendshape weights (MetaHuman), quaternion, rotation-matrix delta (SMPL/Animatomy)
- rbf-psd-correctives.vex — full Pose Space Deformation pipeline: per-corrective Gaussian RBF → weight → apply delta to @P; complexity analysis for MetaHuman 1000+ correctives
- rbf-scattered-interp.vex — 3D scattered data interpolation; Waters 1987 linear + sphincter muscle influence zones inline

Updated: vex/index.md (new RBF section with pipeline diagrams, kernel guide table, 39 → 45 snippets), index.md footer (39 → 45 VEX).
Sources: [[papers/lewis-2000-psd]] [[papers/choi-2022-animatomy]] [[papers/epic-2021-metahuman-rig]] [[papers/waters-1987-muscle-model]]

## [2026-04-09] query | MetaHuman rig internal architecture

Researched MetaHuman Creator facial rig technical internals. Created wiki/papers/epic-2021-metahuman-rig.md and wiki/queries/metahuman-rig-internals.md.

Key findings: DNA four-layer format (Descriptor/Definition/Behavior/Geometry); RigLogic y=Kx linear evaluation with dense block-partitioned joint groups (~6× vs sparse CRS); ~200 FACS controls → 258–669 blendshapes + 397–713 joints; 1,000+ PSD/RBF corrective shapes; 8 head LODs; identical evaluation in Maya + UE via RigLogicModule. Open-sourced DNA Calibration library Nov 2022.

Updated: concepts/facial-blendshape-rigs (new "Production Real-Time Rigs" subsection), index.md (150 papers).

## [2026-04-09] ingest | Muscle-Based Face Systems — 21-paper batch

Created 21 wiki paper pages covering the muscle-based facial animation and physics face simulation literature:

**Foundational (1987–1995):** waters-1987-muscle-model, terzopoulos-1990-physically-based-face, terzopoulos-1993-facial-analysis, lee-1995-realistic-face-modeling

**ILM/Fedkiw FEM Pipeline (2005–2019):** teran-2005-quasistatic-flesh, sifakis-2005-anatomy-muscles, sifakis-2006-speech-muscle, cong-2015-anatomy-pipeline, cong-2016-art-directed-blendshapes, cong-2017-kong-muscle-talk, bao-2019-face-capture-muscles

**EPFL Physics Face Models (2017–2019):** ichim-2017-phace, kadlecek-2019-physics-face-data

**Disney Research Zürich Cluster (2020–2024):** zoss-2020-secondary-dynamics-capture, yang-2023-implicit-physical-face, yang-2024-generalized-physical-face, chandran-2024-anatomically-constrained-face

**Realtime & Neural Physics (2021–2024):** zeng-2021-neuromuscular-face, wagner-2023-softdeca, park-2024-realtime-face-sim-superres

**DWA Production (2017):** lan-2017-digipro

Created 13 new author pages: waters-keith, terzopoulos-demetri, fedkiw-ronald, teran-joseph, cong-matthew, bao-michael, ichim-alexandru, pauly-mark, kadlecek-petr, yang-lingchen, chandran-prashanth, zoss-gaspard, wagner-nicolas, zeng-xiao, park-hyojoon, lan-lana.

Massively expanded concepts/muscles.md to include all 21 new papers with full taxonomy (foundational → production → ILM pipeline → EPFL → Disney Research → realtime).

Updated index.md: 128 → 149 paper pages, 34 → 47 authors. Re-sorted papers table by tag.

## [2026-04-08] ingest | Neural Face Skinning for Mesh-agnostic Facial Expression Cloning (Cha et al., EG 2025)

Ingested 2505.22416.pdf. Created wiki/papers/cha-2025-neural-face-skinning.md.
Key contribution: topology-agnostic FACS-compatible skinning weight prediction via indirect FACS segmentation supervision; global latent deformation + local skinning decoder; handles highly stylized non-human characters.
Updated: concepts/nonlinear-face-models (added to Neural Facial Auto-Rigging table and Connections), concepts/auto-rigging (added to Key Papers), concepts/speech-driven-animation (added topology lock-in note + cross-link). New concept connections: linear-blend-skinning, blendshapes, sol-2025, riganyface.

## [2026-04-09] vex | Forearm Partial Twist — Swing-Twist Decomposition

Indexed forearm-partial-twist.vex in vex/index.md (was created but not indexed).
Added new section: Forearm Twist / Swing-Twist Decomposition.
- forearm-partial-twist.vex — quaternion swing-twist decomposition for forearm pronation/supination; slerp(identity, twist_q, t) produces a partial twist joint at fraction t along the forearm

Total: 45 → 46 VEX snippets. Updated index.md footer count.

## [2026-04-09] technique | Forearm Partial Twist

Created wiki/techniques/forearm-partial-twist.md — full technique page covering:
- The candy-wrapper problem and why LBS / DQS / CoR don't fully solve it
- Swing-Twist quaternion decomposition theory and step-by-step algorithm
- VEX implementation guide (Geometry Wrangle SOP, parameter table, key formulas)
- Python implementation guide (forearm_partial_twist.py)
- KineFX integration notes + auto-derive twist axis from skeleton
- Gotchas: hemisphere flip for >180° rolls, twist axis verification, scale in transforms, joint count tradeoffs
- Comparison table: plain LBS vs partial twist vs DQS vs CoR vs PSD

Created wiki/python/forearm_partial_twist.py — NumPy module with:
- `relative_quaternion`, `swing_twist_decompose`, `partial_twist_xform`, `build_forearm_chain`
- Houdini Python SOP helper (run_in_houdini_python_sop)
- Runnable __main__ demo (90° pronation test; verifies ~30°/60° fractional twists)

Updated: python/index.md (4 → 5 modules, 13 → 17 functions), vex/index.md (technique cross-link added), index.md (3 → 4 techniques, 4 → 5 Python snippets).

## [2026-04-09] lint | Wiki lint pass

**Fixed:**
- `papers/chan-2022-eg3d.md` line 39: `[[papers/nguyen-2023-next3d]]` → `[[papers/sun-2023-next3d]]` (wrong author in slug; paper is by Sun et al. CVPR 2023)
- `wiki/index.md` footer: author count 47 → 50 (three authors added in muscle-batch ingest were not counted)

**No issues:**
- 0 broken wikilinks remaining (1 fixed above)
- 0 orphan pages — all 150 papers, 25 concepts, 50 authors, 4 techniques referenced from index or cross-links
- 0 index/filesystem mismatches — 150 paper files, 25 concepts, 50 authors, 4 techniques all match index table
- 0 concept pages missing — all tags in use have dedicated pages
- 0 technique pages missing — forearm-partial-twist.md added this session

Health: CLEAN

## [2026-04-10] ingest | FACS investigation — concept + 2 papers

Researched FACS (Facial Action Coding System) literature. Identified that FACS was referenced in 31 wiki files but had no dedicated concept page and no paper page for the foundational Ekman & Friesen manual.

**Created:**
- `wiki/concepts/facs.md` — comprehensive FACS concept page: 44 AU table (upper/lower face + head/gaze), intensity A–E scale, bilateral AU conventions, 7 universal expressions with FACS signatures, CG blendshape naming conventions (ARKit, ICT FaceKit, MetaHuman/DNA, Maya), FACS as neural supervision signal (NFR, RigAnyFace, CANRIG, Cha 2025), muscle vs FACS comparison, implementation notes (bilateral AUs, anti-synergies, intensity mapping), key papers table, and external URL references (Paul Ekman Group, CMU FACS, Py-Feat, Melinda Ozel cheat sheet, OpenFACS, FACSvatar)
- `wiki/papers/ekman-friesen-1978-facs.md` — the canonical 1978 FACS manual; full paper page with method, key results, limitations, production implementation notes, and two representative quotes
- `wiki/papers/deng-noh-2007-facial-animation-survey.md` — 2007 Springer CG facial animation survey; bridges FACS psychophysical literature with CG blendshape, muscle, and performance capture pipelines

**Updated:**
- `concepts/blendshapes.md` — FACS section now links [[concepts/facs]] and [[papers/ekman-friesen-1978-facs]]
- `concepts/facial-blendshape-rigs.md` — FACS paragraph and Connections section now link [[concepts/facs]]
- `index.md` — facs concept added to Concepts table; 2 new papers added in blendshapes group; VEX count corrected (45→46); footer updated (150→152 papers, 25→26 concepts)

**External URLs researched and referenced in concepts/facs.md:**
- https://www.paulekman.com/facial-action-coding-system/ — official FACS 2002 manual
- https://www.cs.cmu.edu/~face/facs.htm — CMU AU reference
- https://py-feat.org/pages/au_reference.html — Py-Feat AU table
- https://melindaozel.com/facs-cheat-sheet/ — practitioner AU guide
- https://melindaozel.com/arkit-to-facs-cheat-sheet/ — ARKit→FACS mapping
- https://github.com/phuselab/openFACS — OpenFACS open source toolkit
- https://github.com/NumesSanguis/FACSvatar — FACSvatar real-time pipeline

## [2026-04-10] ingest | ARKit and OpenXR face tracking formats

Investigated ARKit and OpenXR as real-time facial animation standards. Both were referenced in the wiki but had no dedicated concept pages.

**Created:**

`wiki/concepts/arkit-blendshapes.md`
Apple ARKit Face Tracking: TrueDepth camera architecture (30K dot IR, 1,220-pt mesh, 60 Hz); full canonical list of 52 blend shape names grouped by region (eyes 14, brows 6, nose 2, jaw 4, mouth/lips 24, cheeks 2); ARKit→FACS spot mapping table; engine integration (Unreal Live Link Face: pipeline + timecode sync; Unity ARFoundation: ARFaceManager, SkinnedMeshRenderer); MetaHuman 52-name streaming layer; ARKit as research data source (SAiD, UniTalker, REFA, Express4D); standardization position table vs FACS/OpenXR/MPEG-4; 8 external URLs.

`wiki/concepts/openxr-face-tracking.md`
Khronos OpenXR face tracking extensions: XR_FB_face_tracking (Meta, 70 FACS-derived weights, xrGetFaceExpressionWeightsFB, confidence per region); XR_FB_face_tracking2 (multimodal visual+audio, xrGetFaceExpressionWeights2FB); XR_HTC_facial_tracking (HTC, 37 eye + 52 ARKit-compatible lip weights, separate create/query per type); XR_EXT_eye_gaze_interaction (gaze direction only, not weights); weight count comparison table; cross-platform rig strategy (52 ARKit-named blendshapes work across iPhone, Quest Pro, Vive XR Elite); engine integration (Unreal: VIVE OpenXR+MetaHuman, Meta Movement SDK; Unity: Meta Movement SDK, HTC OpenXR, Android XR); Meta 70 vs ARKit 52 delta explained; 11 external URLs + Khronos spec links.

`wiki/papers/deng-2023-facial-capture-survey.md`
Springer 2023 survey on facial capture pipeline evolution: hardware (markers→RGB-D→ARKit), tracking algorithms (FLAME fitting, neural reconstruction), FACS as intermediate representation, real-time delivery (Live Link Face, OpenXR), MetaHuman integration. Modern update to the 2007 survey by same first author.

**Updated:**
- `concepts/facs.md` — added "Real-Time Implementations" section pointing to ARKit and OpenXR concept pages
- `concepts/facial-blendshape-rigs.md` — Connections section now links [[concepts/arkit-blendshapes]] and [[concepts/openxr-face-tracking]]
- `index.md` — 2 new concepts added (arkit-blendshapes, openxr-face-tracking); 1 new paper; footer updated (152→153 papers, 26→28 concepts)

**Key finding:** ARKit's 52-weight parameterization is now the de facto interchange format across Apple, Epic MetaHuman, HTC OpenXR, and Unity/Unreal pipelines. OpenXR extensions explicitly designed for ARKit compatibility (HTC 52-weight lip component). A rig built on ARKit-named blendshapes works across all current XR platforms without remapping.

## [2026-04-09] ingest | Putting Rigid Bodies to Rest (Baktash, Sharp, Zhou, Jacobson, Crane — ACM ToG / SIGGRAPH 2025)

Downloaded paper content via project page and GitHub README (DOI: 10.1145/3731203).
Created `wiki/papers/baktash-2025-resting-rigid-bodies.md`.

Key contribution: pure geometric characterization of all stable resting orientations and their exact probabilities for convex rigid bodies via the Morse-Smale complex of the support function over the Gauss sphere. Enables inverse design (fair/loaded dice, orientation-biased props) at interactive speed.

New author pages: `wiki/authors/crane-keenan.md` (CMU; DDG, heat method, conformal geometry), `wiki/authors/sharp-nicholas.md` (NVIDIA; Polyscope, geometry processing, 3D ML). Updated: `wiki/authors/jacobson-alec.md` (added baktash-2025 to Papers in Wiki).

## [2026-04-09] vex | Rigid Body Resting Analysis VEX snippets

Created `wiki/vex/rigid-body-rest-analysis.vex` — 4 Houdini Geometry Wrangle snippets covering the full Baktash 2025 pipeline:

- **Snippet A** (Over Points) — Support function h(n) = max_{x∈K} n·x; also computes V(n) = h(-n) (COM height / potential energy). Outputs `@support_h`, `@support_pt`, `@potential_V`.
- **Snippet B** (Over Primitives) — Face stability check: projects COM onto face plane, performs 2D winding-number point-in-polygon test in local face frame. Outputs `@stable` (int), `@margin` (float — signed distance to nearest edge).
- **Snippet C** (Over Primitives) — Resting probability from precomputed spherical Voronoi cell areas: `@rest_prob = is_stable ? voronoi_area[@primnum] / 4π : 0.0`.
- **Snippet D** (1-point geo, For-Each) — Quasi-static drop step: slerps toward face normal with lowest V(n); sets `contact_n`, `contact_type`, `settled` state attributes. Full Houdini pipeline setup guide in header comment.

Updated `wiki/vex/index.md`: added Rigid Body Resting Analysis section with parameter table and key formulas. Total: 46 → 50 VEX snippets.

## [2026-04-09] python | Rigid Body Resting Analysis Python module

Created `wiki/python/rigid_body_rest.py` — complete NumPy/SciPy implementation:

Functions:
- `support_function(vertices, directions)` — vectorized h(n) via numpy matmul
- `potential_energy(vertices, normals)` — V(n) = h(-n) for all query normals
- `convex_hull_gauss_map(vertices)` — scipy ConvexHull wrapper; returns face normals, areas, COM
- `check_face_stability(hull, vertices, com)` — COM inside face → 2D cross-product test; returns (stable bool[], margins float[])
- `compute_spherical_voronoi_areas(face_normals)` — scipy SphericalVoronoi; handles duplicate normals (parallel faces) via np.unique with uniform fallback
- `resting_probabilities(vertices, com)` — full pipeline dict; prob[i] = voronoi_area[i] / 4π if stable
- `drop_trajectory(vertices, com, n0, steps, step_size)` — (T,3) gradient descent on S²; tangent-plane finite-difference gradient; snaps to face normal when cos > 0.999
- `inverse_design_target_probs(vertices, com, target_face_idx, target_probs, iters, lr)` — numerical gradient on vertex positions; returns (verts_opt, loss_history)
- `run_in_houdini_python_sop(node)` — writes stable, rest_prob, margin prim attrs + voronoi_area detail array + com detail vector

Runnable __main__ demo: unit cube (expect 6 stable faces ~1/6 each) + regular tetrahedron (4 faces ~1/4 each).

Updated `wiki/python/index.md`: added Rigid Body Resting Analysis section. Total: 5 → 6 Python modules, 17 → 26 functions.
Updated `wiki/index.md`: added baktash-2025 paper, crane-keenan and sharp-nicholas authors, updated VEX/Python counts in footer and VEX section text.
