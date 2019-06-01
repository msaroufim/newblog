---
title: Representation Theory for Robotics
layout: default
---

Work in Progress

# Representation Theory for Robotics
This goal of this post is to teach you how to efficiently represent the state of a robot with as little memory as possible. The primary application of this is that we can then train Reinforcement Learning (RL) algorithms orders of magnitude faster. One of the main reasons isn't the de facto standard in industrial applications is that the sample complexity i.e: the number of runs an agent needs to do is still prohibitive. 

> So how can we RL on a budget?

## Pixel based reprentations
Let's pick a simple example, try out different representations and compare them.

Suppose you have a 2d robot arm which is made up of two limbs and the goal is to reach a red ball.

A trivial representation is all the pixels on the screen. The goal then becomes given all the pixels on the screen what should the agent do next to maximize its reward?

Let's assume the area of an image is 100x100px. The total size of the state is then 100x100x3x255. 

Unfortunately that doesn't even work. The issue with it that given a photograph you don't know which motion led you there. Let's say we're trying to teach an agent how to play Super Mario Bros and we took a snapshot of Mario in the air. How do you know whether he's jumping or falling?

To solve this issue pixel based representations will stack several frames on top of each other. Theoretically you would only need 2 frames but in practice I've seen 4 be a lot more common.

Damn! So now we have a state space of size 100x100x3x255*40 which is kind of insane when you stop and think about it.

> OK so what can we do to make the state space smaller for pixel based representations?

Turns out there's a bunch of good ideas used in practice
1. Crop world to only include salient information. If we were to look at the tensor representation of our world, you'd notice most of it would be just 1 corresponding. Cropping litterally corresponds to taking the center part of the tensor representing the world
2. Grayscale the world. We don't need all 3 RGB channels. The red goal could be identified as a circle as a circle instead so the color isn't essential information to the task. We grayscale by averaging all 3 RGB values of a pixel.
3. Experiment with just stacking 2 frames vs 3 vs more and see what actually works best on your specific problem
4. Similar idea to grayscale is to use some sort of filter as a preprocessing step for e.g an edge detector which should again make your state tensor sparser

> So should we just use pixel based representations?

No, but they're good as a baseline since you don't need to create any sort of domain specific logic. While pixel representations are trivial to work with and work for games like Atari games. They are incredibly inneficient because of how large they are. Tricks help to an extent but are a symptom that maybe we're not working with the right representation. 

> So the next natural question is what is a better representation? Which brings us to Model based representations.

## Model based representations
Let's go back to our 2d robot arm example. You'll notice that it consists of 2 rectangles on an xy plane and there's a goal represented as a circle.

So a first step to represent this could be the 4 corners of each rectangle and the center of the circle with its radius that gives us
1. 8 points total for the rectangles with each point represented as 2 values one for the x coordinate and another for the y coordinate
2. 2 values for the circle center and one value for the radius

Summing everything up we can represent a given state for this 2d robot arm with 19 values. Not too bad.

> But wait a minute, how do you represent velocities?

Well in this case we need exactly 2 frames only since we can deduce the velocity of an arm by looking at how much it moves within 1 frame and as long as acceleration is constant we should be good to go.

> Can we do better than 19 values?

We can reprent the rectangles in an alternate way. As opposed to representing a rectangle as 4 points we can represent it instead as
1. The center of the rectangle. 1 point so 2 values
2. The height and width of the rectangle so 2 values
3. A rotation which is just 1 value for the angle

Summing everything up we can represent each rectangle with 5 values instead of 8 so we can represent the entire state of the world with 13 values instead of 19.

> Can we do better?

Maybe but it does feel like we're getting into some weird algebraic territory here.

> Can't I just use some algorithm to learn the best representation for me?

Glad you asked, let's move on.


## Learning a state representation
One of the challenges with creating our own representation is that we need a lot of domain knowledge around what constitutes a good representation, which features are important and which are not for the task at hand.

Techniques for learning state representations fall into two major buckets
1. Compression
2. World models

Regardless of which method you use the way to best evaluate it is to see how well your agent does on the full task while only being trained on the learned state representation. There are other evaluation techniques that try to make sure that the geometric properties of the space are "nice" so we are seeing a resurgence of interest in techniques that measure the quality of embeddings.

### Compression for state representations
The idea here is a simple one. Take any model based or pixel based state representation and run it through an algorithm like PCA or your other favorite dimensionality reduction algorithm.

In the case of PCA for e.g, you can decide how many dimensions your state should have. It's unclear how much you could compress a priori but the best way to do it is to just benchmark it. As in try PCA with output dimensions of 2, 3, 4, 5... and see how well your agent trained on this compressed representation does on the full task at hand.


### World models
World models have recently become more fashionable and I personally find them to be an extremely exciting research development. The main idea is that we can learn via gradient descent a compressed representation by backpropagating an error between how we predict the world will act and how it actually did.

Specifically we'll be talking about forward and reverse models

1. Forward model: \\(s_t' = f(s_t, a_t; θ) \\)
2. Reverse model: \\(a_t = g(s_t, s_t'; θ) \\)

Both kinds of models can be learned in the same manner using an autoencoder. The beautiful thing about the Reinforcement Learning setting is that we can generate our data, so what an autoencoder effectively does is try to guess what the next state will be in the case of the forward model or which action was made to end up in some state in the case of the reverse model and its guess can be corrected by what actually ends up happening. 

> Whoah man...

We can compress the world by deciding on the dimensionality of the output. We learn the weights of the autoencoder using your favorite gradient descent method where we're minimizing in the standard manner \\f(\hat{y}, y)\\.

### Biasing world models
Reward functions from RL can be used as an additional signal but are not strictly necessary. What makes it compelling though is that we can bias our world models  in multiple ways to make them more robust and useful to us. Some examples are:
* Slowness: Small changes in state locally
* Variability: Representation should spend more space describing moving objects
* Proportionality: state changes by roughly same magnitude for any action
* Repeatability: making the same change to same state should result in the same state



## Next steps
For the most part in this blog post we've focused on how to get small representations for more efficient learning but there are other worthwhile goals to accomplish. For example, some representations do not have singularities in them which makes training a Reinforcement Learning algorithm on them more stable and this can be reasoned through using some tools from perturbation analysis and chaos theory. Another idea is to use representations which encode some symbolic reasoning but as far as I'm concerned that idea is less proven in practice. 

I'm planning on writing more about this in an upcoming blog post so stay tuned if you've enjoyed this one and as always feel free to email me with questions

## BixTex 

If you've found this post useful and would like to cite it in your work please use the following


{% highlight scheme %}

@misc{MSRTR,
  author = {Mark Saroufim},
  title = {A survey of Representation Theory for Robotics},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/msaroufim}
}

{% endhighlight %}
