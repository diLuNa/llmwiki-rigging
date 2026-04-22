# Wiki Log

Append-only chronological record of all wiki activity.

Format: `## [YYYY-MM-DD] <operation> | <title>`

---

## [2026-04-22] update | Switch to 3-segment muscle features
- `jaw_muscle_synthesis.py`: replaced scalar `muscle_stretch_ratio` with `resample_uniform` + `muscle_segment_ratios`; `N_SEGMENTS=3` constant; `extract_biomechanical_signals` returns (N, M*3) + segment feature names
- `nonlinear_face_model.py`: demo updated to M=11×3=33; `neutral_anchor_loss` simplified using `model.n_muscles`; `NonlinearFaceModel` stores `n_muscles` attribute
- Both exploration pages updated: architecture diagrams, input dim notes, muscle section rewritten

## [2026-04-22] exploration | Nonlinear face model — moving beyond PCA
- Created `wiki/explorations/nonlinear-face-model.md`
- Created `wiki/python/nonlinear_face_model.py`
- Architecture: IdentityEncoder (neutral mesh → z_id 64-dim) + MLPDecoder or UVConvDecoder
- 6D continuous rotation representation for jaw SE(3) (no quaternion ambiguity)
- Loss: vertex L1 + Laplacian + neutral anchor
- Multi-subject HDF5 dataset, FaceModelTrainer with cosine schedule + gradient clipping
- synthesize() and cache_identity() inference API
- Houdini Python SOP integration for real-time rig preview

## [2026-04-22] exploration | Jaw + muscle driven face mesh synthesis
- Created `wiki/explorations/jaw-muscle-driven-synthesis.md`
- Created `wiki/python/jaw_muscle_synthesis.py`
- Four synthesis approaches: linear regression, KNN blending, MLP decoder, Houdini Python SOP
- Jaw SE(3) extraction via SVD Procrustes, muscle stretch ratio from polyline length
- Muscle attachment index definitions for FLAME 5023-vertex topology (11 muscles)
- Correlation analysis function: which muscles drive which PCA expression components

## [2026-04-22] lint | Wiki health pass
- Fixed slug mismatches: `kavan-2008-dqs` → `kavan-2007-dqs`, `smith-2018-stable-neohookean` → `smith-2018-neo-hookean`
- Removed dead link to `aberman-2017-style-transfer` (replaced with prose note)
- Created author stubs: `authors/bradley-derek`, `authors/ng-thow-hing-victor`
- Created concept page: `concepts/neural-blend-shapes`
- Indexed orphan pages in `index.md`: `explorations/facs-pose-tsne`, `queries/metahuman-rig-internals`, 4 new author entries
- Remaining known gaps (not ingested): `papers/magnenat-thalmann-1988-lbs`, `papers/kavan-2007-dqs` (stub only), `papers/aberman-2017-style-transfer`

## [2026-04-22] exploration | FACS-guided t-SNE clustering of face expression poses

Context: PCA face model (253 identity + 382 expression params), 100k animated poses.

- Created `wiki/explorations/facs-pose-tsne.md`
- Created `wiki/python/facs_pose_tsne.py`
  - Option A: pre-PCA → UMAP/t-SNE directly on 382 expression params
  - Option B: decode to mesh → per-FACS-region mean displacement features → UMAP/t-SNE
  - Dominant-region labelling for FACS-type colouring
  - Per-region activation subplot grid for verification
  - FLAME-topology region masks for 18 AU-aligned vertex groups
  - Batched decode loop (handles 100k × V × 3 without OOM)

## [2026-04-22] ingest | Deep-dive articles — Melinda Ozel (Face the FACS) × 12

Sources (all premium, accessed via member session):
- /upper-lip-raiser-vs-nasolabial-furrow-deepener/ & /levator-labii-superioris-vs-zygomaticus-minor/ — AU10 vs AU11
- /forehead-dynamics-frontalis-vs-occipitalis/ — frontalis/occipitalis anatomy
- /lip-tightener-vs-lip-presser/ & /lip-tightener/ — AU23 horizontal vs vertical lip tightener
- /advanced-blend-shape-tips-for-blinks/ — blinkles, blink timing asymmetry
- /all-about-upper-lid-raiser-au5/ — AU5 levator palpebrae anatomy, emotion roles
- /zygomaticus-major-variations-the-dimple/ — bifid zyg major causes dimples
- /frontalis-variation/ — frontalis shape diversity and per-subject AU1/AU2 variation
- /inner-brow-raiser-deep-dive/ — AU1 corrugator contamination, effects
- /a-wrinkle-in-time-part-ii/ — static wrinkles taxonomy
- /a-wrinkle-in-time-building-characters-with-real-story-lines/ — dynamic wrinkles, storytelling
- /breaking-down-nose-wrinkler/ — AU9 full expression context, AU38 note

Pages created/updated:
- Created `wiki/queries/melindaozel-deep-dives.md`
- Updated `wiki/concepts/facs.md` — added Production Gotchas section (13 items)
- Updated `wiki/concepts/wrinkle-systems.md` — added anatomical wrinkle taxonomy
- Updated `wiki/index.md`

## [2026-04-22] ingest | Viseme & Speech Reference Guide — Melinda Ozel (Face the FACS)

Source: https://melindaozel.com/viseme-speech-guide/ (premium, accessed via member session).  
Full American English viseme group catalogue: 13 consonant groups, 2 consonant blends, 10 vowel groups.  
Each group includes IPA, example words, phoneme classification (place + manner + voicing). Vimeo video references per phoneme.

- Created `wiki/concepts/visemes-speech.md`
  - Complete viseme group table with IPA, example words, phoneme classification
  - p/b/m production notes (nasal vs. plosive distinction; 3-phase model; labiodental affricate edge case)
  - Viseme→FACS AU mapping for key groups
  - Production rig notes (Preston Blair, ARKit, NVIDIA Maxine)
  - Coarticulation discussion
