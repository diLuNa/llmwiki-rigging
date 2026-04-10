---
title: "ARKit Blend Shapes — Apple Face Tracking Standard"
tags: [blendshapes, facial-capture, facs, digital-human, real-time, rig-generation]
---

## Definition

**ARKit Face Tracking** is Apple's real-time facial animation system, available on iPhones and iPads equipped with a TrueDepth camera (Face ID hardware, iPhone X onwards). It exposes **52 named blend shape coefficients** (weights ∈ [0, 1]) updated at 60 fps, plus a coarse 1,220-vertex face mesh and 6-DOF head pose. The 52-weight parameterization has become the **de facto interchange standard** for real-time facial animation across game engines, XR platforms, and virtual production pipelines.

**Canonical reference:** Apple developer documentation — [ARFaceAnchor.BlendShapeLocation](https://developer.apple.com/documentation/arkit/arfaceanchor/blendshapelocation)

---

## Technical Architecture

### Hardware

- **TrueDepth camera system**: infrared dot projector (30,000 dots), infrared camera, flood illuminator
- **Depth resolution**: 1,220-point 3D face mesh at 60 Hz
- **Processing**: Apple Neural Engine (on-device); no cloud dependency
- **Minimum hardware**: iPhone X / iPad Pro 2018+; iPhone 12+ recommended for MetaHuman Animator

### Data Pipeline

```
TrueDepth camera → depth + IR frames
    ↓
ARKit Neural Face Model (on-device)
    ↓
ARFaceAnchor (per frame, 60 Hz):
    ├── blendShapes   [52 × Float, 0–1]    ← expression weights
    ├── geometry      ARFaceGeometry         ← 1,220-pt mesh
    └── transform     simd_float4x4          ← head pose (6-DOF)
```

### ARFaceGeometry

| Field | Type | Description |
|-------|------|-------------|
| `vertices` | Float3 buffer | 1,220 3D point positions |
| `triangleIndices` | UInt16 buffer | ~2,300 triangles (mesh topology) |
| `textureCoordinates` | Float2 buffer | UV mapping per vertex |

ARFaceGeometry updates every frame and deforms with the actor's face. It can drive a geometric mesh rig directly (vertex deformation approach) or be used only for pose estimation while blendshape weights drive the rig parametrically.

Official ref: [ARFaceGeometry](https://developer.apple.com/documentation/arkit/arfacegeometry)

---

## The 52 Blend Shape Names

Grouped by facial region. All names are `lowerCamelCase`; bilateral shapes have `Left`/`Right` suffixes.

### Eyes (14)
```
eyeBlinkLeft        eyeBlinkRight
eyeLookDownLeft     eyeLookDownRight
eyeLookInLeft       eyeLookInRight
eyeLookOutLeft      eyeLookOutRight
eyeLookUpLeft       eyeLookUpRight
eyeSquintLeft       eyeSquintRight
eyeWideLeft         eyeWideRight
```

### Brows (6)
```
browDownLeft        browDownRight
browInnerUp
browOuterUpLeft     browOuterUpRight
```

### Nose (2)
```
noseSneerLeft       noseSneerRight
```

### Jaw (4)
```
jawForward
jawLeft             jawRight
jawOpen
```

### Mouth / Lips (24)
```
mouthClose
mouthDimpleLeft     mouthDimpleRight
mouthFrownLeft      mouthFrownRight
mouthFunnel
mouthLeft           mouthRight
mouthLowerDownLeft  mouthLowerDownRight
mouthPressLeft      mouthPressRight
mouthPucker
mouthRollLower      mouthRollUpper
mouthShrugLower     mouthShrugUpper
mouthSmileLeft      mouthSmileRight
mouthStretchLeft    mouthStretchRight
mouthUpperUpLeft    mouthUpperUpRight
```

### Cheeks (2)
```
cheekPuff
cheekSquintLeft     cheekSquintRight
```

**Total: 52** — including `cheekSquintLeft` and `cheekSquintRight`, bringing cheeks to 3 entries (cheekPuff is singular/bilateral).

---

## ARKit → FACS Mapping

ARKit blend shapes do not map 1:1 to FACS Action Units. Key differences:
- ARKit splits most bilateral AUs into `Left`/`Right` (e.g., `mouthSmileLeft` = AU12L)
- Some FACS AUs are not represented (e.g., AU11 nasolabial deepener)
- Some ARKit shapes are functional rather than anatomical (e.g., `jawForward` maps to AU28 approximately)
- ARKit uses descriptive English names, not AU numbers

**Canonical mapping resource:** Melinda Ozel  
→ [ARKit to FACS Cheat Sheet](https://melindaozel.com/arkit-to-facs-cheat-sheet/)  
→ [ARKit to FACS Translation Guide](https://melindaozel.com/arkit-to-facs-translation-guide/)

Key spot mappings (partial):

| ARKit Name | FACS AU | FACS Name |
|-----------|---------|-----------|
| `browInnerUp` | AU1 | Inner Brow Raise |
| `browOuterUpLeft/Right` | AU2 L/R | Outer Brow Raise |
| `browDownLeft/Right` | AU4 L/R | Brow Lowerer |
| `eyeWideLeft/Right` | AU5 L/R | Upper Lid Raiser |
| `cheekSquintLeft/Right` | AU6 L/R | Cheek Raiser |
| `eyeSquintLeft/Right` | AU7 L/R | Lid Tightener |
| `noseSneerLeft/Right` | AU9 L/R | Nose Wrinkler |
| `mouthSmileLeft/Right` | AU12 L/R | Lip Corner Puller |
| `mouthDimpleLeft/Right` | AU14 L/R | Dimpler |
| `mouthFrownLeft/Right` | AU15 L/R | Lip Corner Depressor |
| `mouthStretchLeft/Right` | AU20 L/R | Lip Stretcher |
| `mouthFunnel` | AU22 | Lip Funneler |
| `mouthPucker` | AU18 | Lip Puckerer |
| `mouthClose` | AU23/24 | Lip Tightener / Pressor |
| `jawOpen` | AU26/27 | Jaw Drop / Mouth Stretch |

See [[concepts/facs]] for the full AU reference.

---

## Engine Integration

### Unreal Engine — Live Link Face

**Live Link Face** (free iOS app from Epic) streams all 52 ARKit weights + head pose + timecode over Wi-Fi to Unreal Engine in real time.

Pipeline:
```
iPhone → Live Link Face app → Wi-Fi (UDP) → Live Link plugin → Unreal Animation Blueprint
```

- Real-time preview on MetaHuman characters
- Simultaneous CSV export (raw weights) and MOV video reference with timecode stripe
- Tentacle Sync integration for multi-actor synchronization
- Timecode-accurate alignment with body mocap and camera data

Documentation:  
→ [Recording Face Animation on iOS Device](https://dev.epicgames.com/documentation/en-us/unreal-engine/recording-face-animation-on-ios-device-in-unreal-engine)  
→ [Live Link Face app (App Store)](https://apps.apple.com/us/app/live-link-face/id1495370836)

### Unity — AR Foundation

- ARFoundation package provides `ARFaceManager` component
- `ARKitBlendShapeCoefficient` streams 52 weights per frame
- Weights drive `SkinnedMeshRenderer` blend shapes directly
- Platform: iOS/iPadOS with Face ID camera

Documentation:  
→ [AR Foundation Face Tracking](https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@6.2/manual/samples/features/face-tracking.html)  
→ [Apple ARKit XR Plugin Face Tracking](https://docs.unity3d.com/Packages/com.unity.xr.arkit@6.0/manual/arkit-face-tracking.html)

---

## MetaHuman ↔ ARKit

MetaHuman Creator (Epic) exposes two layers:

| Layer | Count | Use |
|-------|-------|-----|
| ARKit-compatible layer | 52 | Live Link Face streaming target |
| Full DNA rig | 258–669 blendshapes + 397–713 joints | Cinematic polish |

The 52-name ARKit layer maps directly to the Live Link Face stream. Custom characters can be configured with ARKit-named curves for the same streaming workflow without using MetaHuman topology.

Documentation:  
→ [Head Blend Controls (MetaHuman)](https://dev.epicgames.com/documentation/en-us/metahuman/head-blend-controls)  
→ [MetaHuman Animator](https://www.metahuman.com/en-US/news/delivering-high-quality-facial-animation-in-minutes-metahuman-animator-is-now-available)

---

## As a Research Data Source

ARKit's accessibility (any modern iPhone) has made it the dominant data collection tool in academic facial animation research:

- **SAiD (2024)**: speech-driven blendshape diffusion; uses 32 ARKit weights as output space
- **UniTalker (2024)**: unified audio-driven 3D face animation; ARKit 52 coefficients as training target
- **REFA (2025)**: real-time egocentric VR facial animation; ARKit as tracking input
- **Express4D**: 4D facial motion benchmark; dataset collected via iPhone TrueDepth
- **KeyframeFace (2024)**: language-driven ARKit animation via LLM-generated keyframes

The 52-weight space's accessibility and standardization makes it a natural annotation format for datasets — see [[concepts/nonlinear-face-models]] for models trained on such data.

---

## Standardization Position

| Standard | Count | Basis | Adoption |
|----------|-------|-------|----------|
| FACS (Ekman 1978) | 44 AUs | Anatomical | Academic reference |
| ARKit (Apple, 2017) | 52 | FACS-derived | **De facto real-time standard** |
| MetaHuman ARKit layer | 52 | ARKit-named | Virtual production |
| HTC OpenXR 52-weight | 52 | ARKit-compatible | XR headsets |
| Meta OpenXR 70-weight | 70 | Extended FACS | Quest Pro headsets |
| MPEG-4 FAPs | 68 | Model-based | Legacy, declining |

See [[concepts/openxr-face-tracking]] for the XR headset extension ecosystem.

---

## Connections

- [[concepts/facs]] — FACS Action Units are the anatomical foundation ARKit blend shapes derive from
- [[concepts/openxr-face-tracking]] — OpenXR extensions extend ARKit's 52 baseline for XR headsets
- [[concepts/facial-blendshape-rigs]] — ARKit weights drive production blendshape rigs
- [[concepts/nonlinear-face-models]] — many neural face models output or train on ARKit weight spaces
- [[papers/epic-2021-metahuman-rig]] — MetaHuman's ARKit streaming layer
- [[papers/ekman-friesen-1978-facs]] — FACS source taxonomy
- [[papers/qin-2023-nfr]] — NFR uses ICT FaceKit (FACS-inspired, similar to ARKit) as supervision

## External Resources

| Resource | URL |
|----------|-----|
| ARFaceAnchor.BlendShapeLocation (official) | [developer.apple.com](https://developer.apple.com/documentation/arkit/arfaceanchor/blendshapelocation) |
| ARFaceGeometry (official) | [developer.apple.com](https://developer.apple.com/documentation/arkit/arfacegeometry) |
| ARKit Face Tracking guide | [developer.apple.com](https://developer.apple.com/documentation/ARKit/tracking-and-visualizing-faces) |
| ARKit → FACS mapping (Melinda Ozel) | [melindaozel.com](https://melindaozel.com/arkit-to-facs-cheat-sheet/) |
| Community blend shape reference | [arkit-face-blendshapes.com](https://arkit-face-blendshapes.com/) |
| Live Link Face (Unreal) | [dev.epicgames.com](https://dev.epicgames.com/documentation/en-us/unreal-engine/recording-face-animation-on-ios-device-in-unreal-engine) |
| MetaHuman Head Blend Controls | [dev.epicgames.com](https://dev.epicgames.com/documentation/en-us/metahuman/head-blend-controls) |
| AR Foundation (Unity) | [docs.unity3d.com](https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@6.2/manual/samples/features/face-tracking.html) |
