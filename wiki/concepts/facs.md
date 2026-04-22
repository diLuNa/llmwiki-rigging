---
title: "FACS — Facial Action Coding System"
tags: [blendshapes, facial-capture, rig-generation, digital-human, muscles]
---

## Definition

The **Facial Action Coding System (FACS)**, developed by Paul Ekman and Wallace Friesen (1978), is an anatomically-grounded taxonomy that decomposes any visible facial movement into a set of **Action Units (AUs)** — the minimal, visually distinguishable movements produced by one or more facial muscles.

The original manual describes **44 AUs** (muscles or muscle groups), 12 head/eye movement descriptors, and an **intensity scale A–E** (A=trace → E=maximum). A given facial expression is encoded as a set of activated AUs with their intensities, e.g., a genuine smile = AU6+AU12.

FACS is the lingua franca of CG facial rigging: production rigs from PDI/DreamWorks, Pixar, ILM, Weta, and Epic MetaHuman all ground their blendshape palettes in FACS AUs, even when muscle-based or neural methods are used to drive them.

**Canonical reference:** [[papers/ekman-friesen-1978-facs]]  
**2002 revised manual:** Paul Ekman Group LLC — [paulekman.com/facial-action-coding-system](https://www.paulekman.com/facial-action-coding-system/)

---

## Action Unit Reference

### Upper Face

| AU | FACS Name | Muscle(s) | CG Notes |
|----|-----------|-----------|----------|
| AU1 | Inner Brow Raise | Frontalis (pars medialis) | Bilateral or L/R; key for sadness/fear |
| AU2 | Outer Brow Raise | Frontalis (pars lateralis) | Almost always paired with AU1 or alone for surprise |
| AU4 | Brow Lowerer | Corrugator supercilii, Depressor supercilii | Anger/concentration; antagonist to AU1+AU2 |
| AU5 | Upper Lid Raiser | Levator palpebrae superioris | Widens eye aperture; surprise/fear |
| AU6 | Cheek Raiser | Orbicularis oculi (orbital) | "Duchenne marker" — genuine smile; raises cheek & narrows eye |
| AU7 | Lid Tightener | Orbicularis oculi (orbital) | Squinting/anger; compresses lower lid |
| AU41 | Lid Droop | Relaxation of levator palpebrae | Fatigue/sadness |
| AU42 | Slit | Orbicularis oculi | Narrowing of eye |
| AU43 | Eyes Closed | Orbicularis oculi (orbital) | Soft close (sleep) |
| AU44 | Squint | Orbicularis oculi | Hard squint |
| AU45 | Blink | Orbicularis oculi | Full blink cycle |
| AU46 | Wink | Unilateral orbicularis oculi | Left or right only |

### Lower Face / Jaw

| AU | FACS Name | Muscle(s) | CG Notes |
|----|-----------|-----------|----------|
| AU9 | Nose Wrinkler | Levator labii superioris alaeque nasi | Disgust; bunny lines |
| AU10 | Upper Lip Raiser | Levator labii superioris | Sneer-like; contempt/disgust |
| AU11 | Nasolabial Deepener | Zygomaticus minor | Deepens nasolabial fold |
| AU12 | Lip Corner Puller | Zygomaticus major | Smile; key activation; bilateral or L/R |
| AU13 | Cheek Puffer / Dimpler | Levator anguli oris (buccinator) | Dimple formation |
| AU14 | Dimpler | Buccinator | Pulls lip corners back; dimples |
| AU15 | Lip Corner Depressor | Depressor anguli oris | Sadness/frown |
| AU16 | Lower Lip Depressor | Depressor labii inferioris | Opens lower lip; disgust |
| AU17 | Chin Raiser | Mentalis | Pouts chin skin upward; pout/sadness |
| AU18 | Lip Puckerer | Incisivii labii | Pout/kiss |
| AU20 | Lip Stretcher | Risorius (platysma) | Fear grimace |
| AU22 | Lip Funneler | Orbicularis oris | Funnel/whistle shape |
| AU23 | Lip Tightener | Orbicularis oris | Pressed-lip anger |
| AU24 | Lip Pressor | Orbicularis oris | Lip compression |
| AU25 | Lips Part | Depressor labii / Mentalis relaxation | Mouth opening phase 1; teeth hidden |
| AU26 | Jaw Drop | Masseter relaxation | Moderate open mouth |
| AU27 | Mouth Stretch | Pterygoids, digastric | Wide-open mouth; extreme surprise |
| AU28 | Lip Suck | Orbicularis oris | Inward lip pull |

### Head & Gaze Descriptors

| Code | Name | Notes |
|------|------|-------|
| AU51/52 | Head Turn Left/Right | Cervical rotation |
| AU53/54 | Head Up/Down | Cervical flexion/extension |
| AU55/56 | Head Tilt Left/Right | Cervical lateral bend |
| AU57/58 | Head Forward/Back | Cervical protrusion/retraction |
| AU61/62 | Eyes Turn Left/Right | Gaze direction |
| AU63/64 | Eyes Up/Down | Vertical gaze |
| AU65 | Walleye / Diverge | Eyes diverge outward |

### Intensity Scale

| Code | Intensity | Rough visual guide |
|------|-----------|--------------------|
| A | Trace | Barely detectable |
| B | Slight | Clearly present, mild |
| C | Marked / Pronounced | Unambiguous, moderate amplitude |
| D | Extreme | Near maximum range |
| E | Maximum | Full anatomic range |

---

## FACS and the 7 Universal Expressions

Ekman's original claim (partially revised in later work): these AU combinations are cross-culturally universal.

| Expression | FACS Prototype | Notes |
|-----------|---------------|-------|
| Happiness | AU6 + AU12 | AU6 (cheek raiser) is the Duchenne marker — distinguishes genuine from posed smiles |
| Sadness | AU1 + AU4 + AU15 | Sometimes AU17 (chin raiser) |
| Surprise | AU1 + AU2 + AU5B + AU26/27 | Note: surprise is not always negative |
| Fear | AU1 + AU2 + AU4 + AU5 + AU20 + AU26 | Large multi-AU combination |
| Anger | AU4 + AU5 + AU7 + AU23 + AU24 | Sometimes AU17, AU25 |
| Disgust | AU9 + AU15 | Sometimes AU16, AU25 |
| Contempt | AU12R + AU14R | **Unilateral** — only R or L side; uniquely asymmetric |

---

## FACS in CG Facial Rigs

### Blendshape Naming Conventions

Production rigs vary in how closely they follow FACS numbering:

**ARKit (Apple, 52 blend shapes):**  
Uses descriptive names (e.g., `browInnerUp`, `cheekSquintLeft`, `jawOpen`). Closely maps to FACS AUs but does not use AU numbers. Bilateral AUs get `Left`/`Right` suffixes. ARKit → FACS mapping: [melindaozel.com/arkit-to-facs-cheat-sheet](https://melindaozel.com/arkit-to-facs-cheat-sheet/)

**Maya (production conventions):**  
Facial rigs typically use AU numbers or muscle/region names (e.g., `AU12_L`, `AU6_R`, or `lipCornerPullerL`). No strict industry standard; studios define their own palettes.

**ICT FaceKit (53 expressions):**  
Used as supervision signal in neural rigging papers ([[papers/qin-2023-nfr]], [[papers/ma-2025-riganyface]]). FACS-inspired but adds production-friendly decompositions (e.g., separate upper/lower eyelid).

**MetaHuman (Epic, 258–669 blendshapes):**  
~200 FACS controls → dense blendshape basis; 1,000+ PSD correctives. See [[papers/epic-2021-metahuman-rig]].

### FACS as Neural Supervision Signal

Recent neural auto-rigging papers use FACS as a *training supervision signal*:

- **NFR** ([[papers/qin-2023-nfr]]): trains on FACS-defined target poses using ICT FaceKit; outputs per-vertex skinning weights for each AU
- **RigAnyFace** ([[papers/ma-2025-riganyface]]): deforms neutral meshes into FACS poses to synthesize blendshapes; scales across topologies
- **CANRIG** ([[papers/canrig-2026-neural-face-rigging]]): cross-attention conditioning on AU labels for local control
- **Neural Face Skinning** ([[papers/cha-2025-neural-face-skinning]]): FACS blendshape supervision via indirect segmentation

### Muscle-Based vs FACS-Based

- **FACS-based rigs**: artist sculpts each AU directly. Fast to author, direct animator control. Interaction effects handled via PSD correctives.
- **Muscle-based rigs**: virtual muscle activation drives skin. More physically correct tissue interaction. FACS AUs can be re-expressed as muscle activation patterns. ([[papers/choi-2022-animatomy]], [[papers/pdi-1998-facial-antz]])
- **Hybrid**: Animatomy uses muscle strain to *drive* blendshape weights that still correspond to FACS AUs.

---

## Implementation Notes

### Bilateral AUs
AUs that can activate independently on left and right sides are coded as `AU_L` and `AU_R`. In CG rigs this means two separate blendshapes. Common bilateral AUs: AU1, AU2, AU4, AU6, AU7, AU12, AU14, AU15.

### Anti-synergies and Physical Constraints
Some AU pairs are anatomically difficult or impossible to combine:
- AU1 + AU4 simultaneously: difficult (opposing muscles). Requires strong voluntary control.
- AU12 + AU15 simultaneously: antagonistic (smile + frown). Rare, gives ambiguous expression.

Production rigs often add clamp/inhibit logic or PSD correctives to handle these.

### Intensity in Production
Most CG rigs use AU weights [0,1] mapping to intensity A–E:
- 0 = no activation
- 0.5 ≈ Intensity C (marked)
- 1.0 ≈ Intensity E (maximum)

Some rigs allow negative weights (overshooting past neutral) for artistic flexibility.

---

## Production Gotchas (Melinda Ozel)

Sourced from [[queries/melindaozel-deep-dives]]. These are practitioner-level distinctions absent from academic FACS documentation.

### AU1 — Inner Brow Raiser
**Common mistake:** adding corrugator supercilii (AU4) to the AU1 shape. Any brow convergence, glabellar bunching, or inner-brow depression in your AU1 shape means it contains AU4. The shape must isolate medial upward pull only.  
**Variation:** AU1 appearance varies dramatically per individual due to frontalis muscle shape (bifurcation depth/position). Medial raise location can shift from the innermost brow tip to center-brow.

### AU4 — Brow Lowerer (Three Independent Sub-Muscles)
Treat as three independently activatable muscles for maximum expressivity:
- **Corrugator supercilii** → brow convergence + vertical glabellar wrinkles
- **Procerus** → medial brow depression + horizontal nasal-root wrinkle
- **Depressor supercilii** → inner-brow pull-down with different vector

These are **not additive LBS equivalents** of each other; each produces a distinct movement pattern.

### AU5 — Upper Lid Raiser
LPS is active whenever the eyes are open — AU5 is coded only for *noticeable increases*. Strong AU1+2 can create a false impression of AU5 (sclera exposure without actual LPS increase) — a known false-positive in automated FACS coding.

### AU9 — Nose Wrinkler
The brow-lowering visible in nose wrinkler is driven by **depressor supercilii/procerus (AU4 components)**, not LLSAN. Full typical nose wrinkler = AU4+6+7+9+10+15+17. **AU38 (nostril dilator) is almost always present but frequently not coded** — include it in disgust/nose-wrinkle shape sets. Some individuals are missing corrugator entirely.

### AU10 vs AU11 — The Upper Lip Overuse Problem
**AU10 (levator labii superioris)** is systematically overused in art/tech as the default upper-lip-elevation shape, due to name bias. There are three upper lip elevators:
1. Levator labii superioris → AU10 (medial, straight-up pull)
2. LLSAN → AU9 (also lifts lip + flares nostril)
3. **Zygomaticus minor → AU11** (lateral pull, changes cheek contour)

Key distinction: AU10 pulls the philtrum straight up; AU11 pulls diagonally/laterally and causes visible cheek-contour change. Zygomaticus minor is highly variable in size and insertion — AU11 shapes may need per-character tuning.

### AU12 — Dimples (Bifid Zygomaticus Major)
Smile dimples are caused by a **bifid variant** of zygomaticus major (two insertion points instead of one). Cannot be reproduced by linear blend of AU12 alone — requires a dedicated corrective tied to the secondary insertion point.

### AU23 — Lip Tightener (Horizontal) + Vertical Lip Tightener
**AU23 is almost universally misrepresented** in online references — most show AU18 (pucker), AU24 (presser), or the vertical "lip cincher" instead.  
True AU23 (horizontal type): taut lip edges, no protrusion, no pressing contact, no vertical narrowing.  
**Vertical lip tightener ("lip cincher")** — Melinda's coined action not in FACS: orbicularis tightens vertically (top lip drawn down, bottom slightly up). Frequently confused with AU23. **Highly valuable lipsync blendshape to include** even though not FACS-official.

### AU23 vs AU24 Disambiguation
- AU23: lips tighten/taut horizontally — no lip contact required
- AU24: lips press together with visible compression force — contact between upper and lower lip
- AU24 is the **primary laughter-suppression shape** (holding back a smile)

### Frontalis / AU1 / AU2 — Individual Variation
Frontalis shape (bifurcation depth, width, position) governs where AU1 ends and AU2 begins. AU1 and AU2 are **moving targets** — their visual appearance is per-subject. Face tracking systems assuming a standard frontalis topology will produce inconsistent AU1/AU2 separation across subjects.

---

## Key Papers

| Paper | Contribution |
|-------|-------------|
| [[papers/ekman-friesen-1978-facs]] | Original FACS manual; defines 44 AUs, intensity A–E, 7 universal expressions |
| [[papers/lewis-2014-blendshape-star]] | Survey of blendshape conventions; connects FACS parameterization to production practice |
| [[papers/epic-2021-metahuman-rig]] | MetaHuman: full production FACS-based rig at scale; DNA format + RigLogic |
| [[papers/choi-2022-animatomy]] | Weta: muscle-based alternative to FACS; maps anatomic strain → rig targets |
| [[papers/qin-2023-nfr]] | NFR: neural auto-rigging with FACS supervision (ICT FaceKit) |
| [[papers/ma-2025-riganyface]] | RigAnyFace: scalable neural rigging using FACS pose deformation |
| [[papers/canrig-2026-neural-face-rigging]] | CANRIG: cross-attention rigging with AU-level local control |
| [[papers/cha-2025-neural-face-skinning]] | Neural Face Skinning: FACS-based segmentation supervision |
| [[papers/pdi-1998-facial-antz]] | First major production FACS + muscle-based facial rig (PDI, 1998) |
| [[papers/modesto-2014-dwa-face-system]] | DreamWorks face system history: FACS adoption in large-scale production |
| [[papers/deng-noh-2007-facial-animation-survey]] | CG survey: FACS in blendshape, muscle, and performance capture pipelines |

---

## Connections

- [[concepts/blendshapes]] — FACS AUs are the standard parameterization for facial blendshape palettes
- [[concepts/facial-blendshape-rigs]] — production taxonomy of FACS-based rigs
- [[concepts/pose-space-deformation]] — correctives applied on top of FACS AU activations
- [[concepts/muscles]] — muscle-based alternative / underlying mechanism for AUs
- [[concepts/rig-inversion]] — solving for AU weights from video/markers (performance capture)
- [[concepts/nonlinear-face-models]] — neural face models that use FACS as a supervision or output space

---

## Real-Time Implementations (CG Standards derived from FACS)

For production pipeline use, see these derived standards:
- **ARKit 52 blend shapes** ([[concepts/arkit-blendshapes]]): Apple's FACS-derived real-time standard; de facto interchange format across engines and XR platforms
- **OpenXR face tracking extensions** ([[concepts/openxr-face-tracking]]): XR headset extensions — Meta (70 weights), HTC (37+52, ARKit-compatible), cross-vendor gaze

## External Resources

| Resource | URL | Notes |
|----------|-----|-------|
| Paul Ekman Group (official) | [paulekman.com/facial-action-coding-system](https://www.paulekman.com/facial-action-coding-system/) | Official FACS 2002 manual access; certification |
| CMU FACS AU Reference | [cs.cmu.edu/~face/facs.htm](https://www.cs.cmu.edu/~face/facs.htm) | Full AU list with automation feasibility notes |
| Py-Feat AU Reference | [py-feat.org/pages/au_reference.html](https://py-feat.org/pages/au_reference.html) | AU table with muscular basis + expression involvement |
| Melinda Ozel Cheat Sheet | [melindaozel.com/facs-cheat-sheet](https://melindaozel.com/facs-cheat-sheet/) | Practitioner-friendly AU guide |
| ARKit → FACS mapping | [melindaozel.com/arkit-to-facs-cheat-sheet](https://melindaozel.com/arkit-to-facs-cheat-sheet/) | Maps Apple's 52 ARKit blend shapes to FACS AUs |
| OpenFACS (open source) | [github.com/phuselab/openFACS](https://github.com/phuselab/openFACS) | Python API + UE4 support for FACS animation |
| FACSvatar (real-time) | [github.com/NumesSanguis/FACSvatar](https://github.com/NumesSanguis/FACSvatar) | OpenFace 2.0 → Unity3D/Blender FACS pipeline |
