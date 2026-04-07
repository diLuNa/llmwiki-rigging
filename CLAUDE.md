# Rigging Wiki — Schema & Agent Instructions

You are the maintainer of a personal research wiki focused on **character rigging papers** — academic work on skinning, deformation, simulation, corrective shapes, rig generation, and related topics from SIGGRAPH, SCA, CGI, and other venues.

The wiki lives in `wiki/`. Raw source documents live in `raw/`. You write and maintain all wiki files. The human curates sources and asks questions.

---

## Directory Layout

```
rigging-wiki/
├── CLAUDE.md          ← this file
├── raw/               ← immutable source documents (papers, notes, images)
│   └── assets/        ← downloaded images/figures
│   └── papers/        ← downloaded papers
├── wiki/
│   ├── index.md       ← master catalog (always update on ingest)
│   ├── log.md         ← append-only chronological log
│   ├── overview.md    ← high-level synthesis of the field
│   ├── papers/        ← one page per paper
│   ├── concepts/      ← one page per concept/algorithm/technique class
│   ├── techniques/    ← implementation-focused pages (VEX, Python, Houdini)
│   ├── authors/       ← one page per notable author
│   ├── comparisons/   ← side-by-side analysis pages
│   ├── queries/       ← saved answers to important questions
│   └── vex/           ← vex code snippets extracted from papers
└── tools/             ← helper scripts (search, lint, etc.)
```

---

## Page Formats

### Paper page (`wiki/papers/<slug>.md`)
```markdown
---
title: "Full Paper Title"
authors: [Last, First; Last, First]
venue: SIGGRAPH 2020
year: 2020
tags: [skinning, correctives, neural, simulation]
source: raw/papers/filename.pdf
---

## Summary
2–4 sentence plain-language summary of what the paper does and why it matters.

## Problem
What gap or limitation does this paper address?

## Method
Core technical approach. Keep it dense and precise. Use math notation where helpful.

## Key Results
What did they demonstrate? Metrics, comparisons, qualitative claims.

## Limitations
What does the paper itself admit? What do you observe?

## Connections
- [[concepts/concept-name]] — how this paper relates
- [[papers/other-paper]] — comparison or dependency
- [[authors/author-name]]

## Implementation Notes
Anything relevant to implementing this in Houdini/VEX/Python. Gotchas. Tricks.

## Quotes
Notable quotes (with page numbers if available).
```

### Concept page (`wiki/concepts/<slug>.md`)
```markdown
---
title: "Concept Name"
tags: [skinning, math, deformation]
---

## Definition
Clear, precise definition.

## Variants / Taxonomy
If this concept has subtypes or related formulations.

## Key Papers
- [[papers/slug]] — one-line note on contribution

## Connections
Links to related concepts.

## Notes
Anything else worth knowing — implementation tips, history, gotchas.
```

### Author page (`wiki/authors/<slug>.md`)
```markdown
---
name: "First Last"
affiliation: Institution (as of last known)
---

## Papers in Wiki
- [[papers/slug]] (Venue Year)

## Research Themes
What are their recurring interests?

## Notes
```

### Comparison page (`wiki/comparisons/<slug>.md`)
Free-form, but always include a markdown table summarizing the comparison along some axis (method, complexity, quality, runtime, etc.).

### Query page (`wiki/queries/<slug>.md`)
Saved answer to a question worth keeping. Format:
```markdown
---
question: "The question that prompted this"
date: YYYY-MM-DD
---
[Answer with citations to wiki pages]
```

---

## Operations

