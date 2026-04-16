---
title: "Unified Expressions — Cross-Platform Face Tracking Standard"
tags: [blendshapes, facial-capture, facs, digital-human, real-time]
---

## Definition

**Unified Expressions** is an open-source, platform-neutral face expression vocabulary developed by the **VRCFaceTracking** project. It provides a single canonical set of expression names that can be driven by any face tracking hardware (iPhone ARKit, Meta Quest Pro, HTC VIVE Full Face Tracker, Magic Leap 2, etc.) through transformation passes. Designed to free avatar rigs from hardware-specific naming conventions.

→ [Official documentation](https://docs.vrcft.io/docs/tutorial-avatars/tutorial-avatars-extras/unified-blendshapes)  
→ [VRCFaceTracking GitHub](https://github.com/benaclejames/VRCFaceTracking)

---

## Motivation

Each face tracking standard uses different names and counts:
- ARKit: 52 shapes, `lowerCamelCase`, Apple-derived
- Meta `XR_FB_face_tracking2`: 70 shapes, `SCREAMING_SNAKE_CASE`, FACS-derived
- HTC `XR_HTC_facial_tracking`: 37 + 52 shapes, split eye/lip
- SRanipal (legacy HTC SDK): different naming again

Without an interop layer, avatar rigs must be duplicated for each platform. Unified Expressions solves this with a **single rig target** that all hardware drivers translate into.

---

## Shape Set

### Base Shapes (~100)

Organized by region:

| Region | Examples |
|--------|---------|
| Eyes (look) | `EyeLookUpRight/Left`, `EyeLookDownRight/Left`, `EyeLookInRight/Left`, `EyeLookOutRight/Left` |
| Eyelids | `EyeClosedRight/Left`, `EyeSquintRight/Left`, `EyeWideRight/Left` |
| Eye extras | `EyeDilationRight/Left`, `EyeConstrictRight/Left` |
| Brows | `BrowDownRight/Left`, `BrowInnerUp`, `BrowOuterUpRight/Left`, `BrowPinchRight/Left`, `BrowLowererRight/Left` |
| Nose | `NoseSneerRight/Left`, `NoseDilationRight/Left`, `NoseConstrictRight/Left` |
| Cheeks | `CheekSquintRight/Left`, `CheekPuffRight/Left`, `CheekSuckRight/Left` |
| Jaw | `JawOpen`, `JawForward`, `JawRight`, `JawLeft`, `JawBackward`, `JawClench`, `JawMandibleRaise` |
| Lips (inner) | `LipSuckUpper`, `LipSuckLower`, `LipFunnel`, `LipPucker` |
| Mouth | `MouthClosed`, `MouthUpperUpRight/Left`, `MouthLowerDownRight/Left`, `MouthSmileRight/Left`, `MouthFrownRight/Left`, `MouthStretchRight/Left`, `MouthDimpleRight/Left`, `MouthRaiserUpper/Lower`, `MouthPressRight/Left`, `MouthLeft`, `MouthRight` |
| Tongue | `TongueOut`, `TongueCurlUp/Down`, `TongueSquish`, `TongueFlat`, `TongueTwistRight/Left`, `TongueBulgeRight/Left`, `TongueUp/Down/Right/Left` |
| Throat | `ThroatSwallow`, `NeckFlexRight/Left` |

### Blended Shapes (~45)

Simplified compound shapes synthesized from base shapes for simpler rig setup. Examples:
- `EyeClosed` (combines L+R)
- `BrowUp` (combines all brow raiser shapes)
- `MouthSmile`, `MouthSad`

---

## ARKit ↔ Unified Expressions Mapping

All 52 ARKit shapes have a direct Unified Expressions equivalent. The mapping is 1:1 for 47 shapes and near-1:1 for the remaining 5 (functional equivalent, slightly different semantic scope).

| ARKit Name | Unified Expression |
|-----------|-------------------|
| `eyeBlinkRight` | `EyeClosedRight` |
| `eyeBlinkLeft` | `EyeClosedLeft` |
| `eyeSquintRight` | `EyeSquintRight` |
| `eyeSquintLeft` | `EyeSquintLeft` |
| `eyeWideRight` | `EyeWideRight` |
| `eyeWideLeft` | `EyeWideLeft` |
| `eyeLookUpRight` | `EyeLookUpRight` |
| `eyeLookDownRight` | `EyeLookDownRight` |
| `eyeLookInRight` | `EyeLookInRight` |
| `eyeLookOutRight` | `EyeLookOutRight` |
| `eyeLookUpLeft` | `EyeLookUpLeft` |
| `eyeLookDownLeft` | `EyeLookDownLeft` |
| `eyeLookInLeft` | `EyeLookInLeft` |
| `eyeLookOutLeft` | `EyeLookOutLeft` |
| `browDownRight` | `BrowDownRight` |
| `browDownLeft` | `BrowDownLeft` |
| `browInnerUp` | `BrowInnerUp` |
| `browOuterUpRight` | `BrowOuterUpRight` |
| `browOuterUpLeft` | `BrowOuterUpLeft` |
| `noseSneerRight` | `NoseSneerRight` |
| `noseSneerLeft` | `NoseSneerLeft` |
| `cheekSquintRight` | `CheekSquintRight` |
| `cheekSquintLeft` | `CheekSquintLeft` |
| `cheekPuff` | `CheekPuffRight` + `CheekPuffLeft` *(split)* |
| `jawOpen` | `JawOpen` |
| `jawRight` | `JawRight` |
| `jawLeft` | `JawLeft` |
| `jawForward` | `JawForward` |
| `mouthClose` | `MouthClosed` |
| `mouthFunnel` | `LipFunnel` |
| `mouthPucker` | `LipPucker` |
| `mouthRollUpper` | `LipSuckUpper` |
| `mouthRollLower` | `LipSuckLower` |
| `mouthShrugUpper` | `MouthRaiserUpper` |
| `mouthShrugLower` | `MouthRaiserLower` |
| `mouthUpperUpRight` | `MouthUpperUpRight` |
| `mouthUpperUpLeft` | `MouthUpperUpLeft` |
| `mouthLowerDownRight` | `MouthLowerDownRight` |
| `mouthLowerDownLeft` | `MouthLowerDownLeft` |
| `mouthSmileRight` | `MouthSmileRight` |
| `mouthSmileLeft` | `MouthSmileLeft` |
| `mouthFrownRight` | `MouthFrownRight` |
| `mouthFrownLeft` | `MouthFrownLeft` |
| `mouthStretchRight` | `MouthStretchRight` |
| `mouthStretchLeft` | `MouthStretchLeft` |
| `mouthDimpleRight` | `MouthDimpleRight` |
| `mouthDimpleLeft` | `MouthDimpleLeft` |
| `mouthPressRight` | `MouthPressRight` |
| `mouthPressLeft` | `MouthPressLeft` |
| `mouthLeft` | `MouthLeft` |
| `mouthRight` | `MouthRight` |
| `tongueOut` | `TongueOut` |

**Notable differences:**
- `cheekPuff` (ARKit bilateral) → splits into `CheekPuffRight` + `CheekPuffLeft` in Unified
- Unified adds eye dilation, throat, extended tongue that ARKit doesn't expose
- Unified adds `BrowPinch` and `BrowLowerer` that map to Meta OpenXR `BROW_LOWERER_L/R` instead

---

## Driver Support

| Hardware | Extension | Translation Available |
|----------|-----------|----------------------|
| iPhone / iPad | ARKit TrueDepth | Direct — 52 shapes map 1:1 |
| Meta Quest Pro | `XR_FB_face_tracking2` | 70→Unified via module |
| HTC VIVE + Face Tracker | `XR_HTC_facial_tracking` (SRanipal) | SRanipal→Unified module |
| Magic Leap 2 | `XR_ML_facial_expression` | ML→Unified module |
| Android XR | ARCore Jetpack XR | 68→Unified (partial) |

Each driver is an installable VRCFaceTracking module — the avatar rig itself never changes.

---

## ARKit vs Unified: Practical Considerations

| Criterion | ARKit Names | Unified Expressions |
|-----------|------------|-------------------|
| Coverage | 52 weights | ~100 base + ~45 blended |
| Bilateral cheek puff | Combined `cheekPuff` | Separate L/R |
| Tongue | 1 shape (`tongueOut`) | 10+ shapes |
| Eye dilation | Not present | `EyeDilationR/L` |
| Platform support | iOS/iPadOS only | All XR platforms via modules |
| Production adoption | **Dominant** (MetaHuman, Unreal Live Link) | Growing (VR/XR community) |
| Research adoption | **Dominant** (dataset target) | Emerging |

---

## Notes

- Unified Expressions is maintained as open source; it is not a Khronos or IEEE standard
- The convention is widely adopted in the **VTubing** and **VRChat** communities, less so in film/VFX production (which still uses ARKit or proprietary)
- Steam Workshop plugin translates ARKit to Unified Expressions for real-time VRChat use
- The `CheekPuff` split (ARKit bilateral → UE bilateral) means a character rig built around ARKit needs one corrective if driven through Unified

---

## Connections

- [[concepts/arkit-blendshapes]] — the 52 ARKit weights that form the foundation of the Unified mapping
- [[concepts/openxr-face-tracking]] — OpenXR vendor extensions that Unified Expressions translates
- [[concepts/facs]] — underlying anatomical reference system
- [[concepts/facial-blendshape-rigs]] — production rigs these standards drive

## External Resources

| Resource | URL |
|----------|-----|
| Unified Expressions docs | [docs.vrcft.io](https://docs.vrcft.io/docs/tutorial-avatars/tutorial-avatars-extras/unified-blendshapes) |
| VRCFaceTracking GitHub | [github.com/benaclejames/VRCFaceTracking](https://github.com/benaclejames/VRCFaceTracking) |
| ARKit-to-Unified Steam plugin | [steamcommunity.com](https://steamcommunity.com/sharedfiles/filedetails/?id=3591848415) |
| Blendshape convention converter (Haï) | [docs.hai-vr.dev](https://docs.hai-vr.dev/docs/products/prefabulous/universal/convert-blendshape-conventions) |
