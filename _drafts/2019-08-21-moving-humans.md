---
title: Moving humans
layout: default
---

# Moving humans: An illustrated guide

![apple reacher](/assets/images/apple-reach.png)

Humans live in a 3D world (4+ depending on who you ask) but before we talk about how to move in 3D it's worth investigating how things work in the 2D world like the one the image above lies in.

We also don't want to deal with the full complexity of the human body so we'll just limit ourselves to an X-ray skeleton of the human body where the dark dots represent the joints and the edges connecting them represent bones.

![apple reacher skeleton](/assets/images/apple-reach-skeleton.png)

Now if we strip away the skin we're left with what looks like a graph.

![apple reacher skeleton only](/assets/images/apple-reach-skeleton-only.png)

You can represent any skeleton as a graph where the vertices \\(V \\) is the set of joints and the set of edges \\(E \\) is the set of bones. This simplification will help us build precise mathematical models.

Here's another graph that you may recognize.

![hand](/assets/images/hand.png)

# How to represent the position of joints 
In the above image we assumed that all joints are the same but that was kind of a lie. The human body has 6 different kinds of joints but we'll again limit ourselves to studying revolute joints are joints that let you in a pure rotation.





# How to represent a rotation

## Rotations in 2d

Any rotation in \\(\mathbb{R}^2 \\) can be represented with a complex number. 

Revolute joints can only rotate so their movement can be represented with a complex number

\\(z = \cos(\theta) + i \sin(\theta) \\) where \\(i^2 = 1 \\)

If we multiply \\(z \\) by the position of a point \\(p = a + ib \\) before a rotation then we get

\\(z * p = (\cos \theta + i \sin \theta)(a + ib) = a \cos \theta - b \sin \theta + i(a \sin \theta + b \cos \theta) \\)

If you stack the real part on top of the imaginary part then you get back a rotation in matrix form. 

\begin{pmatrix}
\cos \theta & - \sin \theta \\ \newline
\sin \theta & \cos \theta 
\end{pmatrix}

The center of the circle represents the revolute joint and the edge coming out of the circle at an angle \\(\theta \\) represents a bone. 

![imaginary plane](/assets/images/imaginary-plane.png)

2d rotations have a couple of interesting properties

* They can composed with the multiplication operation \\(e^{i \theta} e^{i \phi } = e^{i (\theta \phi)} \\)
* The order in which they are composed doesn't matter \\(e^{i (\theta \phi)} = e^{i (\phi \theta )} \\)
* Rotations are invertible with the division operation 
\\(e^{i \theta} / e^{i \theta} = 1 \\)

These are all nice properties and we'd like to keep them when we move to 3d but we're unfortunately going to lose out on commutitativity.

In practive it's important to note that the joint is not unconstrained so because of physical constraints of the skin and other bones a revolute joint will be constrained to a fraction of the total imaginary plane, highlighted below.

![constrained circle](/assets/images/constrained-circle.png)


## Rotations in 3d

Given that it took a 2d number to represent 2d rotations you would expect a 3d number to represent 3d rotations. However, it takes 4 numbers to describe a 3d rotation and we call this structure a quaternion.

TALK ABOUT QUATERNIONS AND WHY THEYRE NEEDED

Euler angles vs quaternions https://stackoverflow.com/questions/8919086/why-are-quaternions-used-for-rotations

Even though we are storing an extra bit of information we end up with faster algorithms that have more built in structure.

### Rotations in 3d are non commutative

Rotations are unfortunately non commutative or in other words if \\(R \\) and \\(Q \\) are two different rotation matrices then \\(RQ != QR\\) or in other words the order in which you apply rotations matters. An example wil cement this in your brain forever. I've borrowed the presentation from [Arthur](https://math.stackexchange.com/questions/2016937/why-are-rotational-matrices-not-commutative)

Feel free to bring out a dice for reference. For reference, here's what a 3D dice looks like unrolled in 2D.

![2d-dice](/assets/images/2d-dice.png)

Next we're going to pick an initial configuration where 1 is on top and we are facing 2 and 3. We have two rotations "Flip left side up" and "Turn 90 degrees clockwise" and apply them in different orders and look at the outcome.

![3d-dice](/assets/images/3d-dice.png)



# IK vs FK




# Next steps
If you've enjoyed this please let me know. Email me your questions and what kind of tooling you'd want to start designing robots at home.

# References

* [Picture of all the human body joints](https://www.google.com/search?q=types+of+joints+of+human+body&rlz=1C1GCEA_enUS749US749&sxsrf=ACYBGNQ9xeYGlxS8htwANyTrOdSgdWpI6w:1568971975562&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjL9o-KjN_kAhVLLK0KHVrpDjMQ_AUIEigB&biw=2560&bih=1280#imgrc=jtkhTs5G1ZG1QM:)