### Ingest a paper
When told to ingest a source:
1. Read the source (ask human to paste or describe if you can't access the file).
2. Discuss key takeaways briefly with the human.
3. Write `wiki/papers/<slug>.md`.
4. Create or update any `wiki/concepts/` pages referenced.
5. Create or update `wiki/authors/` pages for key authors.
6. Update `wiki/overview.md` if the paper shifts the synthesis.
7. Update `wiki/index.md` — add all new/updated pages.
8. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Paper Title`.
9. Report what was touched.

### Expand a paper
When told to expand a source:
1. Read the source (ask human to paste or describe if you can't access the file).
2. Extract the most relevant referenced papers
3. Download the most relevant reference papers
4. Ingest the most relevant downloaded papers
5. Discuss key takeaways briefly with the human.
6. Write `wiki/papers/<slug>.md`.
7. Create or update any `wiki/concepts/` pages referenced.
8. Create or update `wiki/authors/` pages for key authors.
9. Update `wiki/overview.md` if the paper shifts the synthesis.
10. Update `wiki/index.md` — add all new/updated pages.
11. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Paper Title`.
12. Report what was touched.

### Extract core concepts
When told to extract core concepts from a source:
1. Read the source (ask human to paste or describe if you can't access the file).
2. Extract the core concepts described in the paper
3. Create or update any `wiki/concepts/` pages referenced.
4. Update `wiki/overview.md` if the paper shifts the synthesis.
5. Update `wiki/index.md` — add all new/updated pages.
6. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Paper Title`.
7. Report what was touched.

### Answer a query
1. Read `wiki/index.md` to find relevant pages.
2. Read those pages.
3. Synthesize an answer with `[[wiki links]]` as citations.
4. Ask the human if this answer is worth saving to `wiki/queries/`.

### Lint
When asked to lint:
- Check for orphan pages (no inbound links).
- Check for concepts mentioned but lacking their own page.
- Check for contradictions between paper pages.
- Suggest missing papers worth finding.
- Report a health summary.

### Vex
When asked to vex:
- Convert every algorithm found in a paper into Houdini Vex snippets where possible
- Save every Vex snippet created in the vex subfolder.
- Index every Vex snippet in a referencing page with a brief description of the usage and functions written.
- when possible create an example of usage of the Vex functions created.
- provide Python alternative if Vex is not available/possible
- Append to `wiki/log.md`: `## [YYYY-MM-DD] vex | Paper Title`.
- Report a health summary.

---

## Conventions

- **Slugs**: lowercase, hyphen-separated. Paper slugs: `lastname-year-keyword` (e.g. `lbs-1988-skinning`, `degoes-2020-sculpt`).
- **Tags**: use from this list (extend as needed): `skinning`, `lbs`, `dqs`, `correctives`, `blendshapes`, `simulation`, `neural`, `rig-generation`, `pose-space`, `muscles`, `fascia`, `volumes`, `usd`, `houdini`, `vex`, `python`, `math`.
- **Wiki links**: always use `[[relative/path]]` syntax (Obsidian-compatible).
- **Math**: use LaTeX fences ` ```math ` for display math, `$...$` for inline.
- **Figures**: reference as `![[raw/assets/filename.png]]`.
- **Always update index.md and log.md** on any ingest or major edit.

---

## Field Scope

Core topics this wiki covers:
- **Skinning**: LBS, DQS, CoR, implicit skinning, neural skinning
- **Neural blend shapes**: learned pose-dependent corrective blendshapes, data-driven PSD, neural residuals over LBS (e.g. Li et al. 2021)
- **Nonlinear 3D morphable face models**: beyond linear 3DMM — mesh-convolutional autoencoders (CoMA), implicit neural representations (ImFace), nonlinear shape VAEs, neural morphable models
- **Performance-driven facial animation**: real-time blendshape weight solving from video/mocap, marker fitting, expression transfer, NLLS-based optimization (e.g. FACEIT, JTDP03)
- **Diffusion-based facial appearance editing**: rig-conditioned diffusion for face image synthesis and personalized appearance editing (e.g. DiffusionRig)
- **Corrective shapes / Blendshapes**: pose-space deformation, sculpt processing, FACS, blendshape retargeting, surveys (EG 2014 STAR)
- **Simulation-based deformation**: FEM, MPM, muscles, fascia, secondary motion
- **Mesh-based simulation with graph networks**: GNN/MeshGraphNets for cloth, soft tissue, and rigid body simulation on arbitrary meshes; learned physics simulators that run on production mesh topologies
- **Rig generation / automation**: auto-rigging, rig-from-scan, deep learning rigs
- **USD / Houdini pipeline**: UsdSkel, blendshape schemas, HDA patterns
- **Geometric tools**: Laplacian smoothing, bi-Laplacian, harmonic weights, bounded biharmonic
- **Digital human appearance**: skin reflectance capture (BSSRDF, albedo, specular, subsurface), generative face textures (GAN/diffusion), multi-modal texture maps, neural face geometry (VAE/PCA)
- **Hand animation**: dexterous hand grasping, MANO model, RL-based motion synthesis, diffusion grasp generation
- **Speech-driven animation**: audio-driven facial animation, tongue/jaw/lip motion, viseme blendshapes
- **Crowd and procedural animation**: motion cycle blending, crowd simulation, behavioral controls (note-level coverage — 1-page sketches included)
- **Wrinkle systems**: art-directed pose-space wrinkles, tension-driven expression wrinkles, image-based static wrinkle generation

Adjacent topics to note but not deep-dive unless a local PDF exists:
- General physics simulation (fluids, cloth beyond character rigging)
- Full body performance capture and reconstruction
- Rendering and shading beyond skin appearance

---


