---
title: "Visemes — Speech Animation Shapes"
tags: [blendshapes, speech-driven-animation, facial-capture, facs, digital-human]
---

## Definition

A **viseme** is the visual counterpart of a phoneme: the mouth/face shape produced during the articulation of a sound. Unlike phonemes (which are defined by acoustics), visemes are defined by the observable lip, jaw, and tongue configuration. Multiple phonemes that produce the same visible mouth shape share a viseme group.

**Key caveat (Melinda Ozel):** Each viseme is variable. While some visemes possess fixed characteristics required for mechanical production (e.g. m/b/p will always need the lips to close entirely or nearly entirely), facial actions required for each viseme will fluctuate depending on individual facial features, speech context, and coarticulation.

---

## Viseme Groups — American English

Source: Melinda Ozel, *Viseme & Speech Reference Guide* (Face the FACS, 2024). This guide goes deeper than the free Viseme Cheat Sheet; each entry includes Vimeo video references (realtime + slowmo) of posed phoneme production.

### Basic Consonants

| Viseme Group | IPA | Example Word | Phoneme Classification |
|---|---|---|---|
| neutral / silent | — | (rest) | no sound, relaxed |
| p/b/m | /p/, /b/, /m/ | pout, buccinator, masseter | bilabial; /p/ voiceless plosive, /b/ voiced plosive, /m/ voiced nasal |
| ʧ / ʤ / ʃ / ʒ | /ʧ/, /ʤ/, /ʃ/, /ʒ/ | chin; jaw/gem; shine/spatial; genre/measure | post-alveolar; /ʧ/ voiceless affricate, /ʤ/ voiced affricate, /ʃ/ voiceless fricative, /ʒ/ voiced fricative |
| t/d | /t/, /d/ | temporalis, depressor | alveolar plosive; /t/ voiceless, /d/ voiced |
| f/v | /f/, /v/ | face, viseme | labiodental fricative; /f/ voiceless, /v/ voiced |
| k/g | /k/, /g/ | king, guess | velar plosive; /k/ voiceless, /g/ voiced |
| h | /h/ | hippocampus, happy | glottal, fricative, voiceless |
| (light) l | /l/ | labial | alveolar, lateral, voiced |
| n / (dark) l | /n/ | nasal | alveolar, nasal, voiced |
| r / w / oo | /r/, /w/, /u/ | red; (w); food/rue/mood | post-alveolar approximant (r/w); /u/ grouped here for lip rounding similarity |
| s/z | /s/, /z/ | see, zygomatic | alveolar fricative; /s/ voiceless, /z/ voiced |
| θ / ð (th) | /θ/, /ð/ | wreath (voiceless), thoracic (voiced) | dental fricative |

### Consonant Blends

| Viseme | Example | Notes |
|--------|---------|-------|
| bl | blot, blender | onset cluster |
| gl | glow, glamor | onset cluster |

### Vowels

| Viseme | IPA | Example Words |
|--------|-----|---------------|
| ɑ (ah) | /ɑ/ | jaw, cause, stop |
| æ | /æ/ | cat, FACS, zygomaticus |
| ɛ (eh) | /ɛ/ | any, kept, levator |
| i (ee) | /i/ | eel, cheese, meat |
| ɪ (ih) | /ɪ/ | lip, which |
| u (oo) | /u/ | food, rue, mood (shared group with r/w consonants above) |
| ʊ (ouh) | /ʊ/ | puller, look, good |
| oʊ (oh) | /oʊ/ | lowerer, slow, moat |
| ɔɪ (oy) | /ɔɪ/ | joy, soy, join |
| ə (uh) | /ə/ | upper, other |

---

## p/b/m — Important Distinctions

Though p/b/m is one viseme group, /m/ differs critically from /b/ and /p/:

