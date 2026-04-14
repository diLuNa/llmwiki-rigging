---
title: "MIRRORED-Anims: Motion Inversion for Rig-space Retargeting to Obtain a Reliable Enlarged Dataset of Character Animations | Proceedings of the 2025 18th ACM SIGGRAPH Conference on Motion, Interaction, and Games"
source: "https://dl.acm.org/doi/10.1145/3769047.3769064"
author:
published:
created: 2026-04-14
description:
tags:
  - "clippings"
---
## Abstract

### Abstract

We propose MIRRORED-Anims, a novel retargeting procedure for transferring motion between skinned humanoid characters of different morphologies. It is designed so as to mimic the strengths of the closed-source Mixamo’s retargeting method, currently used as a standard to create motion databases and train all state-of-the-art learning-based retargeting methods, despite severe shortcomings (namely, a lack of character diversity and notable penetration artifacts). Taking inspiration from the toolsets of 3D animators, our retargeting algorithm relies on the control rigs used to manipulate skinned characters, by identifying and transferring controller values on predefined bone mechanisms. While producing motions which are closer to Mixamo’s ground truth than any state-of-the-art learning-based technique, MIRRORED-Anims creates fewer penetration artifacts than observed in the Mixamo dataset, improving the perceived quality of the output. Moreover, motion can be retargeted in real-time to and from the SMPL body model, making it possible to leverage the large motion databases available in SMPL format for the retargeting task. Because it relies solely on transparent, explainable rig operations, MIRRORED-Anims can be used to generate ground-truth motions for any humanoid character, providing a reliable baseline for the future training of learning-based methods. Project page: https://mirrored-anims.github.io/MIRRORED-Anims

### AI Summary

To view this AI-generated plain language summary, you must have Premium access.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/968843a5-dd1b-4714-9b5a-97f21d6d3697/assets/images/large/mig25-16-fig1.jpg)

MIRRORED-Anims allows to easily build a large-scale dataset of paired motions for a variety of humanoid characters. Given two skinned characters, our solution relies on the automatic creation of high-level control rigs to define a rig-space retargeting process. As shown above, it transfers feet and hand contacts without any sliding or floating behavior.

## 1 Introduction

The task of transferring motion from one animated 3D character to another, called “retargeting”, is a long-standing problem in the field of computer animation. Indeed, solving this highly challenging task requires understanding the influence that different bone lengths, skeletal structures, and body shapes may have on motion, in order to find the best compromise and generate a new movement that most perceptually resembles the input.

