---
question: "Detailed notes from Melinda Ozel's Face the FACS deep-dive articles (premium)"
date: 2026-04-22
sources:
  - https://melindaozel.com/upper-lip-raiser-vs-nasolabial-furrow-deepener/
  - https://melindaozel.com/levator-labii-superioris-vs-zygomaticus-minor/
  - https://melindaozel.com/forehead-dynamics-frontalis-vs-occipitalis/
  - https://melindaozel.com/lip-tightener-vs-lip-presser/
  - https://melindaozel.com/lip-tightener/
  - https://melindaozel.com/advanced-blend-shape-tips-for-blinks/
  - https://melindaozel.com/all-about-upper-lid-raiser-au5/
  - https://melindaozel.com/zygomaticus-major-variations-the-dimple/
  - https://melindaozel.com/frontalis-variation/
  - https://melindaozel.com/inner-brow-raiser-deep-dive/
  - https://melindaozel.com/a-wrinkle-in-time-part-ii/
  - https://melindaozel.com/a-wrinkle-in-time-building-characters-with-real-story-lines/
  - https://melindaozel.com/breaking-down-nose-wrinkler/
access: Premium member login (LucaPrasso)
---

# Melinda Ozel — Deep-Dive Articles

Notes from premium articles on Face the FACS (melindaozel.com). Each section maps to one article. See also [[queries/face-the-facs-site-report]] for the overview.

---

## AU10 vs AU11 — Upper Lip Raiser vs. Nasolabial Furrow Deepener

**Source:** /upper-lip-raiser-vs-nasolabial-furrow-deepener/ and /levator-labii-superioris-vs-zygomaticus-minor/

### The Three Upper Lip Elevators

Anatomy recognizes **three upper lip elevator muscles**:
1. **Levator labii superioris** → AU10 (upper lip raiser)
2. **Levator labii superioris alaeque nasi (LLSAN)** → AU9 (nose wrinkler — also a lip elevator)
3. **Zygomaticus minor** → AU11 (nasolabial furrow deepener)

**Critical production note:** In art and technology, AU10 (via levator labii superioris) is overused as the default upper-lip-elevation shape, largely due to name bias. "Upper lip raiser" explicitly names the function; the other two muscles' names don't reveal their lip-lifting role. This leads to systematic misuse of AU10 where AU11 or LLSAN activation would be more anatomically correct.

### How to Distinguish AU10 from AU11

Both actions pull the top lip upward and alter the nasolabial furrow — making them visually similar. Key distinguishing markers (from side-by-side GIF comparison with landmarks):

| Feature | AU10 (upper lip raiser) | AU11 (nasolabial furrow deepener) |
|---|---|---|
| **Philtrum pore movement** | Mostly straight upward | Diagonal, more lateral |
| **Upper lip contour pull** | Upward | Lateral |
| **Nostril wing effect** | Dragged upward + slightly outward (more dramatic) | Marginally affected |
| **Pores above nostrils** | Pulled directly upward | Almost stationary |
| **Outer cheek contour** | Barely changes; slight upward drag only | Puffed outward, pulled laterally and slightly upward |
| **Direction summary** | Medial, vertical bias | Lateral, horizontal bias |

### Zygomaticus Minor — Variability

Zygomaticus minor is documented as one of the **more variable facial muscles**, varying in:
- Size
- Origin
- Insertion
- Number of fascicles

This variability makes AU11 particularly hard to recognize and reproduce consistently. The FACS Manual and most anatomy textbooks have done a poor job defining AU11; it is systematically underrepresented in reference libraries.

**Rigging implication:** Avoid designing your AU10 shape to include lateral cheek movement — that is AU11 territory. Keep AU10 medially biased.

---

## Forehead Dynamics — Frontalis vs. Occipitalis

**Source:** /forehead-dynamics-frontalis-vs-occipitalis/

### Frontalis

