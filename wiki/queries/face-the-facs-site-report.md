---
question: "What does the Face the FACS site (melindaozel.com) cover, and how does it map to the wiki's FACS/blendshape scope?"
date: 2026-04-22
sources:
  - https://melindaozel.com/facs-study-guide/
  - https://melindaozel.com/facs-cheat-sheet/eyebrow-combos-cheat-sheet/
  - https://melindaozel.com/lower-face-cheat-sheet/
  - https://melindaozel.com/upper-face-expanded/
  - https://melindaozel.com/emotion-references/
  - https://melindaozel.com/facs-video-references/
access: Premium member login (LucaPrasso)
assets:
  - raw/assets/melindaozel/eyebrow-combos/     (11 GIFs)
  - raw/assets/melindaozel/lower-face/         (19 GIFs)
  - raw/assets/melindaozel/upper-face-expanded/ (29 files: 16 GIFs, 12 PNGs, 1 JPG)
  - raw/assets/melindaozel/emotion-references/  (9 MOV videos; 3 Vimeo embeds noted inline)
  - raw/assets/melindaozel/facs-video-references/ (9 MP4 videos via yt-dlp)
---

# Face the FACS — Site Research Report

**Site:** https://melindaozel.com  
**Author:** Melinda Ozel — Facial Systems Expert, FACS specialist, expression tracking patent holder. Credits include de-aging of Tom Hanks for Robert Zemeckis' *Here*. Cited by Eric Drobile (The Last of Us Part II), Ioana Pirvu (Rockstar Games), Giovanni Nakpil (Adobe), Paul Liaw.

---

## Site Overview

"Face the FACS" is the industry-standard practitioner reference for FACS as applied to animation, face tracking, AI lipsync, and character art. It bridges the original Ekman/Friesen academic FACS system (designed for behavioral scientists) to production workflows used in games, film, and VR. Content includes animated GIFs of real muscle activations, anatomy breakdowns, premium deep-dive articles, and Melinda's own extensions to the FACS taxonomy.

---

## FACS Study Guide — Complete AU Inventory