- Updated `wiki/index.md`

## [2026-04-22] ingest | ARKit to FACS Translation Guide — Melinda Ozel (Face the FACS)

Source: https://melindaozel.com/arkit-to-facs-translation-guide/ (premium, accessed via member session).  
Complete verified ARKit→FACS→muscle mapping table (33 entries). Includes critical production notes not in Apple docs.

- Updated `wiki/concepts/arkit-blendshapes.md`
  - Replaced partial mapping table with complete Melinda Ozel verified table (all 33 ARKit shapes)
  - Added critical notes: mouthShrugUpper contingency; ICT-FaceKit mistranslation warning
  - Added missing AUs section (AU11, AU13, AU23, AU38, AU39, vertical lip tightener)
  - Clarified gaze direction encoding (M61/M62/M63/M64/M65/M66)
  - Clarified AU26 vs AU27 distinction for jawOpen
- Updated `wiki/index.md`

## [2026-04-22] query | Face the FACS — FACS Video References (melindaozel.com)
## [2026-04-22] query | Face the FACS — Emotion References (melindaozel.com)
## [2026-04-22] query | Face the FACS — Upper Face Expanded (melindaozel.com)
## [2026-04-22] query | Face the FACS — Eyebrow Combos & Lower Face Cheat Sheets (melindaozel.com)

## [2026-04-17] technique | ACES Color Management in DCC

New source: `raw/assets/An Idiot's Guide to ACES.md` — toadstorm.com blog (2020-02-25).

- Created `wiki/techniques/aces-color-management.md`
  - ACEScg vs sRGB primaries; ACES pipeline flow; RRT S-curve
  - IDT conversion table: color textures (convert) vs data textures (do not convert)
  - OCIO setup (env var, config download)
  - Per-DCC setup: Houdini (OCIO VOP, COPs caveat), Maya, Fusion, Nuke
  - Gotchas: self-illuminated materials, brand colors, RRT pre-inversion trick, floating-point write requirements
- Updated `wiki/index.md`

## [2026-04-17] ingest | Revisiting Parallel Transport (toadstorm blog)

New source: `raw/assets/Revisiting Parallel Transport.md` — toadstorm.com blog (2026-04-16).

Extended parallel transport coverage with vertex-connectivity approach:
- Updated `wiki/techniques/parallel-transport.md`
  - Added Application 4: `kinefx_hierarchy.h` approach (`getchildren()`/`getparent()`)
  - Three tangent modes (forward, backward, averaged) with comparison
  - `orient` quaternion output via `maketransform()` + `quaternion()`
  - Per-point roll/pitch/yaw via `qrotate()` + `qmultiply()`
  - Added row-vs-column convention gotcha (`rotate()` vs `dihedral()`)
  - Updated VEX Reference table to include Snippet C
- Updated `wiki/vex/parallel-transport.vex` — added Snippet C (full implementation)
- Updated `wiki/vex/index.md` — added Snippet C row; health summary updated to 56 snippets
- Updated `wiki/index.md`

## [2026-04-17] technique | Parallel Transport

Created full technique page and VEX implementations for parallel transport in character rigging.

- Created `wiki/techniques/parallel-transport.md`
  - Covers three applications: Bishop frame along polyline curves, BFS mesh surface propagation (Pinskiy 2010), forearm twist axis chains
  - `dihedral()` VEX primitive as the unified discrete operator
  - Bishop vs Frenet comparison table, holonomy and Gauss-Bonnet theorem, torsion correction (CurveNet)
  - Gotchas: near-antipodal normals, re-projection after transport, closed curve holonomy, row-vector convention
- Created `wiki/vex/parallel-transport.vex`
  - Snippet A: Per-primitive Geometry Wrangle — full Bishop frame propagation with optional torsion correction; outputs `@pt_T`, `@pt_N`, `@pt_B`
  - Snippet B: Per-point single dihedral transport step (BFS building block); includes antipodal-normal fallback
- Updated `wiki/vex/index.md` — added Parallel Transport section with parameter guide and key formulas; health summary updated to 55 snippets
- Updated `wiki/index.md` — added technique row, updated VEX count to 55, updated footer

## [2026-04-17] sweep | Raw assets consolidation (7 md files in raw/assets/)

All 7 markdown files in `raw/assets/` were previously ingested (sessions 2026-04-14 to 2026-04-16). Gap-fills applied:
- `wiki/papers/marquis-bolduc-2022-differentiable-rig.md` — added EA SEED video URL and paper download link
- `wiki/papers/holden-2015-inverse-rig.md` — expanded External References (blog post, paper PDF, SCA 2015 video, Filmakademie video)
- `wiki/papers/mirrored-anims-2025-rig-retargeting.md` — added `doi: 10.1145/3769047.3769064` to frontmatter

## [2026-04-16] ingest | Biomechanical Face Model Architecture Design

New source: `raw/assets/face model architecture.pdf` — 7-page design conversation log for the wiki's own face model project.

- Created `wiki/concepts/biomechanical-face-model-architecture.md`
  - Architecture: PCA identity encoding (64-dim) + expression encoding (muscle stretch ratios + jaw SE(3), 47-dim) → MLP trunk (111→2048, LayerNorm+GELU) → Conv upsample in UV space → vertex deltas
  - Design decisions table, loss functions (vertex L1 + Laplacian + neutral anchor + optional disentanglement), HDF5 data format, project structure, next steps
- Updated `wiki/index.md`
- Updated `wiki/log.md`

## [2026-04-16] ingest | MIRRORED-Anims + Latent Generative Modelling