In an attempt to capture the implicit interplay of these different factors, recent advances relied on deep neural networks to learn the distribution of motions for each character using unsupervised learning, which then allows transferring motion between characters. To this end, NKN \[Villegas et al. [^31]\] introduced the “Mixamo” dataset, which consists in unpaired motions for a dozen different characters. The motions were collected using the Adobe Mixamo software \[Adobe [^2]\], which unfortunately relies on a closed-source algorithm for motion transfer. A family of later works \[Aberman et al. [^1]; Hu et al. [^15]; Lim et al. [^20]; Villegas et al. [^30]; Zhang et al. [2024a](#Bib0034); [^34]\] rely solely on this dataset to train neural networks for the task of motion retargeting.

Unfortunately, NKN’s “Mixamo” dataset is severely limited, for the following reasons:

- It includes a relatively small number of motions, when compared to academic motion-capture datasets;
- The “ground-truth” motions in the dataset show frequent artifacts, most notably penetrations into the ground (or lack of floor contacts), loss of semantic-rich contacts, and self-penetrations.

Moreover, we noticed that state-of-the-art methods fail to generalize to unseen characters from the test-set, which have different limb proportions. We claim that this failure is a direct consequence of the aforementioned limitations of the Mixamo dataset. While the field of retargeting would greatly benefit from a larger dataset, Mixamo’s retargeting method is entirely closed-source, only available through Adobe’s web platform, and subject to a prohibitive license that does not allow its direct use for machine learning.

To solve these issues, we propose a new, open-source retargeting method, named MIRRORED-Anims, aimed at providing a new baseline for motion retargeting tasks, which can be used to generate large quantities of data on virtually any character. We designed our method to:

- Accept any humanoid character as input, regardless of its morphology or the number of bones in the skeleton;
- Be explainable, so that it can rationally be trusted to generate new data for training purposes, with a minimal amount of data curation.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/829207dd-fc9d-40a4-a7ea-fce4c94e0596/assets/images/large/mig25-16-fig2.jpg)

The three steps of our the MIRRORED-Anims retargeting method. First, we automatically create a control rig for the source and target characters, using a modular template that we adapt to their skeleton and morphology. Then, for a given input animation, we perform motion inversion: that is, we find the rig controls that give the same animation. This allows us to perform a rig-based retargeting, with a collision resolution method to keep fine contact details with the torso.

To meet these goals, we draw inspiration from the way that 3D animation experts manually edit motions. In particular, we borrow one of the most widespread tools from their production pipelines: “control rigs”, which are interfaces that allow them to manipulate characters using a set of high-level controllers, instead of editing the pose of each bone separately. These control rigs are engineered by artists called “riggers”, to provide an appropriate set of controllers, based on the requirements of 3D animators. We asked a rigger to provide a control rig template adapted to our use case, and we propose a method to automatically build this control rig from any humanoid character. Moreover, we introduce a dedicated algorithm for “rig inversion”, allowing us to extract the control values from the input animation on the source character. We then propose a procedure for “skeleton-aware rig-space retargeting”, in which we compute a first version of the target character’s control values. Finally, we adapt the controller values by performing a morphology-based correction, to alleviate penetration artifacts. An overview of our method is shown in Figure [2](#fig2).

To assess the quality of the MIRRORED-Anims method, we provide a full analysis of quality of our results based on a series of metrics, a comparison with previous works, and generate a large dataset (shown in Figure [1](#fig1)) to train a learning-method, comparing it with the Mixamo dataset both quantitatively and qualitatively.

## 2 Previous Work

### 2.1 Optimization-based retargeting

Optimization-based motion retargeting was first introduced by Gleicher \[[^9]\], which frames the task as a space-time optimization problem, aiming to solve the target’s motion so that it respects some pre-identified constraints. Later, \[Lee and Shin [^18]\] refines the approach by solving frame-wise inverse kinematics (IK), and Choi and Ko \[[^6]\] adds joint-level constraints. Dynamic constraints are incorporated by Tak and Ko \[[^28]\] to enhance physical plausibility. There have been several extensions to skinned characters, with Jin et al. \[[^16]\] introducing the Aura Mesh for two interacting characters, and Basset et al. \[[^3]\] optimizing energy functions for volume preservation and collision handling. Ho et al. \[[^12]\] further addresses collision prevention using hard constraints. Recently, Cheynel et al. \[[^5]\] simplifies the mesh to a set of key-vertices to perform real-time optimization in order to address semantic contact conservation.

### 2.2 Kinematic retargeting

In the domain of virtual reality, real-time interactions are crucial. This is why some solutions in this field rely on purely kinematic approaches, that do not require computationally expensive optimization steps. These methods often model the relationship between the joints of the characters: Molla et al. \[[^23]\] uses egocentric coordinates and inverse kinematics, and Delahaye et al. \[[^8]\] adds finger retargeting in a real-time scenario. Qualitative evaluations from this neighbouring field seem to highlight that kinematic approaches offer promising results for our motion retargeting objective.

### 2.3 Learning-based retargeting

In contrast, most recent methods use a data-driven approach, training deep learning models to generate solutions to the retargeting problem. The first, seminal work was NKN \[Villegas et al. [^31]\], which initiates the use of the Mixamo dataset containing motions retargeted by Adobe Mixamo \[Adobe [^2]\] on a dozen characters. They argue that supervised learning is not possible, as acquiring paired motion data for source and target characters is very complex; instead, they train a recurrent neural network using a cycle consistency loss and a discriminator. PMNet \[Lim et al. [^20]\] later tries to decouple the pose and the overall movement (root trajectory). SAN \[Aberman et al. [^1]\] introduces convolution operations on skeletons, to allow the network to take diffeomorphic skeletons as input. Training an encoder/decoder architecture for each skeleton, with a shared latent space, allows them to perform retargeting without the need for ground-truth pairs of motion on different characters. SAME \[Lee et al. [^19]\] also trains an autoencoder to learn a skeleton-agnostic latent-space, performing retargeting amongst other tasks. PAN \[Hu et al. [^15]\] adopts a similar approach, but for each limb instead of treating the whole body at once, and Yan et al. \[[^32]\] applies a similar principle for human-to-robot retargeting.

In addition to skeletal information, a few methods also take into consideration the mesh of the character, in order to avoid inter-penetrations during motion while preserving accurate contacts. Villegas et al. \[[^30]\] identifies limb contacts on the source character, and enforced preservation of contacts using a geometry-informed RNN. R <sup>2</sup> ET \[Zhang et al. [2024b](#Bib0035); [^34]\] attenuates both self-collisions and missing contacts by integrating geometry processing inside their training losses, while MeshRet \[Ye et al. [^33]\] encode fine-grained mesh information for a more precise semantic correspondence of contacts. Even more recently, SMTNet \[Zhang et al. [2024a](#Bib0034)\] performs a differentiable rendering of the characters’ meshes, and uses a vision-language model to evaluate the conservation of motion semantics.

First, it is worth mentioning that those works perform evaluation on the mean-squared error (MSE) in 3D joint positions with respects to the Mixamo dataset. However, as pointed out by ReConForM \[Cheynel et al. [^5]\], there are several qualitative issues with the motions of the Mixamo dataset, caused by artifacts of Adobe Mixamo’s closed-source retargeting method.

Moreover, none of the aforementioned methods were able to use supervised training, due to the lack of ground truth dataset of sufficient size and on a large-enough variety of characters. Therefore, instead of relying on paired motions on source and targets character, the models are implicitly trying to learn the distribution of acceptable motions for each character, based on their limb proportions and morphology. This task is arguably more difficult than supervised learning (which the current Mixamo dataset does not allow), especially given its extremely limited character diversity that makes it difficult for models to generalize to new characters with unseen limb proportions or body shape.

We argue that the field of retargeting is missing a way to obtain high-quality data on an almost continuous distribution of input skeletons and morphologies, and introduce our method as a reliable way to generate a larger training dataset. A high-quality reliable retargeting method could already be used by itself in a lot of contexts, but training learning-based methods is still relevant for later use when a differentiable retargeting is needed (for instance, when training other learning-based architectures), or to incorporate new losses that are hard to encode manually.

### 2.4 Control rig inversion

Despite its widespread use in industrial settings, the concept of control rigs remains largely unexplored in academic literature. When used, control rigs are most often seen as a black box, given as input from an animation expert. This “black box” interpretation of the rig assimilates it to a function $f : c \rightarrowtail \left(\right. \mathcal{M}_{n} \left.\right)$, which takes as input a set of control values *c*, and returns either the transformation matrices $\mathcal{M}$ of the *N* bones (which drive the mesh through skinning), or directly that of the mesh’s vertices.

Some previous works manipulate control rigs through the task of “rig inversion”, which consists in finding the inverse *f* <sup>− 1</sup> of that black-box function – essentially, finding the control values which match a given skeleton pose. For instance, Holden et al. \[[^13]\] learn an inverse rig mapping using gaussian process regression, along with the Jacobian of the control rig, which allows for an optimization procedure to reach more accurate control values. Follow-up work \[Holden et al. [^14]\] shows the impact of deep learning instead of traditional machine learning techniques. Marquis Bolduc and Phan \[[^22]\] take a similar approach, by first teaching a multi-layer perceptron to approximate the rig function, before teaching a separate network to invert the first one. Gustafson et al. \[[^10]\] derive an analytical approximation of the rig, and invert the rig using a finite-difference method. Several other works specifically focus on facial rigs (which behave slightly differently from our use case), once again taking the “black box” approach \[Racković et al. [^25]; Racković et al. [^26]\].

It is worth noting that industrials have presented new animation systems that rely on some flavour of control rigs \[Bereznyak [^4]; Hecker et al. [^11]\]. Both of them allow for easy retargeting to characters of different morphologies; however, motions shown are only locomotion, and the proposed systems are not released. Similarly, using “simplified” or “virtual” skeletons to manipulate poses for the retargeting task has also been proposed \[Kulpa et al. [^17]; Monzani et al. [^24]\], which can be understoord as prototypes of control rigs.

To the best of our knowledge, no previous academic work explains in detail the inner mechanisms that drive the construction of control rigs. In contrast, we provide a detailed explanation of these mechanisms and leverage their strengths to propose a robust and efficient retargeting method.

## 3 Method Overview

We propose a pipeline to transfer motions from one animated character to another. Our method comprises three main stages, depicted in Figure [2](#fig2):

- Given a source and target skinned characters (meshes + bones + skinning weights), we automatically build two control rigs adapted to their respective morphologies. We also pre-compute a proxy for the shape of the torso, using a set of cone primitives, which will serve during the collision refinement stage.
- Given the animation of the source character’s bones, we perform “rig inversion”, which is a procedure designed to find the position, rotation and scale of the rig’s controllers, in order to replicate the original motion.
- Finally, we perform retargeting in rig-space, where the high-level abstraction allowed by the rig makes it effortless to transfer the most important aspects of motion (for instance, foot unrolling while walking, or hand positions with respect to one another). We also use our mesh proxy to identify collisions (or lack thereof) on the source motion and transfer them to the target character.

## 4 Automatic Control Rig

Artists often use “control rigs” as a tool to manipulate 3D characters in a more intuitive way. Using the advice of an experienced rigging artist, we built a template control rig in the open-source Blender software \[Community [^7]\]. Our rig implements several mechanisms to allow for easier manipulation of the character’s skeleton, especially thought for the task of motion retargeting. Moreover, we propose a method to automatically build such a rig for any input character, depending on its morphology, by following the steps described next. For more detail on the rig structure, we provide the full control rig on a sample character on the project webpage.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/8f152efb-6f6b-4120-89af-887e47fc2f3c/assets/images/large/mig25-16-fig3.jpg)

Schematics of the constraint system which allows for the dual-hinge mechanism (bottom), with the corresponding deformations of the mesh (top). DEF denotes the original “deform” bone, and MCH denotes the “mechanical” bones of the control rig.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/b9a340a4-a78c-4fab-89a1-e6567900687b/assets/images/large/mig25-16-fig4.jpg)

The heel controller allows for easy foot unrolling, which is useful for animating locomotion.

### 4.1 Heel bone placement

A preliminary requirement is to place a mechanical bone (i.e., a bone not directly deforming the mesh via skinning) for the heel of the character, which serves as a starting point for the foot roll mechanism. To do this, we select the vertices which are skinned to all foot bones. We keep only the vertices whose height is in the lowest 25% range, as we are interested only in the sole of the foot. We then project the 3D position of the vertices on the ground plane, and perform singular value decomposition (SVD) on the 2D positions, taking care to weigh each vertex by the average size of the faces it belongs to. The SVD yields two vectors $\overset{\rightarrow}{u}$ and $\overset{\rightarrow}{v}$, which correspond to the axis with the most variation (arguably, the foot’s longitudinal axis) and the axis with the least variation (arguably, the foot’s side-to-side axis). We compute the oriented bounding box along those two axes; that is (*p <sup>i</sup>* being the position of vertex *i*):

- $u_{\text{min}} = \underset{i}{min} p^{i} \cdot \overset{\rightarrow}{u}$, $u_{\text{max}} = \underset{i}{max} p^{i} \cdot \overset{\rightarrow}{u}$
- $v_{\text{min}} = \underset{i}{min} p^{i} \cdot \overset{\rightarrow}{v}$, and $v_{\text{max}} = \underset{i}{max} p^{i} \cdot \overset{\rightarrow}{v}$

This allows us to place the heel bone between the points $u_{\text{min}} \overset{\rightarrow}{u} + v_{\text{min}} \overset{\rightarrow}{v}$ and $u_{\text{min}} \overset{\rightarrow}{u} + v_{\text{max}} \overset{\rightarrow}{v}$ – with a height of 0 so it rests on the ground plane in 3D space. We provide additional figures illustrating this process in the Supp. Mat.

### 4.2 Foot mechanism

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/64d9bc73-e2e5-4eae-9169-8f611d6df266/assets/images/large/mig25-16-fig5.jpg)

The spine controller (blue) splits its rotation between the spine bones (red).

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/2368f075-7d90-4797-ab74-f9810c3c7d38/assets/images/large/mig25-16-fig6.jpg)

Finger controls.

We then automatically build a standard foot roll mechanism, which has two rotation-only controllers. The core mechanism revolves around two dual-hinge systems, one for the pronation (ankle rolling inwards) and supination (ankle rolling outwards), and the other for the dorsiflexion and plantar flexion. Figure [3](#fig3) visually explains the constraint setup which allows for the latter: it is built entirely with “Copy Rotation” and “Limit Rotation” constraints. The “Copy Rotation” transfers the world-space rotation of the controller to the bones (“MCH bone left” and “MCH bone right” in the figure), just before the “Limit Rotation” restricts those same rotations to a specific range, expressed in local space (allowed range illustrated in white in the figure). This effectively creates a dual hinge, where a positive rotation causes the whole system to rotate around the left bone, and a negative rotation causes the whole system to rotate around the right bone.

Figure [4](#fig4) demonstrates the usefulness of this mechanism for a walk cycle: the first heel impact (3a) and last toe contact (3b) can be modeled with the rotation of a single controller, while the foot’s position controller stays stationary.

### 4.3 Hip control

To control the pelvis’ rotation and position in space, we create a control bone which is located directly under the pelvis, at the height of the thigh bones. This vertical offset prevents stretching of the legs when the controller rotates forward / backward.

### 4.4 Legs and arms inverse kinematics

For hands and feet, we automatically place a controller bone right outside the mesh (in the palm for hands, and under the soles for the feet), to which the hand and feet mechanisms are parented. We then use Blender’s “Inverse Kinematics” constraint, which uses the position of the hand/ankle bone along with the position of a newly created “pole target” controller to drive the bones of the chain.

### 4.5 Spine and neck rotations

Unlike the foot roll (which is a fairly standard mechanism), there are several valid ways to rig spines. In our implementation, we take a simple approach, which consists in splitting the rotation of the controller equally amongst all spine bones (see Figure [5](#fig5)), allowing for retargeting to a character with fewer or more spines.

### 4.6 Fingers

Finally, our method automatically rigs each finger using a single controller. Its rotation determines the rotation of the proximal phalanx, and its scale controls the rotation of other phalanges (how “curled” the finger is), as shown on Figure [6](#fig6).

## 5 Control Rig Inversion

From an animation defined on a source character, rig inversion is the task that consists in finding the right values for the control rig’s parameters, to obtain visually similar poses. In general, control rig inversion is a complex task, which requires scripting a set of rules for each new rig. Moreover, the rig function is neither injective nor surjective: some poses of the bones simply cannot be reached with the controllers, and several different controller values may yield the same pose. However, in our case, all characters now follow the same simple template. We are thus able to derive a procedure which inverts this control rig, regardless of limb proportions, number of bones, or skeleton topology. Our inverse rig algorithm is based on opinionated rules, which solve the aforementioned ambiguity in a convenient way for the retargeting task. Conceptually, we perform the following:

- We rotate the hip controller and place it so that the rig’s pelvis bone is at the same position as the original skeleton’s.
- We rotate the spine (and neck) controllers so that the rig’s last spine (and head) have the same rotation as the original skeleton’s.
- We determine the rotations of the two controllers of the feet (case disjunction depending on the heel and toes rotations).
- We determine the rotation and scales of the fingers controllers so that the rig’s first and last phalanges has the same rotation as the original skeleton’s.
- We rotate the hand and feet controllers and place them so that the wrist and ankle bones are at the same positions as the original skeleton’s.
- We determine the angle of the pole targets of arms and legs IK chains that match the position of the elbows / knees.

The bones of the original skeleton and the control rig having different matrices in T-pose, several changes of coordinate frames are required at each step (i.e., “same rotation” means “same world-space rotation between matrices in T-pose and in final pose”). We left them out in the conceptual explanation above; as such, for reproducibility purposes, we provide a complete pseudo-code description of this algorithm in the Supplementary Material.

## 6 Rig-space retargeting

At this point, we now have two rigged characters (the source and target), whose control rigs are automatically created through the process described in Section [4](#sec-4). We also have transferred the animation of the source character onto its control rig, through the algorithm described in Section [5](#sec-5). In this section, we explain how we transfer the motion from the source control rig onto the target character’s control rig, while preserving the motion semantics.

### 6.1 Driving controllers

First, we analyze the source motion to determine which of the rig’s controllers are “driving” the motion. In traditional character animation (i.e., when no control rig is used), the root bone of the skeleton is often placed near the center of mass of the character (the hips), which – most of the time – doesn’t accurately reflect the way that a human interacts with their environment, unless they are in freefall. As an example, when a human walks, the motion of their hips is due to friction between their feet and the floor, so we can say that each foot is successively “driving” the motion in that case. We propose a mathematical formulation to capture the intuitive concept described above, based on three assumptions:

- Our first assumption is that humans interact mostly with the ground floor, that is, the plane *z* = 0. As such, for each frame *f*, we assign a first weight to each controller *c* (hands, feet, hips) based on the inverse of their height $h_{c}^{f}$.
- Our second assumption is that an extremity interacting with the environment tends to stay stationary and in contact. To give more importance to stationary controllers, we define a weight based on the inverse of their velocity $v_{c}^{f} = \frac{1}{\Delta t} \parallel p_{c}^{f} - p_{c}^{f - 1} \parallel$ (where $p_{c}^{f}$ is the position of controller *c* at frame *f*).
- Our final assumption is that, when several controllers touch the floor, the ones that support the most weight are more likely to stay fixed and “drive” the rest of the motion. As such, we define a third weight for each controller, based on the inverse of the distance between their position $p_{c}^{f}$ and the projection of the hip controller $p_{\text{COM}}^{f} = p_{\text{hip}}^{f} - h_{\text{hip}}^{f} \overset{\rightarrow}{z}$ on the floor (which approximates the center of mass).

All in all, each controller *c* is assigned a weight for frame *f*, which is the product of the three weights defined previously:

$$
w_{c}^{f} = \frac{1}{1 + \alpha h_{c}^{f}} \cdot \frac{1}{1 + \gamma v_{c}^{f}} \cdot \frac{1}{1 + \beta \parallel h_{\text{c}}^{f} - p_{\text{COM}}^{f} \parallel}
$$

which we group into the following vector:

$$
w^{f} = \left{\right. w_{c}^{f} \left|\right. c \in \text{Controllers} \left.\right}
$$

By applying the softmax, we can get a vector which sums to 1: *W <sup>f</sup>* = softmax(*T* × *w <sup>f</sup>*), where *T* = 1 is the temperature parameter.

The hyper-parameters *α*, *γ* and *β* are used to balance the contributions of the three weights. For our experiments, we arbitrarily estimate threshold values for the three components: that is, we might want a controller whose height $h_{c}^{f} = 0.01 \text{m}$ to weigh twice as much as a controller whose height $h_{c}^{f} = 0.03 \text{m}$, giving us *α* = 100. Similarly, we might want a controller whose speed $v_{c}^{f} = 0.01 \text{m}.\text{s}^{- 1}$ to weigh twice as much as a controller whose speed $v_{c}^{f} = 0.03 \text{m}.\text{s}^{- 1}$, giving us *β* = 100. And finally, we might want a controller that is 0.1 m away from the projection of the center of mass to weigh twice as much as a controller that is 0.3 m away, giving us *γ* = 10.

### 6.2 Retargeting with respect to a controller

Say we have a single driving controller (the left foot) on the source character, and that we want to retarget the pose onto the target character’s control rig. We start by putting the target controller at the same position. Then, we can determine the target hip controller’s location, by computing the vector (source ankle *to* source hip) in the reference frame of the source ankle, scaling it by the ratio between the limb lengths on source and target, and transferring it to the reference frame of the target ankle. We can then perform the same operation to locate the right foot based on the hip position, then each hand based on the last spine position, and finally the pole targets (for the knees and elbows). Additional rules are used at each step to ensure, for example, accurate height with respects to the floor: see Supp. Mat. for full details.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/bfd7aec8-5f0c-4d89-b30d-3474cf75ff37/assets/images/large/mig25-16-fig7.jpg)

Visual explanation of the retargeting method

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/a56fa5f3-9159-4e5a-823d-59f5dc08f87d/assets/images/large/mig25-16-fig8.jpg)

Cones fitted to the source character

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/e1e9985c-6945-40af-af3b-8ba4326c5ebc/assets/images/large/mig25-16-fig9.jpg)

Output of section 6, showing collisions

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/8181ac34-66b0-4015-8968-d5f9729cbbdf/assets/images/large/mig25-16-fig10.jpg)

After the collision resolution algorithm

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/36f4560f-0235-4b82-8f26-45068654526a/assets/images/large/mig25-16-fig11.jpg)

Schematized procedure applied when retargeting controllers close to the torso

### 6.3 Retargeting consecutive frames

To retarget the first frame of an animation, we first perform the process explained in Section [6.2](#sec-6-2) for the controller with the highest weight. For each subsequent frame, we then run as many processes as there are controllers. For each target controller, we use its position at the previous frame, along with the world-space velocity of the source controller, to determine its new position, before solving for the rest of the chain (with the same process as described in Section [6.2](#sec-6-2)). This gives us 5 different positions for each controller, and the final result is obtained by a weighted average, using *W <sup>f</sup>*. This hereditary process is depicted on Figure [7](#fig7).

## 7 Restoring semantic contacts

Avoiding interpenetration between the character’s limbs is crucial when retargeting motion from a source character whose mesh does not self-collide. In order to achieve this, we refine the retargeted effector positions whenever the input animation drives them close to the surface of the mesh. To achieve this, we first approximate the surfaces of the source and target characters with a set of cones primitives fitted to the mesh vertices, and use the features of this easily manipulable shape representation to perform a mesh-aware refinement of the effector positions. We detail this process next.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/489da8ac-ff99-448a-b8a4-5942ed3cb8aa/assets/images/large/mig25-16-fig12.jpg)

Results of our collision refinement algorithm. Left to right: source pose, Mixamo’s retargeting, Ours (rig-retargeting only), Ours (collision refinement)

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/2828fbdd-576d-46b6-aa11-dfa529e69a47/assets/images/large/mig25-16-fig13.jpg)

Motion where rig-space retargeting helps preserve the semantic contact between the hands. Left to right: source, Mixamo, MIRRORED-Anims.

### 7.1 Mesh approximation

Let us focus on approximating the character’s torso, which is the source of most unwanted inter-penetration (generally with the arms) when an animation is transferred to a character of different morphology. To do so, we select the vertices which are skinned to a certain set of *k* bones $\left(\left(\right. \mathcal{B}_{i} \left.\right)\right)_{1 \leq i \leq k}$ (the hip and spine bones). We consider the axis $\overset{\rightarrow}{a} = \mathcal{B}_{k} - \mathcal{B}_{1}$ defined by the first and last bones. We split the vertices into *n* uniformly sampled slices along this axis: that is, the *i* -th slice contains vertices $\left{\right. v_{j} \left|\right. \left(\right. v_{j} - \mathcal{B}_{1} \left.\right) \cdot \frac{\overset{\rightarrow}{a}}{\parallel \overset{\rightarrow}{a} \parallel^{2}} \in \left[\right. \frac{i - 1}{k} , \frac{i}{k} \left[\right. \left.\right}$.

For each slice, we fit a circle to the vertices using a least-squares method. The successive circles describe a set of truncated cones, which individually provide a convex approximation of the mesh between two slices, as shown on Figure [8](#fig8).

Moreover, using the average skinning weights of the vertices, we can effectively skin each circle to each of the bones $\left(\right. \mathcal{B}_{i} \left.\right)$, which allows us to keep the approximation of the mesh when it deforms.

### 7.2 Retargeting a controller close to the mesh

Having defined similar approximations for the source’s and target’s torsos, the goal is now to use the relative position of the effectors to the source torso in order to adjust the position of the retargeted effectors, whenever they come close to (or inside) the mesh. This process is illustrated in Figure [11](#fig11).

First, given an effector position *P*, we want to identify which cone this point is “in front of”. As shown on Fig. [11](#fig11).1, this is ambiguous to answer when the character is in a certain pose. To solve this ambiguity, we convert this position *P* into a corresponding position $Q$ when the character is in T-pose. Therefore, we compute virtual “skinning weights” for the point *P*, so that we can invert the linear-blend skinning (LBS) to obtain $Q$. Those skinning weights $w$ are defined using the inverse of the distances between *P* and the closest point on each circle: $w = \text{softmax} \left(\right. \left(\left{\right. \frac{1}{\parallel P - P_{i} \parallel} \left.\right}\right)_{0 \leq i \leq k} \left.\right)$, where *P <sub>i</sub>* is the point closest to *P* on the circle of the *i* -th slice.

Then, we compute the position of $Q$ such that, if it were skinned to the circles (which are themselves skinned to the bones) with the weights $w$, it would end up at the position *P*.

Now that we have a position for $Q$ where the character’s spines are straightened, we can project $Q$ on the axis $\overset{\rightarrow}{a}$ (between first and last bones), and identify which cone this projection lands in. Then, we build a $\text{coordinate system } C$ whose position is the projection of $Q$ on that $\text{cone}$, and whose orientation is defined by the normal and tangent vectors to the cone at that point. We store the position of $Q$ in that coordinate system: $Q \left|\right._{C}$.

Finally, to obtain the corresponding point on the target, we identify the corresponding $\text{coordinate system } C^{′}$ on the corresponding cone. We compute the matching position $Q^{′}$ such that $Q^{′} \left|\right._{C^{′}} = Q \left|\right._{C^{′}}$. Once again, we compute virtual skinning weights $w^{′}$ using inverse distances: $w^{′} = \text{softmax} \left(\right. \left(\left{\right. \frac{1}{\parallel Q^{′} - Q_{i}^{′} \parallel} \left.\right}\right)_{0 \leq i \leq k} \left.\right)$, where $Q_{i}^{′}$ is the point closest to $Q^{′}$ on the circle of the *i* -th slice. Having solved for the T-pose $Q^{′}$ position, we use linear blend skinning to obtain the position of *P* ′ when the target mesh is in the retargeted pose.

All in all, we are able to obtain a matching world-space position *P* ′ for the original controller position *P*, while taking into account the source’s and target’s meshes. After our retargeting process, we interpolate between the current position of the target controller, and this new position *P* ′, based on how close *P* is to the source mesh.

| **Metric** | **Aggregate** | **Value** (m) |
| --- | --- | --- |
| **Average** **pos. err.** | mean | 6.06 · 10 <sup>− 3</sup> |
|  | max | 1.32 · 10 <sup>− 2</sup> |
| **Worst** **pos. err.** | mean | 6.77 · 10 <sup>− 2</sup> |
|  | max | 1.50 · 10 <sup>− 1</sup> |

Results of the rig inversion algorithm (average and worst joint position error across all joints of the animation), aggregated over all animations in the dataset.

| **Network** | **Dataset** | **MSE (↓)** | **Pen.% (↓)** |
| --- | --- | --- | --- |
| R <sup>2</sup> ET | Mixamo | 0.447 | 9.32 |
| R <sup>2</sup> ET | omaxiM | 0.360 | 8.24 |

Comparison between the standard Mixamo dataset, and our omaxiM dataset, both used to train the same network from R <sup>2</sup> ET \[Zhang et al. [^34]\] (skeleton-aware part only).

## 8 Results

### 8.1 Rig inversion

We evaluated the accuracy of our rig inversion algorithm by measuring the average error in joint position across the 30 motions of SMTNet’s test set \[Zhang et al. [2024a](#Bib0034)\], and report it in Table [1](#tab1). Since the rig is over-constrained in some places (fingers, spine), it is not possible to reach a perfect accuracy; however, our rig inversion method still manages to reach a high level of fidelity with respect to the FK motion.

### 8.2 Improved Dataset for Learning-based Retargeting

We used MIRRORED-Anims to retarget the entire Mixamo database \[Adobe [^2]\] (2446 motions) to 40 different characters, in order to create omaxiM: a more extensive, open-source motion retargeting dataset. Then, we trained the skeleton-aware network proposed by R <sup>2</sup> ET \[Zhang et al. [^34]\], and compare it to a training performed only on the standard Mixamo dataset. We report, in Table [2](#tab2), the performance of both trainings on unseen characters and motions from the NKN’s test set \[Villegas et al. [^31]\].

This experiment demonstrates that the generalization abilities of the network are closely tied to the diversity of characters in the training dataset, highlighting the impact that a larger academic dataset could have on the field of retargeting.

### 8.3 Quantitative comparisons

The main motivation for our method was to tackle the lack of high-quality data in learning-based methods, so a direct comparison between our retargeting procedure and the results of learning-based methods is not the primary focus of this work. Nonetheless, to provide quantitative context and demonstrate the quality of our generated data, we report evaluations against state-of-the-art learning-based methods \[Aberman et al. [^1]; Lim et al. [^20]; Villegas et al. [^31]; Zhang et al. [^34]\] in Table [3](#tab3). For this, we used the test set introduced by SMTNet \[Zhang et al. [2024a](#Bib0034)\], which consists of 30 clean Mixamo motions performed by 3 characters, retargeted onto 3 different characters.

To evaluate closeness to the Mixamo “ground-truth”, we used the mean squared error of the joint positions in world-space (MSE), as well as the mean-squared error with respect to the root bone’s position (MSE <sup><i>lc</i></sup>). We also evaluated penetration using the proportion of vertices that penetrate with another part of the mesh. Our method reaches results which are far closer to the outputs of Mixamo than learning-based methods.

| **Method** | **MSE (↓)** | **MSE <sup><i>lc</i></sup> (↓)** | **Pen.%** (↓) |
| --- | --- | --- | --- |
| Source | – | – | 4.43 |
| GT | – | – | 9.06 |
| Copy Rotations | 0.005 | 0.005 | 9.03 |
| NKN \[Villegas et al. [^31]\] | 0.326 | 0.231 | 8.71 |
| SAN \[Aberman et al. [^1]\] | 0.435 | 0.255 | 9.74 |
| R <sup>2</sup> ET \[Zhang et al. [^34]\] | 0.499 | 0.496 | 7.62 |
| SMTNet \[Zhang et al. [2024a](#Bib0034)\] | 0.284 | 0.229 | 3.50 |
| Ours | **0.008** | **0.002** | **3.04** |
| Ours (no coll.) | 0.008 | 0.002 | 3.06 |

Quantitative comparison to several state-of-the-art method. Ours (no coll.) denotes our rig-space retargeting without the collision refinement.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/7133b803-9ae7-43cd-affc-6646304a0479/assets/images/large/mig25-16-fig14.jpg)

Retargeting from SMPL (left) to a Mixamo character (right).

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/7aa614a7-e982-4d12-a827-8a726dad58a8/assets/images/large/mig25-16-fig15.jpg)

Comparison of our method to Mixamo. Top to bottom: source motion, Mixamo, MIRRORED-Anims. Note: on the source motion, the hands do not fully touch the floor, which explains the small offset on our output.

### 8.4 Qualitative comparison

We offer several visual comparisons of our method’s results compared to Mixamo’s proprietary algorithm, which is currently used as “ground truth” in all the learning-based methods.

For one, our method allows for more precise hand contacts, as demonstrated by Figures [15](#fig15) and [16](#fig16): retargeting the cartwheel motion on a character with longer legs and shorter arms automatically causes a lower center of mass during the “upside-down” portion of the motion, with the hands touching the floor. We obtain better hand-floor contacts, while matching Mixamo’s level of quality on foot-floor contacts and foot sliding. Our method also reaches better results on hand-hand interactions, since the controller’s position is computed in the shared coordinate system of the spine, as demonstrated on Figures [13](#fig13) and [17](#fig17). The control rig proves useful for poses like that shown in Figure [18](#fig18): having the heel of the foot precisely on the ground, or the palm of the hand on the floor, would have been unattainable with previous methods. Moreover, thanks to our approximation of the skin mesh, we can refine limbs that overlap with the torso. Figure [12](#fig12) demonstrates the importance of this approximation when retargeting onto characters with a different body shape. Additional explanations as to why our rig-space retargeting performs better than Mixamo can be found in the Supp. Mat.

We performed a double-blind user study to estimate human preference on SMTNet’s test set \[Zhang et al. [2024a](#Bib0034)\], retargeted onto ten different characters. For each sample, we asked 30 people to rank the results of Mixamo, R <sup>2</sup> ET \[Zhang et al. [^34]\], SAME \[Lee et al. [^19]\], and MIRRORED-Anims, from 1 (preferred output) to 4 (worst output). We obtain 660 individual answers, and report the mean rank of each method in Table [4](#tab4). This study demonstrates that MIRRORED-Anims often reaches the same level of quality as Mixamo (48% of answers tied Mixamo and MIRRORED-Anims), and fixes a lot of Mixamo’s defects (27% of answers strictly favored MIRRORED-Anims to Mixamo).

Finally, an experiment demonstrates that manually cleaning up eventual retargeting errors is faster for MIRRORED-Anims than for Mixamo, and in both cases, even faster when using rig controllers rather than editing the “deform bones”. See Supp. Mat. for more details.

| **Method** | **Mixamo** | **R <sup>2</sup> ET** \[[^34]\] | **SAME** \[[^19]\] | **Ours** |
| --- | --- | --- | --- | --- |
| Rank (↓) | 2.04 | 2.41 | 3.54 | **2.00** |

Average rank of each method in our user study.

### 8.5 Retargeting SMPL datasets

Two limitations of the Mixamo dataset, mentioned in Section [1](#sec-1), are the small numbers of motions and characters it contains. Our method could help increase the diversity of motions and character proportions used to train retargeting tasks, by tapping into the available motion capture datasets for the SMPL character \[Loper et al. [^21]\]. Our method allows to retarget any of these motions onto any other characters, even out-of-distribution ones (having extreme, even unrealistic body proportions). We can also retarget these motions onto the cartoon characters from Mixamo. To demonstrate this, we applied our method to a motion from the Moyo dataset \[Tripathi et al. [^29]\]. The SMPL body model is famously difficult to retarget onto artist-made characters, due to the non-conventional placement of its bones. However, our universal control rig allows for a high-level abstraction which circumvents those issues, as shown on Figure [14](#fig14).

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/ecc164f0-1673-44a4-bee2-9fb64c13334f/assets/images/large/mig25-16-fig16.jpg)

Our method is better than Mixamo at capturing hand-floor interactions. Left to right: source pose, Mixamo’s retargeting, MIRRORED-Anims.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/360d9255-a5c3-4a82-8353-88e9e2e94fa9/assets/images/large/mig25-16-fig17.jpg)

Our method also performs better than Mixamo for hand-hand interactions like clapping. Left to right: source pose, Mixamo’s retargeting, MIRRORED-Anims.

![](https://dl.acm.org/cms/10.1145/3769047.3769064/asset/69c0474f-4eb0-4be0-b7db-5dccdafbb9b5/assets/images/large/mig25-16-fig18.jpg)

Example of our retargeting on a complex pose, which demonstrates the importance of the foot and finger rigs. Left: source character, right: target character.

## 9 Discussion, Limitations and Future work

We proposed a motion retargeting method that relies on the adaptation of a standardized control rig on both the source and target characters. Once expressed as an animation of the rig parameter values, the input animation is easily transferred to the target rig. The latter is finally corrected to avoid any unwanted interpenetration due to morphological change, and to restore meaningful contacts. However, we noted a few limitations:

First, the method may fail on some motions where the driving controllers cannot be properly identified by our method, that is, when driving controllers do not follow our assumptions described in Section [6.1](#sec-6-1) (for instance, a character doing pull-ups). A hybrid method could use a learning-based approach to identify the driving controllers.

Second, even though the results are aesthetically pleasing and offer a high degree of fidelity for foot contacts and self-collisions, it is worth noting that the method does not strictly ensure physical realism. To this end, a reinforcement-learning method \[Reda et al. [^27]\] could be used with the results of MIRRORED-Anims, which would improve physical accuracy.

Moreover, our retargeting method is not always able to preserve all semantically meaningful contacts in a pose, which may be a problem when the animation includes multiple contacts, e.g. between the hands and the feet. One could also adapt the retargeting algorithm so that controllers that are close together are Another approach could be to use optimization-based retargeting, which would manage to give satisfying results \[Cheynel et al. [^5]\]; however, these optimization-based methods work on the skeleton level and cannot optimize through the control rig layer.

Furthermore, the collision refinement method could easily be improved with ellipses instead of circles. While our current implementation only prevents penetrations of the end-effectors with the torso, a similar procedure could easily be applied to prevent inter-penetrations between limbs. Finally, the MIRRORED-Anims method could also be refined with a more complex rig setup (for instance, by using Spline Inverse Kinematics) to allow for finer control of some parts of the character, or by integrating ready-made mechanisms found in industry-standard rigging tools like Rigify \[Community [^7]\].

## 10 Conclusion

MIRRORED-Anims is, to the best of our knowledge, the first method to build on industry-grade rigging techniques to perform motion retargeting in rig-space. Retargeting is often a quality bottleneck in motion-related tasks, from human pose estimation to robotics, and learning-based methods seem to be the most promising way to capture a fine understanding of motion semantics. This can only happen through large, high-quality motion datasets. MIRRORED-Anims is a step towards building these large datasets, and we see it as a stepping stone to steer future academic retargeting works towards improved sources of data. We hope to see future work apply our retargeting method to motion capture datasets with a wide diversity of tasks and styles.

[^1]: Kfir Aberman, Peizhuo Li, Dani Lischinski, Olga Sorkine-Hornung, Daniel Cohen-Or, and Baoquan Chen. 2020. Skeleton-Aware Networks for Deep Motion Retargeting. *ACM Transactions on Graphics (TOG), Proc. SIGGRAPH* 39, 4 (2020), 62.

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Skeleton-Aware+Networks+for+Deep+Motion+Retargeting&author=Kfir+Aberman&author=Peizhuo+Li&author=Dani+Lischinski&author=Olga+Sorkine-Hornung&author=Daniel+Cohen-Or&author=Baoquan+Chen&publication_year=2020&pages=62)

[^2]: Adobe. 2024. Mixamo. *[https://www.mixamo.com/](https://www.mixamo.com/)*. Accessed: 2025-03-03.

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Mixamo&author=Adobe&publication_year=2024)

[^3]: Jean Basset, Stefanie Wuhrer, Edmond Boyer, and Franck Multon. 2020. Contact preserving shape transfer: Retargeting motion from one shape to another. *Computers & Graphics* 89 (2020), 11–23.

[Go to Citation](#core-Bib0003-1)

[Crossref](https://doi.org/10.1016/j.cag.2020.04.002)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Contact+preserving+shape+transfer%3A+Retargeting+motion+from+one+shape+to+another&author=Jean+Basset&author=Stefanie+Wuhrer&author=Edmond+Boyer&author=Franck+Multon&publication_year=2020&pages=11-23&doi=10.1016%2Fj.cag.2020.04.002)

[^4]: Alexander Bereznyak. 2016. IK Rig: Moving Forward. (2016). [https://gdcvault.com/play/1023279/](https://gdcvault.com/play/1023279/) GDC.

[Go to Citation](#core-Bib0004-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=IK+Rig%3A+Moving+Forward&author=Alexander+Bereznyak&publication_year=2016)

[^5]: Théo Cheynel, Thomas Rossi, Baptiste Bellot-Gurlet, Damien Rohmer, and Marie-Paule Cani. 2025. ReConForM: Real-time Contact-aware Motion Retargeting for more Diverse Character Morphologies. In *Computer Graphics Forum*. Wiley Online Library, e70028.

[Crossref](https://doi.org/10.1111/cgf.70028)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=ReConForM%3A+Real-time+Contact-aware+Motion+Retargeting+for+more+Diverse+Character+Morphologies&author=Th%C3%A9o+Cheynel&author=Thomas+Rossi&author=Baptiste+Bellot-Gurlet&author=Damien+Rohmer&author=Marie-Paule+Cani&publication_year=2025&pages=e70028&doi=10.1111%2Fcgf.70028)

[^6]: Kwang-Jin Choi and Hyeong-Seok Ko. 2000. Online motion retargetting. *The Journal of Visualization and Computer Animation* 11, 5 (2000), 223–235.

[Go to Citation](#core-Bib0006-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Online+motion+retargetting&author=Kwang-Jin+Choi&author=Hyeong-Seok+Ko&publication_year=2000&pages=223-235)

[^7]: Blender Online Community. 2025. *Blender - a 3D modelling and rendering package*. Blender Foundation, Stichting Blender Foundation, Amsterdam. [http://www.blender.org](http://www.blender.org/)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Blender+-+a+3D+modelling+and+rendering+package&author=Blender%C2%A0Online+Community&publication_year=2025)

[^8]: Mathias Delahaye, Bruno Herbelin, and Ronan Boulic. 2023. Real-time self-contact retargeting of avatars down to finger level. (2023).

[Go to Citation](#core-Bib0008-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Real-time+self-contact+retargeting+of+avatars+down+to+finger+level&author=Mathias+Delahaye&author=Bruno+Herbelin&author=Ronan+Boulic&publication_year=2023)

[^9]: Michael Gleicher. 1998. Retargetting motion to new characters. In *Proc. ACM SIGGRAPH*. 33–42.

[Go to Citation](#core-Bib0009-1)

[Digital Library](https://dl.acm.org/doi/10.1145/280814.280820)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Retargetting+motion+to+new+characters&author=Michael+Gleicher&publication_year=1998&pages=33-42&doi=10.1145%2F280814.280820)

[^10]: Stephen Gustafson, Aaron Lo, and Paul Kanyuk. 2020. Analytically Learning an Inverse Rig Mapping. In *Special Interest Group on Computer Graphics and Interactive Techniques Conference Talks*. 1–2.

[Go to Citation](#core-Bib0010-1)

[Digital Library](https://dl.acm.org/doi/10.1145/3388767.3407316)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Analytically+Learning+an+Inverse+Rig+Mapping&author=Stephen+Gustafson&author=Aaron+Lo&author=Paul+Kanyuk&publication_year=2020&pages=1-2&doi=10.1145%2F3388767.3407316)

[^11]: Chris Hecker, Bernd Raabe, Ryan W. Enslow, John DeWeese, Jordan Maynard, and Kees van Prooijen. 2008. Real-time motion retargeting to highly varied user-created morphologies. In *ACM SIGGRAPH 2008 Papers* (Los Angeles, California) (*SIGGRAPH ’08*). Association for Computing Machinery, New York, NY, USA, Article 27, 11 pages.

[Go to Citation](#core-Bib0011-1)

[Digital Library](https://dl.acm.org/doi/10.1145/1399504.1360626)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Real-time+motion+retargeting+to+highly+varied+user-created+morphologies&author=Chris+Hecker&author=Bernd+Raabe&author=Ryan%C2%A0W.+Enslow&author=John+DeWeese&author=Jordan+Maynard&author=Kees+van+Prooijen&publication_year=2008&doi=10.1145%2F1399504.1360626)

[^12]: Edmond Ho, Taku Komura, and Chiew-Lan Tai. 2010. Spatial Relationship Preserving Character Motion Adaptation. *ACM Trans. Graph.* 29 (07 2010).

[Go to Citation](#core-Bib0012-1)

[Crossref](https://doi.org/10.1145/1833351.1778770)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Spatial+Relationship+Preserving+Character+Motion+Adaptation&author=Edmond+Ho&author=Taku+Komura&author=Chiew-Lan+Tai&publication_year=2010&doi=10.1145%2F1833351.1778770)

[^13]: Daniel Holden, Jun Saito, and Taku Komura. 2015. Learning an inverse rig mapping for character animation. In *Proceedings of the 14th ACM SIGGRAPH/Eurographics Symposium on Computer Animation*. 165–173.

[Go to Citation](#core-Bib0013-1)

[Digital Library](https://dl.acm.org/doi/10.1145/2786784.2786788)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Learning+an+inverse+rig+mapping+for+character+animation&author=Daniel+Holden&author=Jun+Saito&author=Taku+Komura&publication_year=2015&pages=165-173&doi=10.1145%2F2786784.2786788)

[^14]: Daniel Holden, Jun Saito, and Taku Komura. 2017. Learning Inverse Rig Mappings by Nonlinear Regression. *IEEE Transactions on Visualization and Computer Graphics* 23, 3 (2017), 1167–1178.

[Go to Citation](#core-Bib0014-1)

[Digital Library](https://dl.acm.org/doi/10.1109/TVCG.2016.2628036)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Learning+Inverse+Rig+Mappings+by+Nonlinear+Regression&author=Daniel+Holden&author=Jun+Saito&author=Taku+Komura&publication_year=2017&pages=1167-1178&doi=10.1109%2FTVCG.2016.2628036)

[^15]: Lei Hu, Zihao Zhang, Chongyang Zhong, Boyuan Jiang, and Shihong Xia. 2023. Pose-Aware Attention Network for Flexible Motion Retargeting by Body Part. *IEEE Transactions on Visualization and Computer Graphics* (2023), 1–17.

[Digital Library](https://dl.acm.org/doi/10.1109/tvcg.2023.3277918)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Pose-Aware+Attention+Network+for+Flexible+Motion+Retargeting+by+Body+Part&author=Lei+Hu&author=Zihao+Zhang&author=Chongyang+Zhong&author=Boyuan+Jiang&author=Shihong+Xia&publication_year=2023&pages=1-17&doi=10.1109%2Ftvcg.2023.3277918)

[^16]: Taeil Jin, Meekyung Kim, and Sung-Hee Lee. 2017. Motion Retargeting to Preserve Spatial Relationship between Skinned Characters. In *Symposium on Computer Animation (SCA)*. Article 25, 2 pages.

[Go to Citation](#core-Bib0016-1)

[Digital Library](https://dl.acm.org/doi/10.1145/3099564.3106647)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Motion+Retargeting+to+Preserve+Spatial+Relationship+between+Skinned+Characters&author=Taeil+Jin&author=Meekyung+Kim&author=Sung-Hee+Lee&publication_year=2017&doi=10.1145%2F3099564.3106647)

[^17]: Richard Kulpa, Franck Multon, and Bruno Arnaldi. 2005. Morphology-independent representation of motions for interactive human-like animation. In *Eurographics*.

[Go to Citation](#core-Bib0017-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Morphology-independent+representation+of+motions+for+interactive+human-like+animation&author=Richard+Kulpa&author=Franck+Multon&author=Bruno+Arnaldi&publication_year=2005)

[^18]: Jehee Lee and Sung Yong Shin. 1999. A hierarchical approach to interactive motion editing for human-like figures. In *Proc. ACM SIGGRAPH*. 39–48.

[Go to Citation](#core-Bib0018-1)

[Digital Library](https://dl.acm.org/doi/10.1145/311535.311539)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=A+hierarchical+approach+to+interactive+motion+editing+for+human-like+figures&author=Jehee+Lee&author=Sung%C2%A0Yong+Shin&publication_year=1999&pages=39-48&doi=10.1145%2F311535.311539)

[^19]: Sunmin Lee, Taeho Kang, Jungnam Park, Jehee Lee, and Jungdam Won. 2023. SAME: Skeleton-Agnostic Motion Embedding for Character Animation. (2023).

[Digital Library](https://dl.acm.org/doi/10.1145/3610548.3618206)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=SAME%3A+Skeleton-Agnostic+Motion+Embedding+for+Character+Animation&author=Sunmin+Lee&author=Taeho+Kang&author=Jungnam+Park&author=Jehee+Lee&author=Jungdam+Won&publication_year=2023&doi=10.1145%2F3610548.3618206)

[^20]: Jongin Lim, Hyung Jin Chang, and Jin Young Choi. 2019. PMnet: Learning of Disentangled Pose and Movement for Unsupervised Motion Retargeting. In *British Machine Vision Conference (BMVC)*.

[Google Scholar](https://scholar.google.com/scholar_lookup?title=PMnet%3A+Learning+of+Disentangled+Pose+and+Movement+for+Unsupervised+Motion+Retargeting&author=Jongin+Lim&author=Hyung%C2%A0Jin+Chang&author=Jin%C2%A0Young+Choi&publication_year=2019)

[^21]: Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J. Black. 2015. SMPL: A Skinned Multi-Person Linear Model. *ACM Transactions on Graphics (Proc. SIGGRAPH Asia)* 34, 6 (2015), 248:1–248:16.

[Go to Citation](#core-Bib0021-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=SMPL%3A+A+Skinned+Multi-Person+Linear+Model&author=Matthew+Loper&author=Naureen+Mahmood&author=Javier+Romero&author=Gerard+Pons-Moll&author=Michael%C2%A0J.+Black&publication_year=2015&pages=248%3A1%E2%80%93248%3A16)

[^22]: Mathieu Marquis Bolduc and Hau Nghiep Phan. 2022. Rig Inversion by Training a Differentiable Rig Function. In *SIGGRAPH Asia 2022 Technical Communications* (Daegu, Republic of Korea) (*SA ’22*). Association for Computing Machinery, New York, NY, USA, Article 15, 4 pages.

[Go to Citation](#core-Bib0022-1)

[Digital Library](https://dl.acm.org/doi/10.1145/3550340.3564218)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Rig+Inversion+by+Training+a+Differentiable+Rig+Function&author=Mathieu+Marquis%C2%A0Bolduc&author=Hau%C2%A0Nghiep+Phan&publication_year=2022&doi=10.1145%2F3550340.3564218)

[^23]: Eray Molla, Henrique Galvan Debarba, and Ronan Boulic. 2017. Egocentric mapping of body surface constraints. *IEEE transactions on visualization and computer graphics* 24, 7 (2017), 2089–2102.

[Go to Citation](#core-Bib0023-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Egocentric+mapping+of+body+surface+constraints&author=Eray+Molla&author=Henrique%C2%A0Galvan+Debarba&author=Ronan+Boulic&publication_year=2017&pages=2089-2102)

[^24]: Jean-Sébastien Monzani, Paolo Baerlocher, Ronan Boulic, and Daniel Thalmann. 2000. Using an intermediate skeleton and inverse kinematics for motion retargeting. In *Computer Graphics Forum*, Vol. 19. Wiley Online Library, 11–19.

[Go to Citation](#core-Bib0024-1)

[Crossref](https://doi.org/10.1111/1467-8659.00393)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Using+an+intermediate+skeleton+and+inverse+kinematics+for+motion+retargeting&author=Jean-S%C3%A9bastien+Monzani&author=Paolo+Baerlocher&author=Ronan+Boulic&author=Daniel+Thalmann&publication_year=2000&pages=11-19&doi=10.1111%2F1467-8659.00393)

[^25]: Stevo Racković, Cláudia Soares, Dušan Jakovetić, and Zoranka Desnica. 2024. A majorization–minimization-based method for nonconvex inverse rig problems in facial animation: algorithm derivation. *Optimization Letters* 18, 2 (2024), 545–559.

[Go to Citation](#core-Bib0025-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=A+majorization%E2%80%93minimization-based+method+for+nonconvex+inverse+rig+problems+in+facial+animation%3A+algorithm+derivation&author=Stevo+Rackovi%C4%87&author=Cl%C3%A1udia+Soares&author=Du%C5%A1an+Jakoveti%C4%87&author=Zoranka+Desnica&publication_year=2024&pages=545-559)

[^26]: Stevo Racković, Cláudia Soares, and Dušan Jakovetić. 2023. Distributed Solution of the Inverse Rig Problem in Blendshape Facial Animation. arxiv:[https://arXiv.org/abs/2303.06370](https://arxiv.org/abs/2303.06370) \[cs.CV\] [https://arxiv.org/abs/2303.06370](https://arxiv.org/abs/2303.06370)

[Go to Citation](#core-Bib0026-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Distributed+Solution+of+the+Inverse+Rig+Problem+in+Blendshape+Facial+Animation&author=Stevo+Rackovi%C4%87&author=Cl%C3%A1udia+Soares&author=Du%C5%A1an+Jakoveti%C4%87&publication_year=2023)

[^27]: Daniele Reda, Jungdam Won, Yuting Ye, Michiel Panne, and Alexander Winkler. 2023. Physics-based Motion Retargeting from Sparse Inputs. *SCA, Proceedings of the ACM on Computer Graphics and Interactive Techniques* 6 (08 2023), 1–19.

[Go to Citation](#core-Bib0027-1)

[Digital Library](https://dl.acm.org/doi/10.1145/3606928)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Physics-based+Motion+Retargeting+from+Sparse+Inputs&author=Daniele+Reda&author=Jungdam+Won&author=Yuting+Ye&author=Michiel+Panne&author=Alexander+Winkler&publication_year=2023&pages=1-19&doi=10.1145%2F3606928)

[^28]: Seyoon Tak and Hyeong-Seok Ko. 2005. A physically-based motion retargeting filter. *ACM Transactions on Graphics* 24, 1 (2005), 98–117.

[Go to Citation](#core-Bib0028-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=A+physically-based+motion+retargeting+filter&author=Seyoon+Tak&author=Hyeong-Seok+Ko&publication_year=2005&pages=98-117)

[^29]: Shashank Tripathi, Lea Müller, Chun-Hao P. Huang, Taheri Omid, Michael J. Black, and Dimitrios Tzionas. 2023. 3D Human Pose Estimation via Intuitive Physics. In *Conference on Computer Vision and Pattern Recognition (CVPR)*. 4713–4725. [https://ipman.is.tue.mpg.de](https://ipman.is.tue.mpg.de/)

[Go to Citation](#core-Bib0029-1)

[Crossref](https://doi.org/10.1109/CVPR52729.2023.00457)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=3D+Human+Pose+Estimation+via+Intuitive+Physics&author=Shashank+Tripathi&author=Lea+M%C3%BCller&author=Chun-Hao%C2%A0P.+Huang&author=Taheri+Omid&author=Michael%C2%A0J.+Black&author=Dimitrios+Tzionas&publication_year=2023&pages=4713-4725&doi=10.1109%2FCVPR52729.2023.00457)

[^30]: Ruben Villegas, Duygu Ceylan, Aaron Hertzmann, Jimei Yang, and Jun Saito. 2021. Contact-aware retargeting of skinned motion. In *Proceedings of the IEEE/CVF International Conference on Computer Vision*. 9720–9729.

[Crossref](https://doi.org/10.1109/ICCV48922.2021.00958)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Contact-aware+retargeting+of+skinned+motion&author=Ruben+Villegas&author=Duygu+Ceylan&author=Aaron+Hertzmann&author=Jimei+Yang&author=Jun+Saito&publication_year=2021&pages=9720-9729&doi=10.1109%2FICCV48922.2021.00958)

[^31]: Ruben Villegas, Jimei Yang, Duygu Ceylan, and Honglak Lee. 2018. Neural Kinematic Networks for Unsupervised Motion Retargetting. In *The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.

[Crossref](https://doi.org/10.1109/CVPR.2018.00901)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Neural+Kinematic+Networks+for+Unsupervised+Motion+Retargetting&author=Ruben+Villegas&author=Jimei+Yang&author=Duygu+Ceylan&author=Honglak+Lee&publication_year=2018&doi=10.1109%2FCVPR.2018.00901)

[^32]: Yashuai Yan, Esteve Valls Mascaro, and Dongheui Lee. 2023. ImitationNet: Unsupervised Human-to-Robot Motion Retargeting via Shared Latent Space. In *2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)*. 1–8.

[Go to Citation](#core-Bib0032-1)

[Crossref](https://doi.org/10.1109/Humanoids57100.2023.10375150)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=ImitationNet%3A+Unsupervised+Human-to-Robot+Motion+Retargeting+via+Shared+Latent+Space&author=Yashuai+Yan&author=Esteve%C2%A0Valls+Mascaro&author=Dongheui+Lee&publication_year=2023&pages=1-8&doi=10.1109%2FHumanoids57100.2023.10375150)

[^33]: Zijie Ye, Jia-Wei Liu, Jia Jia, Shikun Sun, and Mike Zheng Shou. 2024. Skinned motion retargeting with dense geometric interaction perception. *Advances in Neural Information Processing Systems* 37 (2024), 125907–125934.

[Go to Citation](#core-Bib0033-1)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Skinned+motion+retargeting+with+dense+geometric+interaction+perception&author=Zijie+Ye&author=Jia-Wei+Liu&author=Jia+Jia&author=Shikun+Sun&author=Mike%C2%A0Zheng+Shou&publication_year=2024&pages=125907-125934)

[^34]: Jiaxu Zhang, Junwu Weng, Di Kang, Fang Zhao, Shaoli Huang, Xuefei Zhe, Linchao Bao, Ying Shan, Jue Wang, and Zhigang Tu. 2023. Skinned Motion Retargeting With Residual Perception of Motion Semantics & Geometry. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*. 13864–13872.

[Crossref](https://doi.org/10.1109/CVPR52729.2023.01332)

[Google Scholar](https://scholar.google.com/scholar_lookup?title=Skinned+Motion+Retargeting+With+Residual+Perception+of+Motion+Semantics+%26+Geometry&author=Jiaxu+Zhang&author=Junwu+Weng&author=Di+Kang&author=Fang+Zhao&author=Shaoli+Huang&author=Xuefei+Zhe&author=Linchao+Bao&author=Ying+Shan&author=Jue+Wang&author=Zhigang+Tu&publication_year=2023&pages=13864-13872&doi=10.1109%2FCVPR52729.2023.01332)