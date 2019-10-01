---
layout: default
title: Lagrangian mechanics - how to turn physics into an optimization problem
---

# Lagrangian mechanics - how to turn physics into an optimization problem

Doesn't \\(F = ma \\) solve everything? Seems like all the smart people are thinking about stuff like quantum field theory or string theory. Turns out there's still lots of interesting work going in classical mechanics.

The main idea we'll be exploring with Lagrangian mechanics is whether its possible to do physics in a coordinate invariant manner. This is important because some problems become much simpler or take less parameters to describe depending on the representation. A tight coupling between the representation and the simulation behavior of a physical environment means we'll be less likely to experiment with novel representations.


![pendulum](/assets/images/pendulum.png)

Let's take as an example the position of the center of a ball fixed to the wall via a wire - a pendulum. We can encode this position in one of two different manners
1. Cartesian coordinates: where we keep track of the \\(x, y \\) locations of the ball on some grid whose origin we need to define
2. Polar coordinates:  where we keep track of the length of the wire \\(l \\) and the angle \\( \theta \\) that the wire makes with the normal vector coming out of the ceiling

The polar coordinates in this example have more desirable properties than the cartesian coordinates
* Polar coordinates are invariant to translation: two identical pendulums at different locations in space will be indistinguishable
* Given a pendulum position at time \\(t \\) there's only 3 possible positions the pendulum can take at time \\(t + 1 \\), we can end up in only of \\( [(\theta, l), (\theta + \epsilon), l, (\theta - \epsilon)] \\)
* \\(l \\) is invariant because of the previous point

That said it's still possible to study this problem with plain old Newtonian mechanics, we just have to be comfortable with \\(\sin \\) and \\(cos \\) since there is a one to one correspondence between cartesian and polar coordinates.

### From polar to cartesian

\\(x = l \times \cos(\theta) \\)

\\(y = \times sin(\theta) \\)

### From cartesian to polar

\\(l = \sqrt(x^2 + y^2) \\)

\\( \theta = \tan^{-1} \frac{y}{x}\\)

However, let's stay we're studying a double-pendulum or \\(n \\)-pendulum then we end up with trigonometric expressions that don't look entirely trivial.

Lagrangian mechanics are about studying the invariants of a physical system regardless of the choice of representation.

## Lagrangian process

1. Construct an action function that gives us a way to distinguish realizable motions from others
2. Action function stationary only on path describing realizable motion
3. Action is integral of Lagrangian
4. Come up with ODEs that we then solve

## Lagrangian benefits

1. Coordinate free
2. Don't need to work with individual particles
3. Simpler, more efficient?
4. Helps find conservation laws (if independent of time means there is conservation of energy)

## Topics to cover
* Configuration spaces
* Principle of stationary action
* Euler lagrange equations
* how to find lagrange
* noether's theorem
* constraints as coordinate transformation
* nonholonomic constraints
* coordinate transforms
* canonical perturbation theory


# Newtonian Mechanics

Newtonian Mechanics describes the next position of a system in terms of the current positions, velocitites and accelerations of each of the particles of the system.

Newtonian mechanics are summarized by the famous 3 laws of motions. For what follows we only need to remember the second law of Newton.

Second Law: \\( F = m \ddot x \\) where
* x represents the position
* m represents the mass
* each dot on top of the x represents a derivative with respect to time

A conservative force can represented as the gradient of a potential and suprisingly enough most forces in the universe are conservative. A famous exception is friction. If a force is conservative then we can represent it as the gradient of a potential so we can rewrite the second law of Newton as 

\\(m \ddot x = - \frac{\partial}{\partial x}P \\)

where \\( P \\) is the potential function

Note that this is not inventing new physics, this is just a reformulation of Newton's second law but the primary advantage is that we can work in a coordinate independent manner. This is actually an incredibly important property because coordinate changes can often drastically simplify an expression e.g: Lie groups for single bar linkage problem. In some sense if we think of the laws of physics as code, the newtonian formulation has an unwanted coupling between the simulation logic and the coordinate system while Lagrangians decouple them entirely. It's also worth noting that Lagrangians can be found in many areas of modern physics such as relativity and quantum mechanics but they're interesting enough even in the classical mechanics domain to study on their own.

CODE EXAMPLE HERE




# Lagrangian Mechanics

Lagragian is an alternate formulation of Newtonian Mechanics and while in this tutorial we'll only be talking about classical mechanics, Lagrangians can be found in all areas of physics ranging from electromagnetics to quantum mechanics and relativity.

Instead of predicting the next position based on the current parameters of the system, the goal is to predict the entire path that a system will take and we call this path the configuration path. We can think of all possible configuration paths as occupying their own \\(n \\) dimensional space \\(M \\) and our goal is to find the specific configuration path that would fulfill the principle of least action i.e: minimize action.


