---
title: "Using a Differentiable Function for Rig Inversion"
source: "https://www.youtube.com/watch?v=sYCz9LGIkuI"
author:
  - "[[SEED – Electronic Arts]]"
published: 2022-12-05
created: 2026-04-14
description: "Rig inversion is a mathematical approach that allows animators to remap an existing mesh animation onto an animation rig. This allows animators to tweak and fix up existing mesh animations, which can"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=sYCz9LGIkuI)

Rig inversion is a mathematical approach that allows animators to remap an existing mesh animation onto an animation rig. This allows animators to tweak and fix up existing mesh animations, which can be difficult or impossible otherwise.  
  
The difficulty with rig inversion is finding the rig parameter vector that best approximates a given input mesh.  
  
In this paper, we propose to solve this problem by first obtaining a differentiable rig function. We do this by training a multi-layer perceptron to approximate the rig function. This differentiable rig function can then be used to train a deep-learning model of rig inversion.  
  
This paper was presented at Siggraph Asia 2022.  
  
Download the research paper here: https://www.ea.com/seed/news/seed-rig-inversion-differentiable-rig-function  
  
\----------  
  
SEED is a pioneering group within Electronic Arts, combining creativity with applied research. We explore, build, and help determine the future of interactive entertainment.  
  
Learn more about SEED at https://seed.ea.com  
  
Find us on:  
  
Twitter: https://twitter.com/seed  
LinkedIn: https://www.linkedin.com/company/seed-ea/

## Transcript

### Introduction

**0:01** · Hello, and thank you for watching this video, where we will present a novel solution to the rig inversion problem.

**0:06** · This work was done at SEED, which is a worldwide research and development team at Electronic Arts.

### What is the rig

**0:12** · What is the rig? And why would we want to invert it?

**0:15** · For the purpose of this work, the rig is a function, assumed to be a black box, that takes three control parameters as input and produces opposed mesh as output.

**0:24** · Varying rate control values produces a mesh animation.

**0:28** · Rig inversion is a process of finding rig control values that best match an input mesh.

**0:33** · To illustrate, here is an example. On the left is captured 4D facial mesh data.

**0:39** · In the middle are rig control values found by our method. And on the right is the result of applying these values to the actual facial rig.

**0:47** · This produces a near identical animation. Finding those values allows us to directly insert the captured data in the animator’s existing pipeline.

**0:57** · There is new interest in better solving the rig inversion problem.

**1:01** · Not only are rigs getting more complex, but we have new sources of mesh data.

**1:05** · For example, new capture methods such as this Lightstage facility now allows us to acquire a large amount of high definition facial deformations.

### Deep learninggenerative models

**1:15** · Another source of raw 4D mesh data is Deep Learning generative models. For animators to be able to edit the result using their own tools, the output mesh data needs to be fit on the rig.

### Problem analysis

**1:27** · It’s important to analyze what makes this problem non-trivial.

**1:31** · First, the rig function is assumed to be non-surjective.

**1:34** · This means the rig cannot produce every possible mesh in the topology.

**1:38** · In addition, the rig may not be injective.

**1:41** · This means that different sets of rig parameters can produce the same mesh.

**1:46** · Altogether, this means even rigs that appear very simple at first might not have a perfect inverse.

**1:51** · Finally, every parameter of the rig might not have equal importance, and so optimizing for rig parameters might yield results that are visually sub-optimal.

**2:01** · Since the rig-to-mesh function is assumed to be non-bijective and thus non-invertible, we need the rig inversion model to output the best possible vector of rig parameters.

**2:11** · To determine which is the best possible set, we need to evaluate those parameters in mesh space, instead of in rig space.

### Solution

**2:19** · Here is our proposed solution to solve this problem using a deep learning model.

**2:23** · First, we pre-train a rig function model to produce the same result as the rig.

**2:29** · We then freeze this model and use it to train the rig inversion model with a loss that is in mesh space.

**2:35** · Training the rig model is more straightforward than training its inverse, and there is some prior art on doing so.

**2:41** · The rig can be kept a black box by generating random rig parameters and recording the output mesh to build the training dataset.

**2:49** · Assuming every parameter is not dependent on every other one, the size of the dataset can stay manageable.

**2:55** · Once we have the rig function model, we can then use it to train the rig inversion model.

**3:00** · The rig function model will not be needed at inference time.

**3:04** · It’s a good idea to encourage sparsity in the rig parameters so that they are easier to tune by the animators.

**3:11** · This can be done, for example, by using a lightly-weighted L1 loss on the rig parameters output, in addition to the mesh loss.

**3:18** · Having a differentiable rig model raises the question: why not simply optimize the rig parameters with respect to the mesh?

**3:25** · Unfortunately, this does not guarantee parameters that are temporarily consistent.

**3:30** · Trying to smooth these parameters will not work either, if they jump from two similar, but distant, local minima.

**3:36** · Here is what the result of trying to directly optimize each frame looks like.

**3:44** · Instead, using an inverse rig model allows us to enforce a constraint on the magnitude of its derivative, making similar outputs yield similar outputs.

**3:54** · Noise augmentation during training is one way of doing so.

**3:58** · It is critical to use activations and scaling to make sure that the rig inversion model can only output rig parameter values that are within the bounds of those used to train the rig function approximation.

**4:10** · Otherwise, the inverse rig model will optimize on undefined behavior.

**4:14** · What data should we use to train the rig inverse model?

**4:17** · If the model is for offline purposes, it is trained only using the data that we want to find rig parameters for.

**4:24** · This is possible because, at this point, the training is essentially self-supervised.

**4:28** · On the other hand, if the data that we want to find rig parameters for is not available at training time, the model should be trained using randomly augmented meshes.

**4:38** · The rig we use to develop and demonstrate this method is called FaceRig.

**4:42** · It is an internally-developed blendshape-based facial rig at Electronic Arts.

**4:47** · The proposed method makes no fundamental assumptions about the rig other than it being deterministic.

**4:52** · This being said, a blendshape-based rig has the advantage of lowering the dimensionality of the problem.

**4:59** · Let’s take another look at this method, applied on captured data.

**5:02** · Note that the rig parameters are smooth and as sparse as possible.

**5:11** · When the input mesh is noisy or out of manifold, the method returns rate parameters for the closest solution in mesh space according to the mesh loss.

**5:20** · This can be used to remove noise in the input data, whether captured or generated.

**5:25** · Here is a second example, but this time with input mesh data that was produced by a generative model.

**5:41** · Finally, here is an example of the method being applied to a different mesh and rig that does not use blendshapes.

**5:47** · The mesh animated by the original animation is virtually identical when animated by discovered rig parameters.

### Recap

**5:55** · To recap, we presented the first method of rig inversion that fully addresses the non-bijectivity of rigs.

**6:01** · We do so by having a method that outputs rig parameters that are optimized in mesh space.

**6:07** · As future improvement, we are working on using better mesh losses to support data that is more severely out of manifold.

**6:13** · We’re also working on using this technique to train generative models that directly output rig parameters instead of 4D mesh data, which greatly reduces the dimensionality of the generative problem.

**6:24** · We want to thank Mattias Teyes who contributed to this work, and thank you for watching this video.