The study guide (https://melindaozel.com/facs-study-guide/) is organized into 8 sections. Each AU entry includes: still reference images, GIF tab, "further info" tab, and links to deep-dive premium posts.

### Section 1 — Eyebrows & Forehead

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| AU1 | Inner Brow Raiser | frontalis, pars medialis | Deep dives: "Secret Life of Inner Brow Raiser," "Inner Brow Raiser Deep Dive," "Frontalis Variation" |
| AU2 | Outer Brow Raiser | frontalis, pars lateralis | Deep dive: "Frontalis Variation" — anatomical differences affecting face tracking, mocap, EMG |
| AU4 | Brow Lowerer | corrugator supercilii + depressor supercilii + procerus | Melinda treats all 3 muscles as independently activatable; see sub-anatomy below |
| #notFACS | Ears Up & Back | superior auricular + posterior auricular | Included because "relatively frequent" in real expressions; not official FACS |

**AU4 muscle sub-anatomy:**
1. **Corrugator supercilii** — draws brows toward each other ("knitting"); causes vertical glabellar wrinkles
2. **Depressor supercilii** — pulls medial brow down; technically classified as eye muscle; debated as distinct vs. part of orbicularis oculi (Melinda endorses distinct classification)
3. **Procerus** — nasal muscle; pushes down medial brows above nose; causes horizontal wrinkle at nasal root

### Section 2 — Eyes & Cheeks

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| AU5 | Upper Lid Raiser | levator palpebrae superioris | Deep dive: "All About Upper Lid Raiser" |
| AU6 | Cheek Raiser | orbicularis oculi, pars orbitalis | Deep dive: "Cheek Raiser vs. Lid Tightener"; "It's All in the Eyes & Other Lies" (emotion context) |
| AU7 | Lid Tightener | orbicularis oculi, pars palpebralis | Deep dive: "Cheek Raiser vs. Lid Tightener" |
| AU45 | Blink | orbicularis oculi, pars palpebralis | Separate post with video |
| AU46 | Wink | orbicularis oculi (may involve depressor supercilii) | Melinda considers AU46 "clunky, unnecessary addition" for animation use |
| #notFACS | Open-eyed blink | orbicularis oculi: pretarsal section | Included as practical animation reference |

### Section 3 — Nose & Middle Face

Key framing: Melinda emphasizes the **infraorbital triangle** and **nasolabial furrow** as central to understanding lower-face AU interactions.

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| AU9 | Nose Wrinkler | levator labii superioris alaeque nasi (LLSAN) | Brow lowering in AU9 comes from depressor supercilii/procerus, NOT LLSAN directly. Deep dive: "Breaking Down Nose Wrinkler" (with full AU coding: AU4+6+7+10+15+17) |
| AU10 | Upper Lip Raiser | levator labii superioris, caput infraorbitalis | Deep dive: "upper lip raiser in smiles" |
| AU11 | Nasolabial Furrow Deepener | zygomaticus minor | Rare; see "upper lip raiser vs. nasolabial furrow deepener" |
| AU38 | Nostril Dilator | nasalis, pars alaris | |
| AU39 | Nostril Compressor | nasalis, pars transversa + depressor septi nasi | |

### Section 4 — Lip Corner Elevators & Pinchers

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| AU12 | Lip Corner Puller | zygomaticus major | Deep dives: rigging open-lip smiles; zygomaticus major anatomical variation & dimples; face tracking leverage; Duchenne smile critique |
| AU13 | Sharp Lip Puller | levator anguli oris | YouTube video distinguishing AU12 vs. AU13 |
| AU14 | Dimpler | buccinator | **Melinda's taxonomy**: y-axis dimpler (outer lip corners compress vertically) vs. z-axis dimpler (inner lip corners push against teeth/inner cheeks) — deviation from classic FACS |

### Section 5 — Real & Faux Lip Depressors

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| AU15 | Lip Corner Depressor | depressor anguli oris | |
| AU16 | Lower Lip Depressor | depressor labii inferioris | Shape becomes more square and lateral at higher intensity |
| AU17 | Chin Raiser | mentalis | Often present as transition muscle in other actions (e.g., AU28) |
| AU20 | Lip Stretcher | risorius | **Highly variable muscle** — reported absent in 1–94% of subjects across studies; origin variation drives directional pull differences. Deep dive pending. |
| AU21 | Neck Tightener | platysma | Platysma extends into jawline; closely linked to risorius — confusion between AU20/AU21 appearance is common. Melinda notes Apple ARKit mislabels their `mouthStretch` blend shape due to this confusion. |

### Section 6 — Orbicularis Oris I

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| fAUx8 | Howler Mouth | orbicularis oris | **Melinda's own deviation** — redefined from AU8 "lips toward each other." Named after howler monkey. Sphincter-like lip contraction while jaws are open. 3 intensity levels. |
| AU18 | Lip Pucker | incisivus labii inferioris & superioris | |
| AU22 | Lip Funneler | orbicularis oris | |

**fAUx8 vs. AU8 (classic FACS):** Classic AU8 is defined as a precursor to AU24, requiring AU25 present; Melinda finds this "vague." fAUx8 removes the AU25 requirement and allows lips to touch at high intensities.

### Section 7 — Orbicularis Oris II

| AU | Name | Primary Muscle(s) | Notes |
|----|------|-------------------|-------|
| AU23 | Lip Tightener | orbicularis oris, pars marginalis | **Melinda's 2-type taxonomy** (deviation from classic FACS) |
| AU24 | Lip Presser | orbicularis oris | |
| AU25 | Lips Part | varies (relaxation of mentalis/orbicularis, or contraction of depressors) | |
| AU28 | Lips Suck | orbicularis oris | AU17 appears in transition; often unavoidable |
| AU26 | Jaw Drop | masseter (relaxed) + temporalis (relaxed) + internal pterygoid (relaxed) | |
| AU27 | Mouth Stretch | pterygoids + digastric | |

**AU23 — 2-type taxonomy:**
- **Type 1: Horizontal type** — original FACS definition; lips tighten horizontally
- **Type 2: Vertical type** — Melinda's addition; orbicularis oris fiber directionality tightens vertically toward center; top lip may be drawn down, bottom lip slightly up. Many reference sources *incorrectly* show Type 2 + lip pucker combo as lip tightener. Distinguished from AU18 by absence of incisivus medial draw.

---

## Premium Resource Catalog

Full premium article library at https://melindaozel.com/premium-resources/ — organized in 3 topic areas:

### FACS & Facial Anatomy
| Resource | URL |
|----------|-----|
| FACS Study Guide | /facs-study-guide/ |
| Eyebrow Combos | /facs-cheat-sheet/eyebrow-combos-cheat-sheet/ |
| Upper Face: Expanded | /upper-face-expanded/ |
| Lower Face: Expanded | /lower-face-cheat-sheet/ |
| Emotion References | /emotion-references/ |
| FACS Video References | /facs-video-references/ |

### Face Tracking & Lipsync Technology
| Resource | URL |
|----------|-----|
| Posed Expression Captures | /posed-expression-capture-guide/ |
| ARKit to FACS: Full Guide | /arkit-to-facs-translation-guide/ |
| Viseme Cheat Sheet | /viseme-speech-guide/ |

### Mixed Posts (Selection)
| Title | URL |
|-------|-----|
| Upper Lip Raiser vs. Nasolabial Furrow Deepener | /upper-lip-raiser-vs-nasolabial-furrow-deepener/ |
| Stylized Facial Expression Design | /stylized-facial-expression-design/ |
| Forehead Dynamics – Frontalis vs. Occipitalis | /forehead-dynamics-frontalis-vs-occipitalis/ |
| Lip Tightener vs. Lip Presser | /lip-tightener-vs-lip-presser/ |
| Eyebrow Shapes and Character Design | /eyebrow-shapes-and-character-design/ |
| Advanced Blend Shape Tips For Blinks | /advanced-blend-shape-tips-for-blinks/ |
| Hot Tips For Animating Blinks | /hot-tips-for-animating-blinks/ |
| All About Upper Lid Raiser – AU5 | /all-about-upper-lid-raiser-au5/ |
| Zygomaticus Major Variations & the Dimple | /zygomaticus-major-variations-the-dimple/ |
| Frontalis Variation: Why Wrinkle Patterns Differ | /frontalis-variation/ |
| Inner Brow Raiser: Deep Dive | /inner-brow-raiser-deep-dive/ |
| Wrinkle Tips For Character Artists, Part II | /a-wrinkle-in-time-part-ii/ |
| Building Smiles – The Right Way | /building-smiles-the-right-way/ |
| Bypassing VR Headset Occlusion in Face Tracking | /bypassing-vr-headset-occlusion-in-face-tracking/ |
| Breaking Down Nose Wrinkler (AU9) | /breaking-down-nose-wrinkler/ |
| Lip Tightener (AU23) and Why Everyone Gets It Wrong | /lip-tightener/ |
| Leveraging Facial Muscle Variation | /leveraging-facial-muscle-variation/ |
| Colors of Sadness | /colors-of-sadness/ |

---

## Key Deviations from Classic Ekman FACS

Melinda makes several well-reasoned extensions and corrections to the official FACS system:

| Deviation | Detail |
|-----------|--------|
| **AU4 muscle splitting** | Treats corrugator supercilii, depressor supercilii, and procerus as independently activatable; original FACS groups them |
| **fAUx8 – Howler Mouth** | Replaces vague AU8 definition with a specific sphincter-like open-mouth action; removes AU25 dependency; allows lip contact at high intensity |
| **AU14 y-axis/z-axis** | Splits dimpler into planar variants not present in FACS Manual |
| **AU23 Type 2** | Adds "vertical type" lip tightener; FACS Manual only defines horizontal type; many incorrect reference sources conflate vertical type with lip pucker |
| **#notFACS tags** | Ear movement, open-eyed blink — included because observed frequently in practice |

---

## Connections to Wiki
- [[papers/ekman-friesen-1978-facs]] — original FACS system this site extends
- [[concepts/facial-blendshape-rigs]] — FACS AUs are the basis for most production blendshape rig shapes
- [[papers/li-2017-flame]] — FLAME expression basis uses FACS action units as initialization
- [[concepts/flame-model]] — FLAME's 100 expression components can be driven via FACS AU mapping
- [[papers/faceit-diaz-barros]] — FACEIT uses FACS blendshape weights; directly applicable
- [[papers/epic-2021-metahuman-rig]] — MetaHuman RigLogic is FACS-based; these AU definitions map to DNA controls
- [[papers/raman-2022-mesh-tension-wrinkles]] — expression wrinkles driven by AU activation

---

## Notes for Wiki Use
- Melinda's **AU4 3-muscle breakdown** is more granular than any academic paper in the wiki and directly useful for rig design
- The **AU23 Type 2 vertical tightener** is a production-relevant distinction absent from the literature; worth cross-referencing in concept pages
- The **AU20/AU21 risorius variability** note is a practical rigging gotcha — risorius may be anatomically absent; lip stretcher shapes may need to fall back to platysma-based alternatives
- The **ARKit to FACS guide** is a key resource for cross-referencing [[concepts/openxr-face-tracking]] and [[papers/ekman-friesen-1978-facs]]

---

## Eyebrow Combos Cheat Sheet
**Source:** https://melindaozel.com/facs-cheat-sheet/eyebrow-combos-cheat-sheet/  
**Assets:** `raw/assets/melindaozel/eyebrow-combos/` (11 GIFs, multi-person references)

The 3 primary brow AUs (1, 2, 4) combine into 7 combos. Isolated AUs are in the main FACS Study Guide; this page covers the 4 combinations:

### AU 1+2 — Full Brow Raise
**Muscles:** frontalis, pars medialis + frontalis, pars lateralis  
- Most common brow combo; signature for word emphasis, attentiveness, speech punctuation
- Core component of **surprise** prototype (also requires AU25+26)
- Observable effects: vertical skin stretch between eye and nose; upper eyelid shape change; hairline drag at high intensity (anatomical variation)
- Wrinkle pattern is **hereditary** — Melinda and her mother/aunt share "messy, bulky" raise; her brother and father share "neat, folded, straight" pattern

**GIF references:**
- `au1+2_full-brow-raise_front.gif` — Person A (Melinda), front view
- `au1+2_full-brow-raise_side.gif` — Person A, side view
- `au1+2_full-brow-raise_male.gif` — Person B (Melinda's brother)
- `au1+2_full-brow-raise_personC.gif` — Person C

### AU 1+2+4 — "Fear" Brows
**Muscles:** medial frontalis + lateral frontalis + corrugator supercilii/depressor supercilii/procerus  
- Prototypic brow configuration for **fear**
- AU4 strength can visually suppress AU1 appearance — intensity balance critical
- Wrinkle pattern changes going from 1+2 → 1+2+4: dip forms at medial brow; corrugator bunches/squeezes central forehead

**GIF references:**
- `au1+2+4_fear-brows_front.gif` — front, starts with 1+2 then adds AU4
- `au1+2+4_fear-brows_side.gif` — side view, same sequence

### AU 1+4 — "Sad" Brows
**Muscles:** frontalis, pars medialis + corrugator supercilii (primary)  
- Prototypic brow configuration for **sadness**; also signals worry, concern
- AU4 component is typically corrugator supercilii dominant (not procerus) in sadness
- Creates tent-like shape in upper eyelid: brow lowerer pushes skin down while inner brow raiser pulls up near tear duct
- Often asymmetric (especially visible in Melinda's example)

**GIF references:**
- `au1+4_sad-brows_front.gif` — Person A, front view (starts with AU4 then adds AU1)
- `au1+4_sad-brows_side.gif` — Person A, side view
- `au1+4_sad-brows_personC.gif` — Person C (simultaneous activation)

### AU 2+4 — "The Rock" Brows
**Muscles:** frontalis, pars lateralis + corrugator supercilii/depressor supercilii/procerus  
- Prototypic combo for **The Rock** / Dreamworks smug-face (asymmetric version)
- Brow lowering in this combo often driven primarily by corrugator supercilii
- Asymmetric AU2+4 = "the Dreamworks face" used in animated film villains/smug characters

**GIF references:**
- `au2+4_rock-brows_front.gif` — front, starts with AU2 then adds AU4
- `au2+4_rock-brows_side.gif` — side, starts with AU4 (procerus+depressor supercilii+corrugator) then adds AU2

**Rigging notes:**
- The 4 combos above should exist as dedicated blend shapes in a production FACS rig alongside isolated AU1, AU2, AU4 shapes — they are not simple additive combinations due to skin interaction and wrinkle interference
- For AU1+4, the tent-shape in the upper lid is a key sculpting target; pure additive LBS blend will not reproduce it

---

## Lower Face Cheat Sheet
**Source:** https://melindaozel.com/lower-face-cheat-sheet/  
**Assets:** `raw/assets/melindaozel/lower-face/` (19 GIFs)

Complete inventory of lower-face action units with animated GIF demonstrations:

| AU | Name | Muscle(s) | GIF Asset |
|----|------|-----------|-----------|
| AU10 | Upper Lip Raiser | levator labii superioris, caput infraorbitalis | `au10_upper-lip-raiser.gif` |
| AU11 | Nasolabial Furrow Deepener | zygomaticus minor | `au11_nasolabial-furrow-deepener.gif` |
| AU12 | Lip Corner Puller | zygomaticus major | `au12_lip-corner-puller.gif` |
| AU13 | Sharp Lip Puller | levator anguli oris (aka caninus) | `au13_sharp-lip-puller.gif` |
| AU14 | Dimpler | buccinator | `au14_dimpler.gif` |
| AU15 | Lip Corner Depressor | depressor anguli oris (aka triangularis) | `au15_lip-corner-depressor.gif` |
| AU16 | Lower Lip Depressor | depressor labii inferioris | `au16_lower-lip-depressor.gif` |
| AU17 | Chin Raiser | mentalis | `au17_chin-raiser.gif` |
| AU18 | Lip Pucker | incisivii labii superioris & inferioris | `au18_lip-pucker.gif` |
| AU20 | Lip Stretcher | risorius (with platysma) | `au20_lip-stretcher.gif` |
| AU22 | Lip Funneler | orbicularis oris | `au22_lip-funneler.gif` |
| AU23 | Lip Tightener | orbicularis oris | `au23_lip-tightener.gif` |
| AU24 | Lip Presser | orbicularis oris | `au24_lip-presser.gif` |
| AU25 | Lips Part | depressor labii inf. / relaxation of mentalis or orbicularis oris | `au25_lips-part.gif` |
| AU26 | Jaw Drop | masseter + temporalis + internal pterygoid (all relaxed) | `au26_jaw-drop.gif` |
| AU27 | Mouth Stretch | pterygoids + digastric | `au27_mouth-stretch.gif` |
| AU28 | Lip Suck | orbicularis oris | `au28_lip-suck.gif` |

### Lip Texture Extras (not AU-coded)
Two additional GIFs documenting lip surface physics:

| Asset | Description |
|-------|-------------|
| `lip-texture_sticky-lips.gif` | **Sticky lips** — lip tissue sticks and stretches briefly before separating during AU25 (lips part). Key detail for realistic digital human animation; often missed. |
| `lip-texture_glossy-lips.gif` | **Glossy lips** — reference for non-sticky lip separation with wet specular sheen. Contrast asset to sticky-lips. |

**Rigging/animation notes:**
- **AU26 vs AU27**: AU26 (jaw drop) is passive relaxation of masticatory muscles; AU27 (mouth stretch) requires active pterygoid contraction — they should be separate blend shapes even though both open the mouth
- **AU28 (lip suck)** nearly always co-activates AU17 (chin raiser) as a transition — plan for a combo shape or corrective
- **Lip stick** (sticky lips asset) is a secondary motion detail increasingly expected in digital human performance; orbicularis oris tension at lip margin drives it
- **AU20 variability**: risorius is absent in a significant portion of subjects — blend shape fallback to platysma is practical necessity
- **AU11** (nasolabial furrow deepener) is the rarest AU; easily confused with AU10; see Melinda's deep-dive post for disambiguation

---

## Upper Face Expanded
**Source:** https://melindaozel.com/upper-face-expanded/  
**Assets:** `raw/assets/melindaozel/upper-face-expanded/` (29 files: 16 GIFs, 12 PNGs, 1 JPG)

Expanded reference for AU1, AU2, AU4, AU5, AU6, AU7 — each with multi-view GIF demos, muscle diagrams, stylized animation examples, and comparative stills. Includes AU4's critical 3-muscle breakdown with per-muscle GIF isolation.

---

### AU1 — Inner Brow Raiser
**Muscle:** frontalis, medial area (aka pars medialis — semi-archaic term)

| Asset | Description |
|-------|-------------|
| `au1_inner-brow-raiser_static.png` | Before/after still reference |
| `au1_inner-brow-raiser_front-slow.gif` | Front view, slow |
| `au1_inner-brow-raiser_front-peak.gif` | Front view, peak hold |
| `au1_inner-brow-raiser_stylized.png` | Stylized character example |
| `au1_vs_au1+2_comparison.png` | Side-by-side: AU1 vs. full brow raise (1+2) |

**Notes:**
- Widely perceived as difficult to perform voluntarily — Melinda argues this is a misconception from idealized reference imagery
- Core component of **surprise** (AU1+2+5 upper face) and **sadness** (AU1+4)
- Combines with AU2 for full brow raise; with AU4 for sad brows; with AU2+4 for fear brows
- Wrinkle pattern is strongly **hereditary** — frontalis anatomical variation (bifurcation depth/position) determines raise style; cannot be inferred from neutral geometry alone
- Many online AU1 references are **incorrect** — common error is showing a full brow raise (1+2) labeled as AU1

---

### AU2 — Outer Brow Raiser
**Muscle:** frontalis, lateral area (aka pars lateralis — semi-archaic term)

| Asset | Description |
|-------|-------------|
| `au2_outer-brow-raiser_static.png` | Before/after still reference |
| `au2_outer-brow-raiser_front.gif` | Front view |
| `au2_outer-brow-raiser_side.gif` | Side view |
| `au2_outer-brow-raiser_stylized.png` | Stylized character example |
| `au2_vs_au1+2_comparison.png` | Side-by-side: AU2 vs. full brow raise (1+2) |

**Notes:**
- Much easier than AU1 to perform voluntarily for most people
- Significant minority can only perform AU2 unilaterally or cannot perform it at all
- **Frontalis anatomical diversity** (major rigging/tracking implication): the frontalis is frequently shown as a single muscle with a single bifurcation pattern, but in reality:
  - Some subjects have no bifurcation (continuous frontalis)
  - Some have a fully split frontalis with a gap at center
  - Bifurcation depth and position vary widely
  - These differences govern wrinkle pattern, brow shape at peak, and inter-subject variation in face tracking output

---

### AU4 — Brow Lowerer
**Muscles:** corrugator supercilii + procerus + depressor supercilii (three independently activatable muscles)

| Asset | Description |
|-------|-------------|
| `au4_brow-lowerer_before-after.png` | Before/after still |
| `au4_brow-lowerer_front-slow.gif` | Front view, slow |
| `au4_brow-lowerer_front.gif` | Front view |
| `au4_brow-lowerer_stylized.png` | Stylized example (all 3 muscles combined) |
| `au4_corrugator-supercilii_isolated-personA.gif` | Corrugator supercilii in isolation (Person A) |
| `au4_corrugator-supercilii_isolated-personC.gif` | Corrugator supercilii in isolation (Person C) |
| `au4_procerus_isolated.gif` | Procerus dominant (performed from raised brow) |
| `au4_depressor-supercilii_posed.gif` | Depressor supercilii, posed/asymmetric |
| `au4_depressor-supercilii_spontaneous.gif` | Depressor supercilii, spontaneous |

**Per-muscle anatomy:**

**1. Corrugator supercilii**
- Draws brows toward each other ("knitting")
- Causes **vertical** glabellar wrinkles
- Easiest of the three to isolate voluntarily

**2. Procerus**
- Technically a nasal muscle; pushes down medial brow area above nose
- Causes **horizontal** wrinkle at nasal root
- Melinda cannot isolate procerus from neutral — only from a fully raised brow position; note this as a voluntary control caveat

**3. Depressor supercilii**
- Technically classified as an eye muscle
- Actively debated in anatomy literature whether it is a distinct muscle or part of orbicularis oculi
- Melinda endorses it as distinct (consistent with surgeons/dermatologists/ophthalmologists)
- Demonstrated via posed asymmetric action and spontaneous GIFs

**Rigging implications:**
- Production rigs that treat AU4 as a single blend shape conflate three distinct movement patterns — consider splitting into corrugator, procerus, and depressor supercilii shapes for maximum expressivity
- Corrugator produces horizontal brow convergence + vertical wrinkles; procerus produces medial depression + horizontal nasal root wrinkle; depressor supercilii produces inner brow pull-down with different vector than corrugator — the three shapes are **not additive LBS equivalents** of one another

---

### AU5 — Upper Lid Raiser
**Muscle:** levator palpebrae superioris

| Asset | Description |
|-------|-------------|
| `au5_upper-lid-raiser_static.png` | Still reference |
| `au5_upper-lid-raiser_muscle.png` | Muscle anatomy diagram |
| `au5_upper-lid-raiser_front.gif` | Front view |
| `au5_upper-lid-raiser_side.gif` | Side view |

**Notes:**
- Rarely confused with other AUs, but strong AU1+2 can create a false impression of lid retraction (sclera exposure) — important disambiguation for automated FACS coding
- Harder to detect when co-occurring with AU4, AU6, AU7, or AU9 (all compress the peri-orbital area)
- Prototype component of **surprise** upper face: AU1+2+5
- Combined with AU4 and AU7 in upper-face **anger** display

---

### AU6 — Cheek Raiser
**Muscle:** orbicularis oculi, orbital part (aka pars orbitalis)

| Asset | Description |
|-------|-------------|
| `au6_cheek-raiser_static.jpg` | Still reference |
| `au6_cheek-raiser_front.gif` | Front view |
| `au6_cheek-raiser_side.gif` | Side view |

**Notes:**
- One of the most difficult AUs to perform voluntarily
- Frequently co-activated with AU7 (lid tightener) — the palpebral and orbital portions of orbicularis oculi are anatomically adjacent, making independent voluntary control difficult
- Also accidentally paired with AU12 due to learned association (cheek raise + lip corner pull = happiness)
- Presence of AU6 is the distinguishing marker of a **Duchenne smile** (authentic happiness) when combined with AU12
- Also present in: sadness prototypes, pain, squinting, skepticism

---

### AU7 — Lid Tightener
**Muscle:** orbicularis oculi, palpebral part (aka pars palpebralis)

| Asset | Description |
|-------|-------------|
| `au7_lid-tightener_muscle.png` | Muscle anatomy diagram |
| `au7_lid-tightener_front.gif` | Front view |
| `au7_lid-tightener_side.gif` | Side view |

**Notes:**
- Easier to voluntarily produce than AU6, but co-activation of AU6 increases with intensity of AU7
- Difficult to detect when combined with AU9 (nose wrinkler)
- Functional contexts: concentration, skepticism, difficulty seeing (squinting to focus)
- Upper-face **anger** involves AU4 + AU5 + AU7

---

**Key rigging takeaways from Upper Face Expanded:**
- **AU4 must be split into 3 sub-shapes** for correct anatomical representation: corrugator (medial convergence + vertical wrinkles), procerus (medial depression + horizontal nasal root), depressor supercilii (medial inner corner pull-down)
- **AU6 and AU7 are frequently confused** even by experienced animators; having clear GIF references for each in isolation is critical for training review
- **Frontalis variation** (AU1/AU2) is systematic and hereditary — face tracking systems should account for per-subject frontalis topology rather than assuming a single muscle shape
- **AU5 + AU1+2** interaction: strong full brow raise can artifactually appear to include AU5 — a known false-positive source in automated FACS coding systems

---

## Emotion References
**Source:** https://melindaozel.com/emotion-references/  
**Assets:** `raw/assets/melindaozel/emotion-references/` (9 MOV videos, self-hosted)  
**Media type:** All clips are video (`.mov`), not GIFs. Three additional clips hosted on Vimeo (not downloadable).

All clips are **unposed, spontaneous** expressions of genuine emotion. Melinda notes camera presence may introduce some exaggeration and flags cases where disingenuousness cannot be fully ruled out.

---

### Happiness Spectrum

| Asset | Section | Context | AU notes |
|-------|---------|---------|----------|
| `happiness_laughing-natural.mov` | laughing | Spontaneous laughter during a brow raise reference session with Friend H | Natural laughter prototype: AU6+12+25+26, likely AU1+2, possible AU5 |
| `happiness_laughing-hard-blink.mov` | laughing + hard blink | Spontaneous laughter with Friend A; camera was present for expression posing session | Laughter + AU46 hard blink interaction |
| `happiness_trying-not-to-laugh.mov` | trying not to laugh | Same Friend A session; trying to stop laughing and resume expression posing | Key reference: AU24 (lip presser) used to actively suppress open-mouth smile — and failing. Genuine laughter suppression attempt |

---

### Sadness Spectrum

| Asset | Section | Context | AU notes |
|-------|---------|---------|----------|
| `sadness_crying-while-talking.mov` | crying while talking | From "August Anxcriety" series; Melinda had been sobbing for an hour from stress/anxiety/depression, then began talking to camera | Sustained post-sob face + active speech; FACS coding complicated by overlay of AU6+17+1+4 with speech AUs |
| *(Vimeo 639686718)* | laughing transition to crying (NEW) | Anxiety-induced cry triggered by extended laughing | Rare transition reference: first 3s = laughter, seconds 3–6 = mixed laughter+cry, second 8+ = full cry. Prototypic emotion blend |
| `sadness_mixed-laughing-while-crying.mov` | mixed laughing while crying | August Anxcriety continuation; recognized absurdity of situation and began laughing briefly | Simultaneous AU6+12 (laughter) + AU1+4+17+54 (crying) — key reference for blended emotion rigs |
| `sadness_sadness-to-laughter.mov` | sadness to laughter | Depression cry while watching a movie; funny scene triggered laughter | Full-face and 3/4-view; sadness-to-laughter transition showing AU configuration shift |
| `sadness_sticky-lips-post-cry.mov` | sticky lips, post-cry | August Anxcriety; post-cry lip stickiness | Lip stickiness significantly increases after extended crying; more pronounced than baseline sticky-lips reference. Key secondary motion detail |
| `sadness_blowing-nose-post-cry.mov` | blowing nose, post-cry | August Anxcriety nose blow | Post-cry nose clearing; AU38 (nostril dilator) + facial compression |

---

### Disgust Spectrum

| Asset | Section | Context | AU notes |
|-------|---------|---------|----------|
| `disgust_reaction-gross-drink.mov` | reaction to gross drink | Drinking an unappealing beverage in harsh, bright light | Genuine disgust reaction. **Note:** bright lighting likely amplified upper face AUs; Melinda did not control for exaggeration in this clip. Expected AUs: AU9+15+16+17+25, possible AU4+7 |

---

### Miscellaneous

| Asset | Section | Context | AU notes |
|-------|---------|---------|----------|
| *(Vimeo 639696159)* | sassy vibes | Subject post-breakup, happily/sassily celebrating; in slow-mo from second 2 onward | Catty/fake smile reference. Strong asymmetric mouth movements consistent across all of subject's expressions — useful for studying individual facial asymmetry patterns |
| *(Vimeo 639696212)* | venting frustration and bitterness | Instagram story; subject recounting encounters with a dangerous person | Predominantly authentic despite IG story context; frustration + bitterness emotional blend. Caveat: IG performance context acknowledged |

---

**Key animation/rigging takeaways from Emotion References:**
- **Laughter suppression** (trying-not-to-laugh clip): AU24 (lip presser) is the primary voluntary suppression mechanism — animators often omit this when showing a character holding back a smile; it's a key believability marker
- **Laughing → crying transition** (Vimeo clip): the blend zone (seconds 3–6) is the most valuable reference; AU configurations for both emotions partially coexist before resolving to cry state
- **Post-cry sticky lips** is documented as significantly more pronounced than neutral sticky lips — relevant for any sustained-crying sequence in animation
- **Disgust clip lighting caveat**: upper face AUs (AU5, AU7) may be artificially intensified by harsh overhead lighting; use lower-face AUs (AU9, AU15–17) as the primary disgust reference from this clip
- **Individual asymmetry**: the sassy vibes subject shows consistent facial asymmetry across genuine and posed expressions — confirms asymmetry is a structural/neuromuscular property, not an acting choice; important for character design where asymmetry is used as a personality signal