New sources from raw/assets/:

**MIRRORED-Anims** (`raw/assets/MIRRORED-Anims_...md`):
- Created `wiki/papers/mirrored-anims-2025-rig-retargeting.md`
- Updated `wiki/concepts/rig-inversion.md` — added analytic template inversion variant and key paper entry
- Updated `wiki/papers/holden-2015-inverse-rig.md` — added MIRRORED-Anims cross-link and Filmakademie student implementation note

**Generative Modelling in Latent Space** (Dieleman 2025 blog, `raw/assets/Generative modelling in latent space.md`):
- Created `wiki/concepts/latent-generative-modelling.md` — covers two-stage recipe, TSR, KL regularisation, VQGAN lineage, latent diffusion, relevance to neural face models

Both pages added to `wiki/index.md`.

## [2026-04-16] research | OpenXR ↔ ARKit blend shape relationship

Researched OpenXR face tracking extensions and their relationship to ARKit blend shape coefficients. Sources consulted: Khronos OpenXR Registry, Meta developer docs, Apple developer docs, Unity ARKit/AndroidXR packages, VRCFaceTracking Unified Expressions, Melinda Ozel ARKit-FACS mapping.

Updated pages:
- `wiki/concepts/openxr-face-tracking.md` — added full 70-weight XR_FB_face_tracking2 enumeration with descriptions; Android XR / Jetpack XR 68-shape extension; audio-to-expression multimodal section; Unified Expressions interop section; updated weight count table; expanded external resources
- `wiki/concepts/arkit-blendshapes.md` — added `tongueOut` as explicit tongue section; noted ARKit's 1 tongue weight vs Meta's 7; added Unified Expressions connection

Created pages:
- `wiki/concepts/unified-expressions.md` — full ARKit 52→Unified Expressions name mapping table; ~100 base shape enumeration; driver support matrix (ARKit / Meta / HTC / ML2 / Android XR); comparison table ARKit vs Unified for practical rig decisions

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

## [2026-04-13] lint | Wiki lint pass

**Broken links fixed (2):**
- `singleton-2025-alien-rigs.md` line 19: `[[Hessler & Talbot 2016]]` → `([[authors/hessler-mark]] & Talbot 2016)` (citation-style link, not a valid wikilink)
- `singleton-2025-alien-rigs.md` line 21: `[[Speirs et al. 2024]]` → `([[authors/speirs-jacob]] et al. 2024)` (same issue)

**False positive (no action needed):**
- `[[ia, ib, ic]]` in `cage-green-coords.vex` — NumPy fancy indexing `cage_verts[[ia, ib, ic]]` inside a Python code comment; not a wikilink.

**Noted (not fixable — log is append-only):**
- `[[papers/nguyen-2023-next3d]]` in `log.md` historical entry — file was renamed to `sun-2023-next3d.md` and was fixed in the source paper last session, but the log record remains.

**No issues:**
- 0 orphan pages — all 154 papers, 28 concepts, 52 authors, 4 techniques have inbound links
- 0 index/disk mismatches — 154 papers, 28 concepts, 52 authors, 4 techniques all match index table
- Footer counts verified correct (154 papers, 28 concepts, 52 authors, 4 techniques, 50 VEX snippets, 6 Python modules)

Health: CLEAN

## [2026-04-13] ingest | Dem Bones — Skinning Decomposition Technique

Researched "Dem Bones" and identified it as the EA SEED open-source C++ library implementing SSDR (Smooth Skinning Decomposition with Rigid Bones). The primary SSDR paper (Le & Deng 2012) was already in the wiki. Ingested the follow-up SIGGRAPH 2014 paper and created a full technique page.

**Created:**
- `wiki/papers/le-2014-skeletal-rigging.md` — "Robust and Accurate Skeletal Rigging from Mesh Sequences" (Le & Deng, ACM ToG SIGGRAPH 2014, DOI: 10.1145/2601097.2601161). Extends SSDR with joint position estimation via closed-form least-squares, weight smoothness regularization (Laplacian term), and automated bone pruning. Generates complete skeletal rig (joints + hierarchy + weights) from mesh sequences alone.
- `wiki/techniques/dem-bones.md` — Full technique page: what Dem Bones is, 3 operating modes (auto joints+weights / weight-solving given skeleton / transform-solving given weights), Houdini Dem Bones Skinning Converter SOP parameter guide + pipeline diagram, algorithm pseudocode (SSDR alternating opt + joint update), comparison table (SSDR vs Le 2014 vs Dem Bones vs Maya Bake Deformer vs RigNet), 5 production use cases, 5 external URLs.

**Updated:**
- `wiki/papers/le-2012-ssdr.md` — added Connections to le-2014-skeletal-rigging and techniques/dem-bones; updated Implementation Notes to reference the Houdini SOP; added 3 External References
- `wiki/authors/le-binh.md` — added le-2014-skeletal-rigging to Papers in Wiki
- `wiki/index.md` — added le-2014-skeletal-rigging to skinning group, added dem-bones to Techniques table; footer updated (154→155 papers, 4→5 techniques)

**External URLs researched and referenced:**
- https://github.com/electronicarts/dem-bones — EA SEED official library (BSD 3-Clause, C++, Eigen+OpenMP)
- https://www.ea.com/seed/news/open-source-dem-bones — EA announcement + production context (in use since 2015)
- https://www.sidefx.com/docs/houdini/nodes/sop/dembones_skinningconverter.html — Houdini SOP full documentation
- https://sidefxlabs.artstation.com/projects/AqOz4L — SideFX Labs showcase
- https://robertjoosten.github.io/projects/dem_bones/ — Maya implementation reference
- https://binh.graphics/papers/2014s-ske/ — Le 2014 author project page
- https://doi.org/10.1145/2601097.2601161 — ACM DL

