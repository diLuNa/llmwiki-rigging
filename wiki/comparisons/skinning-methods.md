---
title: "Skinning Methods — Comparison"
---

## Overview
Comparison of skinning algorithms along key axes.

| Method | Candy-wrapper | Bulging | Non-rigid | GPU | Artist control |
|--------|--------------|---------|-----------|-----|----------------|
| LBS | ❌ severe | ✅ none | ❌ | ✅ fast | ✅ weights |
| DQS | ✅ fixed | ⚠️ mild | ❌ | ✅ fast | ✅ weights |
| Implicit/volumetric | ✅ | ✅ | ⚠️ partial | ⚠️ moderate | ⚠️ complex |
| Neural | ✅ | ✅ | ✅ | ✅ (inference) | ❌ opaque |

## Analysis
For production characters with moderate pose range: **DQS** is the pragmatic choice. Add corrective shapes (PSD) for anatomical accuracy. Neural methods are promising but not yet art-directable.

## Key Papers
- [[papers/kavan-2007-dqs]]
- [[papers/jacobson-2011-bbw]]
