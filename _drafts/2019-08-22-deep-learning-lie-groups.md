---
title: Deep Learning on Lie Groups for Skeleton based action recognition
layout: default
---

# Lie groups for robotics

This post is a summary of a paper by [Huang et Al](https://arxiv.org/pdf/1612.05877.pdf). It's denser than the typical ML paper so I'm summarizing the core ideas while addding the appropriate background material you need to understand the paper.

If you stick with it you'll learn

1. How to represent a human skeleton
2. What are Lie groups and why they're great at representing motions
3. Lie group feature learning
4. How action recognition algorithms work

## How to represent a human skeleton

A skeleton can be represented as a graph \\(S = (V, E)\\) where \\(V = \{ v_1, ... , v_n \} \\) corresponds to joints or nodes of our graph and \\(E = \{ e_1, ... , e_n \} \\) corresponds to bones or edges of our graph. In 2D this definition is enough and in 3D we further add that the edges need to each have an orientation \\(\vec{n} \\).

Below is an image of a possible way to abstract a human skeleton by Marija Mihova.

![Skeleton](/assets/images/2019-08-22-deep-learning-lie-groups-skeleton.JPG){:height="70%" width="70%"}

Each bone has a parent which is the joint above it that is closest to it. The movement of any bone is started either at its parent joint or any of the bones above its parent joint. For non human skeletons, we can flexibily determine parent joints without resorting to the altitude heuristic.

## What are Lie groups and why they're great at representing motions

The presentation here closely mirrors [Lorenzo Sadun's fantastic youtube video](https://www.youtube.com/watch?v=uILYfubYxd0&t=429s)

The set of \\(n \times n\\) rotation matrices in \\( R^n \\) is called the Special Orthogonal Group \\(SO(n) \\) which is a matrix Lie group. 

Let's focus on 3D rotations as in \\(SO(3)\\) an its associated Lie algebra \\(so(3)\\)

\\(SO(3)\\) consists of all rotations in \\(R^3\\) and is equivalent to the set of \\(3 \times 3\\) orthogonal matrices with determinant equal 1. \\(A \\) is orthogonal if \\(A^T = A^{-1} \\)

\\(so(3)\\) consists of all \\(3 \times 3 \\) skew-symmetric real matrices which is just a fancy way of saying \\(A^T = -A\\)

A notational dump isn't useful unless \\(SO(3) \\) and \\(so(3)\\) have some useful properties which they do. And as we'll see next, those properties make them ideal for representing rotations and the infinitely small rotations.

> Theorem 1: If \\(R, T \in SO(3) \\) then \\(R^-1 \\) and \\(RT \in SO(3) \\) which means its a group

Now the mind blowing part

> Theorem 2: If \\(A \in so(3), \exp^A \in SO(3) \\)

Which provides us with the core intution if \\(SO(3) \\) represents a rotation then \\(so(3) \\) represents a tiny step towards that rotation or more specifically a differentiation.

While this seems like an innocuous theorem we can use it to create closed form solutions to the forward kinematics and inverse kinematics problems.

But first let's also introduce motions in the form of the Special Euclidean group \\(SE(3) \\) and its corresponding algebra \\(se(3) \\)

\\(SE(3) \\) is also known as rigid body motions or homogeneous transformation matrices because it can be used to either displace rigid bodies or represent changes of perspective in a continuous manner.

We will now show how Lie groups can be used to greatly simplify the forward and inverse kinematics problems. Instead of working with an entire skeleton we can work with a single arm where an arm is defined as a single bar, as in a skeleton where each node except the root has exactly one parent.

### Forward kinematics



Need a diagram of forward kinematics here

Julia code 

https://github.com/JuliaRobotics/RigidBodyDynamics.jl/blob/master/examples/3.%20Four-bar%20linkage/3.%20Four-bar%20linkage.jl