## [2026-04-13] ingest | ML Deformer — Neural Deformation Approximation

Researched "ML Deformer" and discovered it is both a Houdini 20+ official tool and a technique family for neural facial/body rig approximation. No single originating paper, but a convergence of related SIGGRAPH 2020 works.

**Created:**
- `wiki/papers/bailey-2020-fast-deep-facial.md` — "Fast and Deep Facial Deformations" (Bailey, Omens, Dilorenzo, O'Brien; SIGGRAPH 2020, DOI: 10.1145/3386569.3392397). CNN-based decomposition: v_final = v_LBS + CNN(pose_params). 17× speedup on hero facial rigs. [GitHub](https://github.com/stephen-w-bailey/fast-n-deep-faces).
- `wiki/papers/song-2020-differential-subspace.md` — "Accurate Face Rig Approximation with Deep Differential Subspace Reconstruction" (Song, Shi, Reed; Blue Sky Studios; SIGGRAPH 2020, DOI: 10.1145/3386569.3392491). Differential coordinate approach: learns offsets in Laplacian space, reconstructs via harmonic solve. Smoother error distribution than CNN.
- `wiki/papers/arcelin-2024-ml-deformer-crowds.md` — "Implementing a Machine Learning Deformer for CG Crowds: Our Journey" (Arcelin, Maraux, Chaverou; Golaem; DIGIPRO 2024, arXiv:2406.09783, DOI: 10.1145/3665320.3670994). Production case study comparing Bailey/Song/Li/Radzihovsky approaches; selected Song 2020 for Golaem pipeline.
- `wiki/techniques/ml-deformer.md` — Full technique page: what ML Deformer is, the problem it solves, 4 architectural approaches (CNN residual, differential subspace, joint learning, FaceBaker hierarchical), Houdini SOP setup (ML Train Deformer + ML Deform), training best practices, 5 use cases, comparison table, 5 external URLs.

**Created author pages:**
- `wiki/authors/bailey-stephen.md` — UC Berkeley / Industry; Neural deformation approximation pioneer
- `wiki/authors/song-steven.md` — Blue Sky Studios; Differential subspace deformation learning
- `wiki/authors/arcelin-bastien.md` — Golaem; ML deformer production implementation

**Updated:**
- `wiki/papers/radzihovsky-2020-facebaker.md` — Connections now link to bailey-2020, song-2020, arcelin-2024, li-2021, techniques/ml-deformer
- `wiki/papers/li-2021-neural-blend-shapes.md` — Connections now link to bailey-2020, song-2020, radzihovsky-2020, techniques/ml-deformer
- `wiki/index.md` — added bailey-2020 and song-2020 papers, arcelin-2024 paper, ml-deformer technique, 3 new authors (bailey-stephen, song-steven, arcelin-bastien); footer updated (155→158 papers, 52→55 authors, 5→6 techniques)

**External URLs researched and referenced:**
- https://github.com/stephen-w-bailey/fast-n-deep-faces — Bailey CNN implementation (BSD licensed)
- https://github.com/PeizhuoLi/neural-blend-shapes — Li et al. neural blend shapes (from li-2021)
- https://www.sidefx.com/docs/houdini/ml/mldeformer.html — Houdini official ML Deformer SOP documentation
- https://www.sidefx.com/docs/houdini/nodes/sop/ml_deform.html — ML Deform SOP node docs
- https://www.sidefx.com/contentlibrary/ml-deformer/ — SideFX Labs content library (H20/20.5 examples)
- https://arxiv.org/abs/2406.09783 — Arcelin et al. arXiv preprint

**Key Finding:** ML Deformer is a convergence of 4 distinct 2020 approaches (Bailey CNN, Song differential, Radzihovsky hierarchical, plus Li's end-to-end); no single paper. Houdini 20 integrated this as official ONNX-based ML Train Deformer + ML Deform SOPs. Production validation: Golaem selected Song 2020 approach; Pixar validated FaceBaker; Bailey approach widely used in industry.

## [2026-04-13] ingest | SIGGRAPH 2020-2025 Character Rigging Papers (23 papers)

Completed comprehensive ingestion of 23 remaining SIGGRAPH character rigging papers (2020-2025), bringing total ingested papers from this research batch to 27. All papers cover core rigging, animation, facial, hand, and motion synthesis topics.

**SIGGRAPH 2025 Papers (5):**
- `wiki/papers/zheng-2025-autokeyframe.md` — Autoregressive keyframe generation from mixed dense/sparse motion controls
- `wiki/papers/he-2025-lam.md` — Large avatar model for one-shot animatable Gaussian head synthesis
- `wiki/papers/wu-2025-animportrait3d.md` — Text-based animatable 3D avatars with morphable model alignment
- `wiki/papers/he-2025-3dgh.md` — 3D head generation with composable hair and face components
- `wiki/papers/lan-2025-jgs2.md` — Near second-order Jacobi/Gauss-Seidel GPU elastodynamics solver

**SIGGRAPH 2024 & Asia 2024 Papers (9):**
- `wiki/papers/tan-2024-soap.md` — Style-omniscient animatable portraits from 2D images
- `wiki/papers/lin-2024-layga.md` — Layered Gaussian avatars for clothing transfer
- `wiki/papers/chen-2024-taming-diffusion.md` — Real-time character control via motion diffusion models
- `wiki/papers/gao-2024-hierarchical-neural-skinning.md` — Self-supervised hierarchical soft-body deformation
- `wiki/papers/benchekroun-2024-stiffgipc.md` — GPU IPC for stiff affine-deformable simulation
- `wiki/papers/ye-2024-kinematic-motion-retargeting.md` — Contact-aware hand manipulation retargeting
- `wiki/papers/liang-2024-drawingspinup.md` — 3D animation from single character drawings
- `wiki/papers/an-2024-refined-inverse-rigging.md` — Quartic-smooth blendshape weight solving
- `wiki/papers/tang-2024-decoupling-contact.md` — Fine-grained contact control in motion style transfer

**SIGGRAPH 2023 & Asia 2023 Papers (4):**
- `wiki/papers/nam-2023-bidirectional-gaitnet.md` — Bidirectional gait-anatomy prediction model
- `wiki/papers/lin-2023-posevocab.md` — Joint-structured pose embeddings for avatar appearance
- `wiki/papers/benchekroun-2023-fast-complementary-dynamics.md` — Reduced-space secondary motion via skinning eigenmodes
- `wiki/papers/ghosh-2023-emote.md` — Emotional speech-driven animation with content-emotion disentanglement

**SIGGRAPH 2022 & Earlier Papers (5):**
- `wiki/papers/xu-2022-morig.md` — Motion-aware rigging from point cloud motion sequences (SIGGRAPH Asia 2022)
- `wiki/papers/peng-2021-amp.md` — Adversarial motion priors for physics-based character control (SIGGRAPH 2021)
- `wiki/papers/wu-2023-aniportraitgan.md` — Animatable 3D portrait generation from 2D images (SIGGRAPH Asia 2023)
- `wiki/papers/aberman-2020-unpaired-motion-style.md` — Unpaired motion style transfer from video (SIGGRAPH 2020)
- `wiki/papers/aberman-2020-skeleton-aware-retargeting.md` — Skeleton-aware networks for deep motion retargeting (SIGGRAPH 2020)

**Topics covered:**
- Automated keyframing and motion synthesis (AutoKeyframe, Taming Diffusion, AnyTop, AMP)
- Neural avatar and head generation (LAM, AnimPortrait3D, 3DGH, SOAP, LayGA, AniPortraitGAN)
- Auto-rigging and skeleton extraction (MoRig, DrawingSpinUp, UniRig, Anymate, Zhang-UniRig)
- Facial animation and blendshapes (Refined Inverse Rigging, EMOTE, Compressed Skinning)
- Motion retargeting and style transfer (Decoupling Contact, Skeleton-Aware, Unpaired Style Transfer, Kinematic Retargeting)
- Physics-based simulation (StiffGIPC, Fast Complementary Dynamics, JGS2, Hierarchical Neural Skinning)
- Specialized animation (Bidirectional GaitNet, PoseVocab)

**Meta-statistics:**
- 4 papers already ingested from research batch (Zhang UniRig, Gat AnyTop, Deng Anymate, Kavan Compressed Skinning)
- 23 new papers added this session
- Total SIGGRAPH 2020-2025 character rigging papers in wiki: 27
- Venues: SIGGRAPH 2020-2025, SIGGRAPH Asia 2022-2024
- Year range: 2020-2025
- Total wiki papers now: 181 (154 → 181)

## [2026-04-13] python | Analytically Learning an Inverse Rig Mapping

Implemented full Python and VEX code for Gustafson, Lo, Kanyuk SIGGRAPH Talks 2020.

**Files created:**
- `wiki/python/inverse_rig_mapping.py` — complete Python implementation (~450 lines)
- `wiki/vex/inverse-rig-mapping.vex` — 3-snippet Houdini VEX implementation

**Python module (`inverse_rig_mapping.py`):**
- `RotationOp` — single-joint rotation operator with analytic matrix() and dmatrix_dparam()
- `TranslationOp` — single-joint translation operator
- `ForearmTwistOp` — multi-joint twist operator; distributes one parameter across N joints via cumulative fractions (extension for partial-twist rigs not covered by paper's general framework)
- `LearnedRigApproximation.train()` — classifies each parameter to an Op type, sorts composition order via pairwise test (paper eq. 6), returns learned approximation
- `LearnedRigApproximation.evaluate()` / `.jacobian()` — forward pass and analytic (3·n_joints × n_params) Jacobian using SO(3) log-map chain rule
- `RigInverter.invert()` — Gauss-Newton (30 iter) + Levenberg-Marquardt fallback
- `ArmRig` — concrete 5-param example: shoulder_rx/ry/rz (ZYX Euler), elbow_bend, forearm_twist → 5 joints (shoulder, elbow, forearm_1/2/3)
- `demo_arm_rig()` — trains approximation, inverts random poses, prints parameter and residual errors

**VEX file (`inverse-rig-mapping.vex`):**
- Snippet A — Python SOP pseudocode: writes Jacobian columns as detail float[] attributes
- Snippet B — KineFX Geometry Wrangle: Gauss-Newton solver reading stored Jacobian; outputs `beta_solved` + named rig channels
- Snippet C — Standalone arm + forearm twist example: hardcoded 5-param × 5-joint Jacobian, inline Gauss-Newton, no offline training required

**Key algorithmic decisions:**
- SO(3) log-map Jacobian: J_r^-1 = I + 0.5·[rv]× + a·[rv]×² (falls back to vee() at θ < 1e-8)
- ForearmTwistOp detects multi-joint parameters with parallel rotation axes and monotonically increasing rates during classification step
- Sorting via insertion sort with pairwise precedes test (eq. 6 from paper)
- VEX uses Gauss-Seidel to avoid matrix inversion (VEX has no native linear solver for float arrays)

**Updated indexes:**
- `wiki/python/index.md` — added inverse_rig_mapping.py section with quick-start, class table, formulas
- `wiki/vex/index.md` — added inverse-rig-mapping.vex section; health summary: 50 → 53 snippets

## [2026-04-13] technique | Inverse Rig Mapping

Created `wiki/techniques/inverse-rig-mapping.md` covering the full Gustafson et al. 2020 technique:
- Problem framing (rig inversion bottleneck, Jacobian cost)
- Three stages: classification, sorting, Gauss-Newton inversion
- Operator taxonomy: RotationOp, TranslationOp, ForearmTwistOp
- Arm + forearm twist concrete example with annotated 15×5 Jacobian
- Python usage (ArmRig, LearnedRigApproximation, RigInverter)
- Houdini VEX usage (Snippets A/B/C from inverse-rig-mapping.vex)
- Gotchas: nonlinear params, same-joint ordering, discarded params, VEX solver limits
- Performance notes (~2ms, 5000× speedup)
- Comparison table vs. numerical Jacobian, FaceBaker, Dem Bones, ML Deformer

Updated `wiki/index.md` — added technique row.

## [2026-04-14] update | Inverse Rig Mapping — extend ArmRig to shoulder+elbow+hand

Extended the concrete rig example from a 5-param forearm-twist rig to a 7-param arm+hand rig:

**Changes:**
- `ArmRig`: num_params 5→7, num_joints 5→3; removed forearm_1/2/3 joints; added hand joint (3-DOF ZYX Euler); forward kinematics now evaluates shoulder, elbow, hand independently
- `ArmRig.ground_truth_jacobian`: updated from (15×5) to (9×7); hand block (rows 6:9, params 4:7) mirrors shoulder ZYX Euler structure
- `demo_arm_rig()`: test cases updated to 7-element beta vectors; 7 new test cases covering shoulder-only, elbow-only, hand-only, mixed combinations
- Module docstring updated to reflect new param/joint layout
- `wiki/vex/inverse-rig-mapping.vex` Snippet C: rewritten from 15×5 to 9×7 Jacobian; `forearm_twist` channels replaced with `hand_rx/ry/rz`; Gauss-Seidel loop updated for 7 params
- `wiki/vex/index.md`: Snippet C table row, joint layout table, Jacobian code block, attribute table updated
- `wiki/python/index.md`: quick-start example, ArmRig description, joint layout diagram updated
- `wiki/techniques/inverse-rig-mapping.md`: arm example section rewritten; new 9×7 Jacobian table; Python and VEX usage code blocks updated

## [2026-04-13] update | Inverse Rig Mapping — add forearm partial twist procedural joints via CompoundOp

Extended `ArmRig` from 3 joints (shoulder, elbow, hand) to 6 joints (shoulder, elbow, forearm_1, forearm_2, forearm_3, hand). Forearm joints are procedural: they receive `hand_rx / 3` each as a candy-wrapper twist distribution.

**Key architectural addition — `CompoundOp`:**
- One parameter (`hand_rx`) simultaneously drives a `ForearmTwistOp(joints=[2,3,4], fracs=[1/3,2/3,1.0], axis=X, rate=1.0)` and a `RotationOp(joint=5, axis=X, rate=1.0)`
- Classification auto-detects this via rate-grouping: joints with equal rate (1/3) → ForearmTwistOp; joint with different rate (1.0) → RotationOp; multiple groups → CompoundOp wrapper
- Jacobian for `hand_rx` column has entries 1/3 at forearm rx rows and 1.0 at hand rx row; `JᵀJ[4,4] = 4/3` (non-unit)

**Changes:**
- `wiki/python/inverse_rig_mapping.py`: added `CompoundOp` class (with `_apply()`, `jacobian_contributions()`); updated `evaluate()`, `jacobian()`, `_classify_parameter()` for CompoundOp; rewrote `ArmRig` (num_joints 3→6, new FK, new ground-truth Jacobian (18×7)); updated `demo_arm_rig()` with 8 test cases
- `wiki/vex/inverse-rig-mapping.vex` Snippet C: rewritten from 9×7 to 18×7 Jacobian; 6-joint layout; hand_rx column with 1/3 at forearm rows + 1.0 at hand row; Gauss-Seidel on 18 DOFs / 7×7 JᵀJ
- `wiki/vex/index.md`: Snippet C table row updated to "6 joints × 7 params (18×7)"; joint layout table extended to 6 rows; Jacobian code block updated with 1/3 entries; CompoundOp note added
- `wiki/python/index.md`: quick-start comments updated for 6-joint layout; ArmRig entry updated; joint layout diagram updated to 18-vector with CompoundOp notation
- `wiki/techniques/inverse-rig-mapping.md`: arm example section renamed and rewritten; 18×7 Jacobian table; CompoundOp classification explanation; Python and VEX code blocks updated


## [2026-04-14] ingest | Marquis Bolduc & Phan 2022 — Rig Inversion by Training a Differentiable Rig Function

Ingested three raw PDFs added to `raw/papers/`, all in the rig-inversion family:

**New pages created:**
- `wiki/papers/marquis-bolduc-2022-differentiable-rig.md` — SIGGRAPH Asia 2022 Technical Communications; key contribution: train differentiable MLP rig approximation L̂_d, then use it to train inverse rig model with mesh loss instead of parameter loss; handles non-injective/non-surjective rigs; 3–4× lower error than Holden 2015 on EA facial rig (137 params, 8447 vertices)
- `wiki/papers/holden-2017-inverse-rig-tvcg.md` — IEEE TVCG 2017 extended journal version of Holden SCA 2015; adds Gaussian Process Regression (with farthest-point active subsampling) as alternative to MLP; super-sampling augmentation; method selection guide (GPR vs MLP)
- `wiki/authors/marquis-bolduc-mathieu.md` — new author page (SEED, EA)

**Updated pages:**
- `wiki/papers/holden-2015-inverse-rig.md` — source PDF added (`2786784.2786788.pdf`); summary and connections expanded; added link to TVCG 2017 journal version and Marquis Bolduc 2022
- `wiki/papers/gustafson-2020-inverse-rig.md` — added connections to Holden 2015/2017 and Marquis Bolduc 2022
- `wiki/concepts/rig-inversion.md` — taxonomy expanded with differentiable rig approximation variant; Key Papers section now lists all four rig-inversion papers
- `wiki/authors/holden-daniel.md` — added TVCG 2017 paper
- `wiki/index.md` — two new paper rows, one new author row

## [2026-04-14] lint | Wiki lint pass

**Broken links fixed (4):**
- `papers/lin-2023-posevocab.md`: typo `ranja-2018-coma` → `ranjan-2018-coma`
- `concepts/rig-inversion.md`: added `[[techniques/inverse-rig-mapping]]` link (technique page was orphaned)

**Missing pages created (3):**
- `concepts/motion-synthesis.md` — covers physics-based (AMP), data-driven, neural generative, retargeting, crowd synthesis; links 9 orphan papers
- `concepts/simulation.md` — covers FEM, projective dynamics, rig-space physics, ML surrogates, cloth, facial sim; links 12 orphan papers
- `authors/komura-taku.md` — missing author referenced from `holden-2017-inverse-rig-tvcg.md`

**Index updated:** `concepts/simulation`, `concepts/motion-synthesis`, `authors/komura-taku` rows added

**Remaining known issues (not fixed — low priority or need user action):**
- 18 papers lack local PDFs (classical foundational works: delta-mush, BBW, ARAP, green-coords, etc.)
- `papers/aberman-2020-unpaired-motion-style.md` references `[[papers/aberman-2017-style-transfer]]` — paper not yet ingested
- 31 orphan pages remain; most are covered by the new concept pages but not all are explicitly linked from within the knowledge graph (they appear in index.md)
- `log.md` historical entries mention `nguyen-2023-next3d` (renamed to `sun-2023-next3d`) — left as-is since log is append-only

## [2026-04-14] ingest | Inverse Rig Mapping — research pass (Rackovic 2023–2024 series)

**Research:** surveyed the full inverse rig mapping literature beyond the existing wiki entries.

**New papers ingested (3):**
- `papers/rackovic-2023-distributed-rig-inversion.md` — SIGGRAPH Asia 2023 Technical Communications; ADMM distributed blendshape inversion with spatial clustering and overlapping shared weights. Source: `raw/papers/3610543.3626166.pdf`
- `papers/rackovic-2023-highfidelity-inverse-rig.md` — arXiv 2023 (2302.04820); quartic blendshape model + coordinate descent; >20% sparsity gain vs SOTA
- `papers/rackovic-2023-accurate-interpretable-inverse-rig.md` — arXiv 2023 (2302.04843); SQP/MM solvers for quadratic correctives; up to 45% RMSE improvement

**Existing paper updated (1):**
- `papers/an-2024-refined-inverse-rigging.md` — corrected authors (was wrong: An/Park/Nam → correct: Rackovic/Soares/Jakovetic); expanded method (Quartic Smooth, L1+roughness joint optimization, temporal decoupling, MetaHuman evaluation table). Source updated to `raw/papers/3680528.3687670.pdf`

**New author page (1):**
- `authors/rackovic-stevo.md`

**Concept pages updated (1):**
- `concepts/rig-inversion.md` — expanded Variants taxonomy to include full blendshape inversion sub-taxonomy (per-frame LS, quartic coordinate descent, quadratic SQP/MM, ADMM distributed, Quartic Smooth temporal)

**Lint fixes — missing concept pages created (2):**
- `concepts/correctives.md` — comprehensive corrective shape taxonomy (by trigger type and model order), authoring methods, inversion challenge
- `concepts/skinning.md` — umbrella overview linking LBS, DQS, CoR, implicit, neural skinning and cage-based deformation

**Implementation reference noted:**
- GitHub: lukaskapp/InverseRigMapping — PyTorch/Maya toolset for mocap retargeting to arbitrary rigs via neural inverse rig (based on Holden 2015)

**Index updated:** 3 new paper rows, 2 new concept rows (correctives, skinning, updated rig-inversion), 1 new author row

## [2026-04-14] ingest | Learnable B-Spline Volumes — research pass

**Research:** surveyed the full B-spline/Bernstein trivariate volume literature from foundational FFD through learnable/differentiable variants and production applications.

**New concept page (1):**
- `concepts/b-spline-volumes.md` — comprehensive coverage of FFD, B-spline solid muscles, differentiable/learnable FFD (DeformNet, Jack 2018), spline deformation fields; includes PyTorch differentiable FFD implementation and PyGeM usage

**New papers ingested — B-spline volumes / FFD (5):**
- `papers/sederberg-1986-ffd.md` — foundational FFD (SIGGRAPH 1986); trivariate Bernstein lattice
- `papers/ng-thow-hing-1997-bspline-solid.md` — B-spline solid as muscle primitive; fibre orientation; spring-mass dynamics (CAS 1997)
- `papers/kurenkov-2017-deformnet.md` — differentiable FFD layer; CNN predicts control point displacements (WACV 2018)
- `papers/jack-2018-learning-ffd.md` — learning FFD for 3D reconstruction; SOTA on ShapeNet (ACCV 2018)
- `papers/song-2025-spline-deformation-field.md` — spline trajectories for dense point motion; analytic velocity/acceleration; SIGGRAPH 2025

**New papers ingested — new raw papers (5):**
- `papers/lykkegaard-2025-ooooo-rig.md` — Pixar's first mesh-free character rig; SDF hierarchy (BlObjects + BlOperators); SIGGRAPH Talks 2025. Source: `raw/papers/2025.ooooo_rig.pdf`
- `papers/mohammadi-2026-canrig.md` — CANRIG: cross-attention neural face rigging; variable local control regions; shape-preserving additive layers; DisneyResearch|Studios; Eurographics 2026. Source: `raw/papers/CANRIG-Cross-Attention-Neural-Face-Rigging-with-Variable-Local-Control-Paper.pdf`
- `papers/ma-2025-riganyface.md` — RigAnyFace: topology-agnostic neural facial auto-rigging; FACS blendshapes; 2D supervision for unlabeled data; NeurIPS 2025. Source: `raw/papers/2511.18601v1.pdf`
- `papers/cha-2025-neural-face-skinning.md` — Neural Face Skinning: mesh-agnostic expression cloning via learned skinning weights; global+local; arXiv 2025. Source: `raw/papers/2505.22416.pdf`
- `papers/hoffman-2024-insideout2-rig.md` — Inside Out 2 rig challenges: four-corner lids, eye auto-gaze correction; SIGGRAPH Talks 2024. Source: `raw/papers/2024.SiggraphTalks.HNSZ.pdf`

**Index updated:** 11 new paper rows, 1 new concept row (b-spline-volumes)

**External resources noted:**
- PyGeM: https://github.com/mathLab/PyGeM — Python FFD library (B-spline + RBF + IDW)
- FFD.jl: https://github.com/OptimalDesignLab/FFD.jl — Julia B-spline FFD
- DeformNet project: https://deformnet-site.github.io/DeformNet-website/

## [2026-04-17] sweep | Raw assets consolidation (7 md files in raw/assets/)

Reviewed all 7 markdown files in `raw/assets/`. All were ingested in prior sessions. Applied 3 targeted gap-fills:

**`papers/marquis-bolduc-2022-differentiable-rig.md`** — added External References section:
- EA SEED YouTube talk https://www.youtube.com/watch?v=sYCz9LGIkuI (source: `raw/assets/Using a Differentiable Function for Rig Inversion.md`)
- Author-hosted paper PDF https://www.ea.com/seed/news/seed-rig-inversion-differentiable-rig-function

**`papers/holden-2015-inverse-rig.md`** — expanded External Implementation to External References:
- Daniel Holden's blog https://theorangeduck.com/page/learning-inverse-rig-mapping-character-animation (source: `raw/assets/Learning an Inverse Rig Mapping for Character Animation.md`)
- Author-hosted PDF http://theorangeduck.com/media/uploads/rigmapping.pdf
- SCA 2015 video https://www.youtube.com/watch?v=P4-0esMIvuo

**`papers/mirrored-anims-2025-rig-retargeting.md`** — added `doi: 10.1145/3769047.3769064` to frontmatter (from ACM DL source `raw/assets/MIRRORED-Anims_...md`)

Files already fully ingested in prior sessions:
- `raw/assets/Refined Inverse Rigging...md` → `papers/an-2024-refined-inverse-rigging.md` (2026-04-14)
- `raw/assets/MIRRORED-Anims_...md` → `papers/mirrored-anims-2025-rig-retargeting.md` (2026-04-16)
- `raw/assets/XrFaceExpression2FB.md` → `concepts/openxr-face-tracking.md` (2026-04-16)
- `raw/assets/Generative modelling in latent space.md` → `concepts/latent-generative-modelling.md` (2026-04-16)
- `raw/assets/Inverse Rig Mapping - Technical Directing...md` → noted in `papers/holden-2015-inverse-rig.md` (2026-04-16)

## [2026-04-22] ingest | Face Anything: 4D Face Reconstruction from Any Image Sequence

Source: `raw/papers/2604.19702v1.pdf` — Kocasarı, Giebenhain, Shaw, Nießner (arXiv 2026).

- Created `wiki/papers/kocasari-2026-face-anything.md`
- Created `wiki/authors/giebenhain-simon.md`
- Updated `wiki/authors/niessner-matthias.md`
- Updated `wiki/index.md`

## [2026-04-22] ingest | FLAME face model — concept page + Python

Researched FLAME (Li et al. 2017) from `raw/papers/flame_paper.pdf`.

- Created `wiki/concepts/flame-model.md` — full parameterization, training pipeline, fitting pipeline, downstream ecosystem table (10+ papers), implementation gotchas
- Created `wiki/python/flame-forward-pass.py` — `rodrigues`, `lbs`, `flame_forward` numpy reference implementation
- Created `wiki/authors/romero-javier.md`
- Updated `wiki/authors/black-michael.md` — added CoMA, DECA, EMOCA, MICA, SMIRK, HeadCraft
- Updated `wiki/index.md` — added flame-model concept row, python snippet row

## [2026-04-22] assets | Face the FACS — reference images downloaded

Downloaded all FACS Study Guide images and GIFs from melindaozel.com (premium session).

- 86 files, 145 MB into `raw/assets/melindaozel/` with 8 section subfolders
- Descriptive AU-named filenames: `AU1-inner-brow-raiser.gif`, `AU23-lip-tightener-vertical-1.gif`, etc.
- Covers AU1–AU28, fAUx8, and #notFACS entries; GIFs for every AU that has one
- `raw/assets/melindaozel/README.md` — full annotated index

## [2026-04-22] query | Face the FACS site research report

Logged in to melindaozel.com/facs-study-guide/ (premium account).

- Created `wiki/queries/face-the-facs-site-report.md`
  - Full AU inventory (AU1–AU28 + notFACS + fAUx entries) with muscle names and section organization
  - Premium resource catalog (18+ posts across FACS, face tracking, lipsync)
  - Melinda Ozel AU taxonomy deviations from classic FACS: AU4 3-muscle split, fAUx8 howler mouth, AU14 y/z-axis dimpler, AU23 2-type lip tightener
  - Cross-links to wiki papers and concepts
- Updated `wiki/index.md`
