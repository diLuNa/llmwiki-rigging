---
title: "Inverse Rig Mapping - Technical Directing - Animationsinstitut Filmakademie BW"
source: "https://www.youtube.com/watch?v=N5rSmC9WJlQ"
author:
  - "[[R&D_Filmakademie]]"
published: 2023-09-05
created: 2026-04-14
description: "Inverse Rig Mapping - Technical Directing - Animationsinstitut Filmakademie BWCurrent motion editing and synthesis methods work on the skeleton rather the rig which makes later editing by an animato"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=N5rSmC9WJlQ)

Inverse Rig Mapping - Technical Directing - Animationsinstitut Filmakademie BW  
  
Current motion editing and synthesis methods work on the skeleton rather the rig which makes later editing by an animator difficult since the skeleton data needs to be mapped onto the rig. This problem (known as "rig inversion problem") prevents the use of such technology in a production since solving this problem often involves creating custom, hard-coded solutions which are time-consuming and hard to maintain.  
  
The proposed toolset for Maya based on the paper "Learning an inverse rig mapping for character animation" is to map animation data from the skeleton to an arbitrary rig. With this system data-driven animation techniques could be used in a production and also combined with the work of an animator. The user only needs to provide a few rig poses which will then be used to learn the rig mapping to the system. After that the system predicts the individual rig attributes based on the animation data of the skeleton.  
  
This project was developed as part of the Technical Directing course at Animationsinstitut of Filmakademie Baden-Württemberg.  
  
Application deadline for courses starting in fall is February 15th.  
International students are welcome!  
  
Further information at technicaldirector.de  
https://animationsinstitut.de/  
https://www.filmakademie.de/

## Transcript

### Intro

**0:07** · thank you in animation character movement is meticulously crafted using an animation rig a complex system that controls the character's mechanics such as joints constraints and deformers through user-defined control parameters that can number in the hundreds however animation technology focuses on skeletons which creates challenges for integration with production mapping back to an animation rig to edit the animation requires complex tools or handwritten scripts that are time consuming and character specific based on the research paper learning an inverse rig mapping for character animation by Daniel Holden John Saito and taku komura the inverse rig mapping tool abbreviated irm was developed as part of the technical directing course at Film Academy bought in wurtenberg to fill this Gap irm aims to provide an efficient flexible workflow that works with any rig it achieves this by using machine learning to learn the correlation between rig control parameters and dependent joint parameters after training that the tool can predict these parameters based on the skeletal animation data the workflow for using the inverse rig mapping tool consists of several steps the first step is to create training data by adding control and Joint parameters and setting plausible ranges for each rig parameter random poses are generated Within These ranges to cover a wide range of motion using pytorch with G Pi torch the model learns the correlation between rig control and Joint parameters through a GPU accelerated gaussian process regression model it minimizes prediction error by iteratively adjusting internal parameters based on a user-specified learning rate and epics which takes time depending on data complexity in model hyper parameters we use the train model to map the skeletal animation back to our rig by defining the animated joints and their attributes collecting the animation data at each frame predicting the animated rig values and applying them to the rig the predicted animation of the rig now Loosely matches the animation of the skeleton the gap between the animated skeleton and the rig can be closed by adjusting the model's training data in hyper parameters please note however that there are still limitations to the accuracy of this mapping complex rigs with many parameters may present some challenges and the predicted rig animation may not perfectly match the skeletal animation \[Music\]