- **/m/ is nasal**: sound is produced while lips are closed; air escapes through the nose. Lips can stay together throughout.
- **/p/ and /b/ are plosives (stops)**: require a burst of air released at lip reopening. Three phases:
  1. **approach** — lips come together
  2. **hold** (occlusion/closure) — lips held closed to build pressure
  3. **release** (burst/plosion) — lips part, releasing built-up air pressure

**Important:** /b/ and /p/ require the lips to **part** after initial closure to propel air for the plosive sound.

**Edge case:** When /p/ is followed by /f/ (e.g. "stepfather", "hopeful"), the /p/ can lose part of its closure during transition — producing a [voiceless labiodental affricate](https://en.wikipedia.org/wiki/Voiceless_labiodental_affricate). These are standard exceptions in lipsync timing.

---

## Visemes vs. FACS

Viseme shapes are produced by combinations of FACS Action Units. Key mappings:

| Viseme Group | Primary AUs Active |
|---|---|
| neutral/silent | none (relaxed) |
| p/b/m | AU24 (lip presser) → lip closure; AU25 (lips part) for /b/ & /p/ release |
| ʧ/ʤ/ʃ/ʒ | AU22 (lip funneler) + partial AU26 (jaw drop) |
| f/v | lower lip contacts upper teeth; AU16 (lower lip depressor) |
| i (ee) | AU20 (lip stretcher) — wide mouth, teeth visible |
| u/oo | AU18 (lip pucker) or AU22 (lip funneler) — rounded lips |
| ə/ɑ | AU26 (jaw drop) dominant |
| θ/ð (th) | tongue tip contacts upper teeth; minimal AU movement |

See [[concepts/facs]] for full AU definitions.

---

## Viseme Blendshapes in Production Rigs

Production lipsync workflows typically use **15–17 viseme blendshapes**, not one per phoneme. Common sets:

- **Preston Blair (13 visemes)**: the industry-standard traditional set; often seen in 2D animation
- **ARKit phoneme blendshapes**: not directly viseme-indexed; driven procedurally from audio
- **NVIDIA Maxine / Audio2Face**: 46-phoneme output retargeted to viseme blendshapes
- **Melinda Ozel's system**: viseme groups (as above) with phoneme-level detail for lipsync quality

For production, lipsync systems (e.g. Melinda Ozel's *All About Lipsync* course) drive **per-phoneme timing** into the viseme blendshapes, with coarticulation handled by the solver or animator.

---

## Coarticulation

Natural speech involves **coarticulation**: overlapping and anticipatory articulation of adjacent phonemes. The jaw position for an upcoming vowel begins forming while a preceding consonant is still in production. This is why:
- Purely rule-based phoneme→viseme mapping sounds robotic
- Neural lipsync models (FaceFormer, SAiD) produce more natural results — they predict continuous weight sequences rather than per-phoneme on/off switches

See [[concepts/speech-driven-animation]] for neural approaches.

---

## Key Papers

- [[papers/taylor-2017-speech-animation]] — LSTM-based lipsync; one of the first deep learning approaches
- [[papers/fan-2022-faceformer]] — Transformer speech-driven animation; wav2vec 2.0 audio features
- [[papers/medina-2022-tongue-animation]] — inner-mouth viseme shapes (tongue, jaw, lips simultaneously)

## Connections

- [[concepts/speech-driven-animation]] — neural methods for audio-driven viseme animation
- [[concepts/blendshapes]] — viseme shapes are blendshapes driven by audio
- [[concepts/facs]] — FACS AUs underlie viseme shape construction
- [[concepts/arkit-blendshapes]] — ARKit 52-weight space includes viseme-relevant shapes
- [[concepts/facial-blendshape-rigs]] — production rigs include viseme blendshape sets

## External Sources

- Melinda Ozel, *Viseme & Speech Reference Guide* — https://melindaozel.com/viseme-speech-guide/ (premium)
- Melinda Ozel, *Viseme Cheat Sheet* — https://melindaozel.com/viseme-cheat-sheet/ (free)
