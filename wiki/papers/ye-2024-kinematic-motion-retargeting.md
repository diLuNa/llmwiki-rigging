---
title: "Kinematic Motion Retargeting for Contact-Rich Anthropomorphic Manipulations"
authors: [Ye, Yuting; Yang, Lanyao; Xu, Jiawei; He, Jing; Deng, Yue; Xu, Weiwei]
venue: ACM Transactions on Graphics
year: 2024
tags: [motion-retargeting, hand-animation, contact-modeling, inverse-kinematics, manipulation]
source: TBA
doi: 10.1145/3723872
---

## Summary
Framework for retargeting hand-object manipulations across diverse target hands leveraging contact areas as retargeting medium. Formulates problem as nonisometric shape matching using dense correspondences between contact regions. Enables transfer of complex anthropomorphic grasping and manipulation motions.

## Problem
Retargeting hand manipulations across different hand morphologies is challenging due to contact constraints and varying kinematic structure. Existing methods don't explicitly preserve contact relationships which are critical for manipulation fidelity.

## Method
- **Contact-based retargeting**: Dense correspondences between contact distributions as primary medium
- **Nonisometric shape matching**: Handles varying hand sizes and proportions
- **Inverse kinematics**: Solves for target hand joint angles maintaining contact
- **Temporal optimization**: Ensures smooth contact transitions and trajectory continuity

## Key Results
- Accurate retargeting of complex hand manipulations across morphologies
- Preserves contact forces and grasp stability
- High-quality results suitable for downstream physics controllers
- Real-time retargeting with predictive sampling

## Limitations
- Requires accurate contact detection in source motion
- Complex multi-contact interactions challenging to retarget
- Assumes similar hand topology and capabilities
- Performance depends on source motion quality

## Connections
- [[papers/jain-2010-hand-secondary]] — hand modeling and deformation
- [[papers/cao-2024-multimodal-grasp]] — multi-modal grasp learning
- [[concepts/hand-animation]] — dexterous hand control
- [[papers/holden-2015-inverse-rig]] — inverse kinematics for character control
- [[concepts/secondary-motion]] — enriching manipulation motions

## Implementation Notes
- Contact distribution representation critical for stability
- Dense correspondence enables fine-grained control transfer
- Compatible with physics-based hand controllers
- Preprocessing steps for motion cleaning improve results

## External References
- ACM DL: [doi.org/10.1145/3723872](https://doi.org/10.1145/3723872)