- Origin: **galea aponeurotica** (tendinous sheet)
- Insertion: superficial muscles of the lower forehead (corrugator, procerus, orbicularis oculi)
- **No bony attachments**
- Function: elevates brows + **drags part of the scalp forward**

Because frontalis has no bony attachments, it must pull against other structures. When it contracts, it doesn't just raise the brows — it applies tension to the scalp.

### Occipitalis

- Origin: near the **base of the skull** (bony attachment)
- Insertion: galea aponeurotica (where frontalis *originates*)
- Function: **retracts the scalp** (pulls it back)

### Synergistic / Antagonistic Relationship

When frontalis elevates brows and strains the scalp forward, occipitalis anchors and counterbalances by retracting. Their combined effects can be described as **synergistic** (they cooperate to produce controlled brow movement) or **antagonistic** (they pull in opposite directions on the galea).

**Rigging implication:** Brow raise shapes that include realistic scalp tension and secondary displacement should account for this opposing force. Very high-intensity AU1+2 in real humans shows visible scalp movement — relevant for hyperrealistic digital humans.

---

## AU23 vs AU24 — Lip Tightener vs. Lip Presser

**Source:** /lip-tightener-vs-lip-presser/ and /lip-tightener/

### The Confusion

Both AU23 (lip tightener) and AU24 (lip presser) are driven by **orbicularis oris** and produce surface-level lip compression. They are among the most frequently confused FACS shapes — even in professional references.

### AU23 — Lip Tightener (horizontal type)

- Classic FACS definition: tightening/narrowing of the lips on a **horizontal plane**
- The rope analogy: the orbicularis fibers tighten like a rope under tension — but crucially, the tension is not induced by a horizontal pull from outside. The tightening is an intrinsic sphincter-like contraction.
- Visible effect: lips appear more taut, edges more defined, but no visible forward protrusion or vertical compression
- **Difficulty:** AU23 is notoriously hard to perform in isolation. People reflexively add AU18 (lip pucker), AU24 (lip presser), or both.

### Vertical Lip Tightener — "Lip Cincher" (Melinda's extension)

The FACS Investigator's Guide admits: *"FACS probably does not include all of the visible, reliably distinguishable actions in the lower part of the face."*

Melinda's coined action: **lip cincher** (also called "vertical lip tightener"):
- Orbicularis oris tightens on a **vertical plane** — top lip drawn down, bottom lip slightly up, toward center
- Not in official FACS
- **Commonly mistaken for AU23 (horizontal type)** in online references
- The mistake: most AU23 reference images online actually show vertical lip cincher or a lip cincher + AU18 combo
- **Lipsync value:** highly useful blendshape for lipsync shape sets even though not FACS-official

### AU24 — Lip Presser

- Orbicularis oris compresses the lips together with visible **pressure** between upper and lower lip
- Distinguished from AU23 by the lip-pressing/contact component
- AU24 is the primary voluntary mechanism for **laughter suppression** (holding back a smile) — see [[queries/face-the-facs-site-report]] emotion references section

### Common Misrepresentations in the Wild

When you see references labeled "AU23 lip tightener" on the internet, they typically show:
- **AU18** (lip pucker) — incisivus medial draw
- **AU24** (lip presser) — lip compression with contact
- **Lip cincher** — vertical orbicularis tightening

A true AU23 is visually subtle: taut lip edges, no pucker, no pressing, no forward protrusion.

---

## Advanced Blink Tips — Blinkles & Timing

**Source:** /advanced-blend-shape-tips-for-blinks/

### Blinkles

Melinda coins **"blinkles"**: the wrinkles that form during a blink. These are distinct from resting wrinkles and expression wrinkles — they appear only during the blink motion itself and involve orbicularis oculi palpebral contraction compressing lower lid tissue.

### Blink Timing Asymmetry

