---
layout: default
title: Why can neural networks solve so many different kinds of problems
---

Work in progress

# Why can neural networks solve so many different kinds of problems

I often have friends that don't work in Machine Learning but have some interesting startup ideas that ask me

> Can I solve X with Machine Learning

My answer usually goes something like

> Can you frame your problem as a supervised learning problem? i.e: do you have well defined inputs and outputs and if so sure you can solve it

I've found neural networks to also be a great educational tool to illustrate this point where you can pretty much encode any supervised learning problem as long as you know the sizes of your inputs and outputs.

All of the above diagrams involve minimizing f(output, prediction) but while introductory ML treatments often treat output and prediction as either real numbers or categories, the truth is that output and prediction can be be vectors which means they can be data structures which substantially opens up the scope of applications we can cover.

Many neural net architectures will use different constraints on the hidden layer to increase accuracy but what a neural net can express is mostly determined by its input and output dimensions so we'll be treating the hidden layers as a blackbox. All we need to know about these black boxes is that they "bias" our outputs towards favorable representations.

Can represent a neural network as some arbitray continuous differentiable function of input and output f(x) = y where x can be R, a vector, a tensor and same for y. Can also display a contin

![simple](/assets/images/simple.svg)


## Predict whether it will rain tomorrow

## Output an action in RL - Make a decision

## Given an image output another image

m*x -> m*n

## Given a song output an image

## Given a world in RL output a rotation

### Euler rotation
Output 3 real numbers

### Quaternion rotation 
Output 4 real numbers

## Output a ranking

### Either train classifier 

### Or  train a list generator

## Output a tree
Input is a node and left or right child and output is is another node. Need seperate memory for this

## Output a 3d model
List of n points. Think about how to do this while also adding edges

## Output 



### Next steps

If you're looking for more examples to motivate you, I'd recommend you try to answer the following
1. How can I model problems with unspecified input and output sizes? Google RNN for this, the key idea is feedback and state
2. How would things like self play in reinforcement learning work in this setting since you don't really have labeled data? You can bootsrap off of your current best estimate which to me is one of the coolest idea I've encountered in ML