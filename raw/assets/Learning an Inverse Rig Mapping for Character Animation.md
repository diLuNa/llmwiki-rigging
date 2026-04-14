---
title: "Learning an Inverse Rig Mapping for Character Animation"
source: "https://theorangeduck.com/page/learning-inverse-rig-mapping-character-animation"
author:
published:
created: 2026-04-14
description: "Computer Science, Machine Learning, Programming, Art, Mathematics, Philosophy, and Short Fiction"
tags:
  - "clippings"
---
```
ijjooooiiiiiijjjjjjjjoooiiiiiiiiijjji11jjoiiiiiiiiiiiii111111111111111111111111111111n1111
ijjjjjjooiiiiiijjjjjjoiiiiiiiiiiijji11jjoiiiiiiiiiiiiii11111111111111111111111111111111111
1iiijjjjjjoi11ijjjjjjoiiiiiiiiiiaji11jjoiiiiiiiiiiiiiiijjjjj111111111111111111111111111111
1iiiiiijjjjjjjj                                                           1111111111111111
111iiiiiiiijjjj  Learning an Inverse Rig Mapping for Character Animation  11ii111111111111
11111jjiiiiijjj                                                           11jjiiii11111111
111111jjjjjijjjjjooooojjoooojjj11jjii1i1nnnoojjjjiii111nnniiiiiiiin111111111iiijjiiii11111
11111oojjjjjjjjjjjooooiiiiojjj11jjoiiiiinnnjjjjii111111niiiiij111111111111111111iii1111111
11111111ooojjjjoooooooiiiiaoo111joiiiiiinnijjii1111iiijiijj1111111111111111111111111111111
```

---

### 27/08/2015

This year I presented a paper at [SCA](http://www.siggraph.org/attend/events/sca-2015) called *Learning an Inverse Rig Mapping for Character Animation*. In this paper we explain a technique for inversing an animation rig to transfer skeletal animation into keyframe data which animators can then edit. You can [download the paper here](http://theorangeduck.com/media/uploads/rigmapping.pdf).

[Webpage](https://theorangeduck.com/page/learning-inverse-rig-mapping-character-animation) • [Paper](https://theorangeduck.com/media/uploads/rigmapping.pdf) • [Video](https://www.youtube.com/watch?v=P4-0esMIvuo) • [Slides](https://theorangeduck.com/media/uploads/rigmapping_slides.odp)

![](https://www.youtube.com/watch?v=P4-0esMIvuo)

**Abstract:** We propose a general, real-time solution to the inversion of the *rig function* - the function which maps animation data from a character's rig to its skeleton. Animators design character movements in the space of an animation rig, and a lack of a general solution for mapping motions from the skeleton space to the rig space keeps the animators away from the state-of-the-art character animation methods, such as those seen in motion editing and synthesis. Our solution is to use non-linear regression on sparse example animation sequences constructed by the animators, to learn such a mapping offline. When new example motions are provided in the skeleton space, the learned mapping is used to estimate the rig space values that reproduce such a motion. In order to further improve the precision, we also learn the derivative of the mapping, such that the movements can be fine-tuned to exactly follow the given motion. We test and present our system through examples including full-body character models, facial models and deformable surfaces. With our system, animators have the freedom to attach any motion synthesis algorithms to an arbitrary rigging and animation pipeline, for immediate editing. This greatly improves the productivity of 3D animation, while retaining the flexibility and creativity of artistic input.