The motion of a system \\(S \\) can be described by the positions of each particle in that system at every timestep where
* \\(N \\) is the total number of particles
*  \\(T \\) is the total number of timesteps
*  \\(p_i^j \\) represents the position of the \\(i \\)'th particle at timestep \\(j \\).

  $$ S = \begin{bmatrix} p_1^{1} & p_1^{2} & \dots  & p_1^{T}  
  \\ p_1^{1} & p_1^{2} & \dots  & p_1^{T}  
  \\ p_2^{1} & p_2^{2} & \dots  & p_2^{T}  
  \\ \dots & \dots & \dots  & \dots 
  \\ p_1^{N} & p_N^{2} & \dots  & p_N^{T}  
  \\  \end{bmatrix} $$

Lagrangian \\(L \\) is defined as the difference between the kinetic energy \\(K \\) and potential energy \\(P \\). 

Kinetic energy is the scalar associated with the vector of motion and potential energy the scalar associated with the vector of location.

\\(L = K - P = \frac{1}{2}mv^2 - P \\)

The kinetic energy of a system is always the same and the potential energy is a function of the domain we're working with. So some examples:

It's worth noting a couple of things here
1. We don't have any vectors in our expression
2. We have no dependence on a specific coordinate system
3. We are not explicity modeling the forces and counterforces at each point (what you did in high school with normal vectors and whatnot) - we are just plugging in the values for potential and kinetic energy and getting back the correct equations of motion

EXAMPLES HERE

## Lagrangian optimization - Machine Learning interlude

If you squint you'll recognize this formula as being similar to the way we define the Lagrangian in Machine Learning

\\(L' = f(x) + \lambda g(x) \\)

where
* \\(f \\) is the function we're looking to minimize
* \\(g \\) is a constraint s.t \\(g(x) = 0 \\)
We didn't define P intentionally because it depends on the system we're working with. Let's assume the system we're working with is a ball bouncing around an apartment then we could define \\(P = m g h \\) where
* m is mass
* g is the gravitational constant
* h is the height from the floor

In the variational formulation we can free ourselves from having to work with specific particles but also free ourselves from the choice of a coordinate system.


## Lagrangian principle of least action

Let's define the action \\(S = \int_a^b L \,dt  \\) and our goal is to minimize \\(S \\) which will give us the path of least action. The path that an object will take to reach a given position in space is the one that minimizes action. This is very similar to the way light takes the shortest path between two possible points, in fact you can derive refraction and reflection from the principle of least action. Great! Let's be more specific about how we'll find the path.



## Noether's theorem

If a coordinate does not appear in the Lagrangian of a system then it's a velocity is a conserved quantity



# Next steps
Hopefully this tutorial made you appreciate how powerful Lagrangians are and encourages you to take a look at deeper applications of Lagrangians in Quantum Mechanics and Relativity. A good place to start would be these excellent textbooks which among other things will introduce you to conservation laws via symmetry, Lie groups and Hamiltonian mechanics.
* [Physics from Symmetry](https://www.amazon.com/Physics-Symmetry-Undergraduate-Lecture-Notes/dp/3319666304/ref=as_li_ss_tl?ie=UTF8&qid=1519141872&sr=8-1&keywords=physics+from+symmetry&linkCode=sl1&tag=physfromsym-20&linkId=b86805feb0c3da1f89c0a34d3e50a0a7) 
* [Structure and Interpretation of Classical Mechanics](https://www.amazon.com/dp/0262028964/)
* [Gauge Fields, Knots and Gravity](https://www.amazon.com/gp/product/9810220340/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1)
* [MathPhysicsBook](https://www.mathphysicsbook.com/)


And of course email/tweet me if you'd like me to elaborate on something in a further blog post.

# Extra references
* http://www.physicsinsights.org/lagrange_1.html
* http://www.macs.hw.ac.uk/~simonm/mechanics.pdf
* http://www.physicsinsights.org/shortest_path_picture.html
* http://docs.juliadiffeq.org/stable/tutorials/ode_example.html
* https://www.youtube.com/watch?v=MIBfKJHMWHU
* https://brilliant.org/wiki/lagrangian-formulation-of-mechanics/
* https://en.wikipedia.org/wiki/Noether%27s_theorem
* https://blog.jle.im/entry/hamiltonian-dynamics-in-haskell.html


### Notes from reading https://brilliant.org/wiki/lagrangian-formulation-of-mechanics/



Newton's laws are written in terms of vectors that are easiest to manipulate in Cartesian coordinates. While this is fine in some cases in others like double pendulum the notation starts getting in our way. Lagrangian mechanics let us rewrite Newton's laws with scalars instead of vectors. Which frees from the artifacts of working with poorly chosen coordinate systems.

Issues with Newtonian Mechanics
1. Vector representation is difficult to work with
2. Number of interactions between particles exploded 
3. Encoding constraints is explicit (not sure what this means yet)

d'Alembert principle