Key reference note (citing scientific literature): after the **turning point** (maximum closure), the **upstroke** (reopening) continues at approximately **half the speed** of the downstroke (closing). This is a physiologically documented asymmetry — important for timing blink animations realistically.

**Rigging implication:** A blink animation curve is NOT symmetric. The close phase should be approximately twice as fast as the open phase.

---

## AU5 — Upper Lid Raiser (All About)

**Source:** /all-about-upper-lid-raiser-au5/

### Levator Palpebrae Superioris (LPS) — Anatomy

- **Origin:** Sphenoid bone (inside the orbit)
- **Insertion (two layers):**
  - Superficial layer → **tarsal plate** (dense fibrous tissue inside the upper eyelid)
  - Deep layer → **superior conjunctival fornix**
- LPS is both **skeletal** (voluntary, conscious control) AND **smooth muscle** (involuntary)
  - The smooth muscle component = **superior tarsal muscle (Müller's muscle)**, attached to LPS; assists with lid retraction
- **Key fact:** LPS is active any time the eyes are open. AU5 is only FACS-coded when there is a *noticeable increase* in lid retraction beyond baseline.

### Emotion Prototype Involvement

Per Ekman prototypes (useful but not prescriptive — Melinda holds a pluralist view on emotion theory):
- **Surprise:** AU1+2 (+ AU5, upper face component)
- **Fear:** AU1+2+4+5
- **Anger:** AU4+5+7

**Important caveat from Melinda:** Basic emotion prototypes are useful heuristics but should not be over-applied. "Emotions are complex systems contingent on context, culture, and individuality." AU5 is more reliably read as a general indicator of **alertness and heightened arousal** than as a specific emotion marker.

### Functional Contexts Beyond Emotion

- Concentration / alertness
- Sudden loud noise
- Physical exertion (tennis, effort) — high-intensity arousal
- Any sudden stimulus requiring increased visual acuity

### Eyelid Diversity Note

Eyelid physical characteristics are diverse across individuals: lid thickness, fold depth, skin excess (epicanthal folds), ptosis baseline. These differences substantially affect how AU5 appears — a given individual's AU5 may look more or less dramatic than average.

---

## Zygomaticus Major Variations & the Dimple

**Source:** /zygomaticus-major-variations-the-dimple/

### What Causes Smile Dimples

Smile dimples are caused by a variation of **zygomaticus major** (the AU12 muscle) involving **two insertion points** (bifid zygomaticus major) rather than the standard single insertion point.

- Standard: single insertion → lip corner area
- Bifid variant: two insertions → second insertion creates a tethering point that produces the characteristic skin indentation (dimple) when the muscle contracts during smiling

### Literature References

- Literature documents the bifid variant as a **relatively common** anatomical variation
- Some case reports describe a variant where the extra branch of zygomaticus major inserts into **orbicularis oris** muscle itself
- Additional reports describe **quadrifid** variants (four insertion points) in rare cases
- Primary reference: Pessa et al. — paper on bifid zygomaticus major

### Rigging Implications

- Dimples cannot be reproduced by standard linear blend of AU12 shapes — they require either:
  - A dedicated corrective shape that activates on top of AU12
  - A secondary geometry locked to an internal surface attachment point
- For character design: dimple presence/absence is genetically/anatomically determined — tied to zygomaticus major topology, not AU strength

---

## Frontalis Variation — Why Wrinkle Patterns Differ

**Source:** /frontalis-variation/

### Wrinkle Formation Principle

> **Wrinkles form perpendicular to the direction of muscle fibers.**

Since frontalis fibers are **vertical**, frontalis contraction produces **horizontal(ish) wrinkles** across the forehead.

### Frontalis Anatomy Basics

- Frontalis is a paired muscle with a central tendinous division — the **galea aponeurotica** (also: epicranial aponeurosis, aponeurosis epicranialis)
- The central split = **bifurcation**
- Standard depiction: symmetric bifurcated muscle with medial (pars medialis) and lateral (pars lateralis) portions

### Shape Diversity

The mainstream bifurcated frontalis shape is **not the only shape**. Documented variations include:
- **No bifurcation** (continuous frontalis, no split)
- **Partial bifurcation** at varying depths
- **Full split** with a gap at center (completely divided)
- Variations in **width**, **height**, **angle**, and **relative position** among surrounding muscles (corrugator, procerus)

### Why This Matters

| Application | Implication |
|---|---|
| FACS rig shape libraries | AU1 and AU2 appearance is individual-specific; building shapes from a single reference will not generalize |
| Facial mocap / face tracking | Forehead hotspot positions for marker/electrode placement vary per subject |
| EMG electrode placement | Optimal placement depends on where the muscle actually sits (individual anatomy required) |
| FACS coding | AU1 vs AU2 vs AU1+2 vs AU1+4 disambiguation is frontalis-topology-dependent |
| Character design | Drawing/sculpting anatomy-accurate brow raises requires knowledge of per-character frontalis shape |

**Key insight from Melinda:** "AU1 and AU2 are moving targets." What constitutes "inner brow raise" vs "outer brow raise" vs "full brow raise" varies considerably based on individual frontalis shape, size, and location. A fully split frontalis person will produce AU1 that looks markedly different from someone with a centered, unsplit frontalis.

---

## Inner Brow Raiser Deep Dive — AU1

**Source:** /inner-brow-raiser-deep-dive/

### Definition

AU1 (inner brow raiser) raises the **medial brow/forehead area** via contraction of the **medial region of the frontalis** muscle.

### The Most Common Mistake: Adding Corrugator

The most frequent error in AU1 FACS shape creation is **mixing in corrugator supercilii (AU4)**. This produces a shape that shows brow convergence/knitting along with medial raise — which is AU1+4, not AU1 alone.

Root causes:
- Many AU1 references in widely used anatomy textbooks (including textbooks used in art programs) are inaccurate
- AU1 is genuinely difficult to perform in isolation voluntarily — the corrugator tends to co-activate
- When creating reference captures for FACS shapes, it's essential to verify marker/tracking data shows AU4 is absent

### Effects of True AU1

**Primary effects:**
- Raises medial brow
- Stretches skin near the inner eye cover fold

**Secondary effects (highly variable per individual):**
- Pull location varies: some at the innermost tip of the inner brow, others half an inch away (toward center of brow)
- Wrinkle patterns vary significantly:
  - Some individuals: no wrinkles
  - Some: straight wrinkles concentrated in center of forehead
  - Variation governed by frontalis shape and skin properties (see frontalis-variation article)

### Key Emotion / Expression Role

- Core component of **sadness** prototype: AU1+4 ("sad brows")
- Core component of **surprise**: AU1+2
- Core component of **fear**: AU1+2+4

### Rigging Note

If your AU1 shape shows any brow convergence, glabellar bunching, or inner brow depression — it contains AU4. Resculpt to isolate the medial upward pull only.

---

## Wrinkle Tips — Dynamic & Static Wrinkles

**Sources:** /a-wrinkle-in-time-building-characters-with-real-story-lines/ (Part I) and /a-wrinkle-in-time-part-ii/ (Part II)

### Part I — Dynamic Wrinkles (Expression Lines)

**Dynamic wrinkles** (also "dynamic expression lines") are formed by **repeated facial expressions**. They are perpendicular to the underlying muscle fiber direction.

#### Wrinkles as Storytelling

Dynamic wrinkles reflect a character's habitual emotional life. Useful for character design:
- **Medial brow wrinkles (AU1 dominant):** suggests empathetic, hopeful, or worried nature
- **Full brow raise wrinkles (AU1+2):** suggests sociable, engaged, active listener
- **Brow furrow wrinkles (AU4):** suggests frequent anger, concentration, confusion, or tiredness
- **Orbital eye wrinkles / crow's feet (AU6, orbicularis orbitalis):** joy, repeated squinting
- **Nasolabial smile lines (AU12):** happiness history

#### Analysis Example (Photojournalism)

Using portraits by photographer Araki (cited as reference):
- *"The Warm Woman"*: medial brow wrinkles (AU1 dominant) + eye and mouth joy lines → empathetic, joyful character
- *"The Wise Man"*: fuller brow wrinkles (AU1+2), deeper furrow lines (AU4), limited lower face visibility → sociable + habitual brow concentration

**Warning:** Dynamic wrinkles are NOT guaranteed knowledge about habitual expressions. Wrinkle patterns are also affected by:
- Facial morphology / bone structure
- Genetics (Melinda and her mother share AU2 asymmetry as a neutral quirk, not an emotional tendency)

### Part II — Static Wrinkles

**Static wrinkles** are NOT caused by muscle movement. Sources include:
- **Gravity** — skin folds from gravitational loading over decades
- **Compression** — pressure from sleeping positions, habitual postures
- **Intrinsic aging** — collagen/elastin degradation, skin thinning
- **Sun damage** — extrinsic aging via UV-induced elastin breakdown
- **Anisotropy** — skin is directionally dependent; wrinkles form along lines of least mechanical resistance

#### Sleep Position Wrinkles

**Example: Anthony Hopkins** — deep vertical crease on the left half of his forehead. Cannot be explained by any muscle movement. Explained by **longterm pressure from sleeping on his left side**. Melinda notes this crease is on the side favored by left-side sleepers (per ergonomics literature).

**Rigging implication:** For aged or established characters, static wrinkles should be modeled into the neutral mesh — not as blendshapes, but as permanent geometry. They should not change with expression (or only deform passively under skin stretch).

---

## Breaking Down Nose Wrinkler — AU9

**Source:** /breaking-down-nose-wrinkler/

### Full Expression Context

AU9 (nose wrinkler) driven by **levator labii superioris alaeque nasi (LLSAN)** is almost never seen in complete isolation. The full typical nose wrinkler expression involves:

**Full FACS coding: AU4+6+7+9+10+15+17** (and frequently AU25 for any lip parting)

Per Melinda's video breakdown:
- **AU2+4** — outer brow raise + brow lowerer (secondary brow involvement)
- The brow lowering in AU9 is NOT driven by LLSAN itself — it comes from depressor supercilii/procerus (components of AU4)
- At high intensity: AU24 can be added → sequence: 2+4+5+6+7+9+10+15+17+24, then AU5 relaxes out

### Key Notes

1. **Some individuals are missing corrugator** — more common than typically assumed. In these subjects, the brow-lowering component of nose wrinkler will appear different or absent.
2. **Nostril flaring (AU38)** is prevalent in most nose wrinkler expressions but is frequently not coded. Watch for it and include it in shape sets.
3. Whenever lips are parted in any expression, **AU25 should always be assumed** (coded separately).
4. The **infraorbital triangle** is the key diagnostic region for AU9/10/11 disambiguation — changes in this zone differentiate the three middle-face elevators.

### Rigging Implications

- A standalone AU9 blendshape will look isolated/unnatural in expressions — plan for corrective combos with AU4 components
- AU38 (nostril dilator) should be part of any disgust/nose wrinkle expression shape set
- The LLSAN is also the primary muscle for AU9 AND acts as an upper lip elevator (relevant for AU10 vs AU9 disambiguation)

---

## Connections

- [[concepts/facs]] — all AUs referenced above
- [[concepts/wrinkle-systems]] — dynamic vs static wrinkle taxonomy from Part I/II
- [[concepts/facial-blendshape-rigs]] — production implications throughout
- [[concepts/arkit-blendshapes]] — ARKit missing AUs (AU11, AU23, AU38, AU39)
- [[queries/face-the-facs-site-report]] — site overview and full AU inventory
