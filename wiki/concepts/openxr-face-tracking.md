---
title: "OpenXR Face Tracking Extensions"
tags: [blendshapes, facial-capture, facs, digital-human, real-time]
---

## Definition

**OpenXR** is the open, royalty-free API standard for XR (VR/AR/MR) application development, governed by the **Khronos Group** (same consortium as OpenGL, Vulkan, glTF). OpenXR decouples XR applications from vendor-specific runtimes; a single OpenXR app runs on Meta Quest, HTC Vive, Valve Index, and other compliant headsets without modification.

**Face tracking** in OpenXR is implemented via vendor extension layers on top of the core specification. Each vendor publishes a named extension (e.g., `XR_FB_face_tracking`, `XR_HTC_facial_tracking`) that exposes face expression weights through a consistent API pattern. All extensions return arrays of float weights in [0, 1] keyed by enum values, mirroring ARKit's coefficient model.

**Khronos OpenXR Registry:** [registry.khronos.org/OpenXR](https://registry.khronos.org/OpenXR/)  
**Full specification (1.1):** [registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html](https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html)

---

## Face Tracking Extensions

### XR_FB_face_tracking — Meta (70 weights)

The Meta/Facebook face tracking extension for Quest Pro and Quest 3 headsets. Outputs **70 FACS-derived blend shape weights** covering the full face.

**Extension name:** `XR_FB_face_tracking`  
**Revision:** Extended by `XR_FB_face_tracking2` (see below)

Key API:
```c
xrCreateFaceTrackerFB(session, &createInfo, &faceTracker);
xrGetFaceExpressionWeightsFB(faceTracker, &expressionInfo, &expressionWeights);
// expressionWeights.weights → float[XR_FACE_EXPRESSION_COUNT_FB]  (70 values)
// expressionWeights.confidences → upper_face + lower_face confidence [0,1]
```

**Weight regions (70 total):** Brows, eyes (blink, squint, wide, look), nose, cheeks, mouth corners, lips (funnel, pucker, roll, shrug, press, stretch), jaw (drop, sideways), chin.

**FACS coverage:** Superset of ARKit 52 — includes additional expression granularity (more AU decomposition, micro-expression weights) beyond what ARKit exposes.

**Official docs:**  
→ [xrGetFaceExpressionWeightsFB](https://registry.khronos.org/OpenXR/specs/1.0/man/html/xrGetFaceExpressionWeightsFB.html)  
→ [XrSystemFaceTrackingPropertiesFB](https://registry.khronos.org/OpenXR/specs/1.0/man/html/XrSystemFaceTrackingPropertiesFB.html)  
→ [Meta Developer: Face Tracking (Native)](https://developers.meta.com/horizon/documentation/native/android/move-face-tracking/)

---

### XR_FB_face_tracking2 — Meta (enhanced, multimodal)

An extended version of `XR_FB_face_tracking` that adds **multimodal input** support (visual + audio).

Key addition: `xrGetFaceExpressionWeights2FB` — returns the same 70 weights but with explicit source flags indicating whether the data is visually tracked, audio-inferred (lip sync from microphone), or both. Useful for lip animation continuity when the face is occluded.

**Official docs:**  
→ [XrFaceExpression2FB](https://registry.khronos.org/OpenXR/specs/1.0/man/html/XrFaceExpression2FB.html)  
→ [XrSystemFaceTrackingProperties2FB](https://registry.khronos.org/OpenXR/specs/1.1/man/html/XrSystemFaceTrackingProperties2FB.html)

---

### XR_HTC_facial_tracking — HTC (37 + 52 weights)

HTC's extension for Vive XR Elite and Vive Focus 3 with VIVE Full Face Tracker accessory. Splits tracking into two independently queryable subsets:

| Subset | Count | Coverage |
|--------|-------|----------|
| Eye expressions | 37 | Blink L/R, gaze direction (left/right/up/down), squint, wide, openness, pupil dilation |
| Lip expressions | 52 | **Directly ARKit-compatible names and semantics** |

The 52-weight lip component is deliberately designed to match ARKit blend shape semantics, enabling a single character rig to be driven identically by either an iPhone (ARKit) or an HTC headset (OpenXR) without remapping.

Key API:
```c
xrCreateFacialTrackerHTC(session, &createInfo, &facialTracker);
// createInfo.facialTrackingType = XR_FACIAL_TRACKING_TYPE_EYE_DEFAULT_HTC
//                               or XR_FACIAL_TRACKING_TYPE_LIP_DEFAULT_HTC
xrGetFacialExpressionsHTC(facialTracker, &facialExpressions);
// facialExpressions.weights → float[37] or float[52]
```

**Official docs:**  
→ [xrGetFacialExpressionsHTC](https://registry.khronos.org/OpenXR/specs/1.0/man/html/xrGetFacialExpressionsHTC.html)  
→ [HTC Developer: Integrate with MetaHuman (Unreal)](https://developer.vive.com/resources/openxr/openxr-pcvr/tutorials/unreal-engine/integrate-vive-openxr-facial-tracking-metahuman/)  
→ [HTC Developer: Face Data (Unity)](https://developer.vive.com/resources/openxr/unity/tutorials/face-data/getting-data-of-facial-tracking/)

---

### XR_EXT_eye_gaze_interaction — Cross-vendor (gaze direction)

Core OpenXR extension for **eye gaze direction** (not expression weights). Provides the eye's optical axis as a pose action, used for foveated rendering, UI interaction, and avatar gaze targeting. Not a facial expression extension.

```c
// Exposes eye gaze as an XrAction (pose type) — direction only, no weights
XrSystemEyeGazeInteractionPropertiesEXT.supportsEyeGazeInteraction
```

**Official docs:**  
→ [XR_EXT_eye_gaze_interaction](https://registry.khronos.org/OpenXR/specs/1.0/man/html/XR_EXT_eye_gaze_interaction.html)  
→ [Unity OpenXR: Eye Gaze Interaction](https://docs.unity3d.com/Packages/com.unity.xr.openxr@1.15/manual/features/eyegazeinteraction.html)

---

## Weight Count Comparison

| Standard | Count | Basis | Device / Source |
|----------|-------|-------|-----------------|
| FACS | 44 AUs | Anatomical muscles | Reference taxonomy |
| ARKit | 52 | FACS-derived | iPhone / iPad TrueDepth |
| XR_FB_face_tracking | 70 | Extended FACS | Meta Quest Pro, Quest 3 |
| XR_HTC_facial_tracking (eyes) | 37 | Precision eye | VIVE XR Elite + tracker |
| XR_HTC_facial_tracking (lips) | 52 | **ARKit-compatible** | VIVE XR Elite + tracker |
| MPEG-4 FAPs | 68 | Model-based | Legacy standard |

**Key observation:** HTC's 52-weight lip set is ARKit-compatible. A character rig using ARKit-named blendshapes is natively drivable from HTC hardware without any remapping layer.

---

## Cross-Platform Rigging Strategy

The practical implication for rig design:

```
Design target: 52 ARKit-named blendshapes (core rig)

Driver A: iPhone ARKit           → 52 weights → direct mapping
Driver B: HTC XR_HTC lip (52)   → 52 weights → direct mapping
Driver C: Meta XR_FB (70)       → 70 weights → 52-subset mapping + 18 extra
Driver D: Eye gaze (XR_EXT)     → pose action → eye rotation joints
```

A production character rigged to the 52 ARKit names can be driven across all current XR platforms with no structural rig changes. Engine plugins (Unreal, Unity) handle the extension-to-name remapping at runtime.

---

## Engine Integration

### Unreal Engine

**HTC + MetaHuman:**
→ [VIVE OpenXR Facial Tracking with MetaHuman](https://developer.vive.com/resources/openxr/openxr-pcvr/tutorials/unreal-engine/integrate-vive-openxr-facial-tracking-metahuman/)

**Meta Movement SDK (Unreal):**
→ [Movement SDK for Unreal](https://developers.meta.com/horizon/documentation/unreal/unreal-movement-overview/)

OpenXR face tracking is exposed through Unreal's XR subsystem; Live Link receives the weights and routes them to Animation Blueprints — same blueprint setup as Live Link Face (ARKit), just with a different source plugin.

### Unity

**Meta Movement SDK (Unity):**
→ [Face Tracking for Movement SDK](https://developers.meta.com/horizon/documentation/unity/move-face-tracking/)  
→ [Unity-Movement GitHub samples](https://github.com/oculus-samples/Unity-Movement)

**HTC OpenXR (Unity):**
→ [Getting Data of Facial Tracking](https://developer.vive.com/resources/openxr/unity/tutorials/face-data/getting-data-of-facial-tracking/)

**Android XR (Unity OpenXR):**
→ [Face tracking — Android XR 1.1](https://docs.unity3d.com/Packages/com.unity.xr.androidxr-openxr@1.1/manual/features/faces.html)

In Unity, face weights stream into a `SkinnedMeshRenderer`'s blendShape weights array. The plugin maps extension enum indices to Unity blendshape names — if the rig uses ARKit-named blendshapes, HTC's plugin maps directly.

---

## Relationship to Production Rigs

### Why 52 weights has become the standard

1. Apple shipped TrueDepth on iPhone X (2017) — widespread accessible hardware
2. Unreal's Live Link Face (2020) cemented the 52-name standard in virtual production
3. Epic's MetaHuman uses ARKit names as its streaming-layer target
4. HTC explicitly adopted ARKit compatibility in their OpenXR extension (2023)
5. Result: any rig built to ARKit names is cross-platform without modification

### Meta's 70-weight extension

Meta's extra 18 weights beyond ARKit's 52 cover:
- Additional jaw lateral movements
- Cheek puff (bilateral separate, vs ARKit's combined `cheekPuff`)
- More granular lip shapes (separate inner/outer lip components)
- Brow raise/lower with more intermediate positions

For production rigs targeting Quest Pro, these 18 weights can drive corrective shapes on top of the core 52, or they can be remapped to custom controls. Most studios ignore them and use only the ARKit-compatible 52 for cross-platform portability.

---

## Connections

- [[concepts/facs]] — FACS Action Units are the anatomical foundation all extensions derive from
- [[concepts/arkit-blendshapes]] — ARKit's 52-weight standard is the baseline all XR extensions relate to
- [[concepts/facial-blendshape-rigs]] — production rigs targeting these streaming standards
- [[papers/epic-2021-metahuman-rig]] — MetaHuman's 52-name ARKit streaming layer
- [[papers/ekman-friesen-1978-facs]] — original AU taxonomy underlying all these formats

## External Resources

| Resource | URL |
|----------|-----|
| Khronos OpenXR Registry | [registry.khronos.org/OpenXR](https://registry.khronos.org/OpenXR/) |
| OpenXR 1.1 Full Specification | [registry.khronos.org/OpenXR/specs/1.1](https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html) |
| XR_FB_face_tracking reference | [registry.khronos.org (man page)](https://registry.khronos.org/OpenXR/specs/1.0/man/html/xrGetFaceExpressionWeightsFB.html) |
| XR_HTC_facial_tracking reference | [registry.khronos.org (man page)](https://registry.khronos.org/OpenXR/specs/1.0/man/html/xrGetFacialExpressionsHTC.html) |
| Meta Face Tracking (Native) | [developers.meta.com](https://developers.meta.com/horizon/documentation/native/android/move-face-tracking/) |
| Meta Movement SDK (Unity) | [developers.meta.com](https://developers.meta.com/horizon/documentation/unity/move-face-tracking/) |
| Unity-Movement GitHub | [github.com/oculus-samples/Unity-Movement](https://github.com/oculus-samples/Unity-Movement) |
| HTC: MetaHuman + OpenXR (Unreal) | [developer.vive.com](https://developer.vive.com/resources/openxr/openxr-pcvr/tutorials/unreal-engine/integrate-vive-openxr-facial-tracking-metahuman/) |
| HTC: Face Data (Unity) | [developer.vive.com](https://developer.vive.com/resources/openxr/unity/tutorials/face-data/getting-data-of-facial-tracking/) |
| XR_EXT_eye_gaze_interaction | [registry.khronos.org (man page)](https://registry.khronos.org/OpenXR/specs/1.0/man/html/XR_EXT_eye_gaze_interaction.html) |
| OpenXR GitHub (SDK + Docs) | [github.com/KhronosGroup/OpenXR-SDK](https://github.com/KhronosGroup/OpenXR-SDK) |
