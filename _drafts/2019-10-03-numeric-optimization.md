---
layout: default
title: Numeric optimization
---

# Numerical optimization

> Once you know what you want, how do you optimize for it?

Optimization problems are formulated as

\\(\min f(x) \\)

\\(s.t \quad g_i(x) \leq b_i \quad \forall  i \\)

The goal is to minimize an objective function \\(f \\) while making sure that \\(i \\) different \\(g \\) functions are constrained by a variable \\(b_i \\). While this right now sounds abstract it's a very general framework we can use to express a large number of problems. Some examples

* A point in an interval: \\(f(x) = x\\) s.t \\(g(x) \leq 5 \\)
* Minimizing the negative is the same as maximizing \\(\min -f(x) = \max f(x) \\)
* Find the position of a particle in a physical system which minimizes total energy (conservation of energy): \\(\min E \\) s.t \\()


The examples above should have convinced you that we can think of

\\(\min f(x) \\)

\\(s.t \quad g_i(x) \leq b_i \quad \forall  i \\)

as

\\(\min goal \\)

\\(s.t \quad constraints = True \\)


This formulation makes it shocking how many problems we can formulate as an optimization problem and we'll come back to this formulation in the next chapter when we introduce Reinforcement Learning for control tasks.

While it's easy to formulate a problem as an optimization problem not all problems are efficiently solvable. Typically an efficiently solvable optimization problem is a convex optimization problem where \\(f, g \\) are convex.

In calculus you typically learn that to minimize some function \\(f \\) you take its derivative, set it to zero and solve for \\(x \\) \\(f'(x) = 0 \\). While this works for convex functions like \\(f(x) = x^2 \\) it won't work for other functions.

![convex-nonconvex](/assets/images/convex-nonconvex.png)

For the first function if you solve for x, \\(f'(x) = 0\\) you're only only ever going to get back a single point \\(A \\)
For the second function if you solve for x, \\(f'(x) = 0\\) you can get back on of the three points, \\(B \\) is neither a minimum nor maximum. \\(C \\) is a local minimum and \\(A \\) is a global minimum.

So how do we solve non convex problems? There's a few tricks but nothing is really guaranteed to work in a really satisfactory way. 

The two main approaches are 
1. Approximating a non-convex optimization as a convex one -> very innacurate
2. Trying different initializions for the solution space -> very slow

Convex functions have the desirable property that any local minimum is a global minimum.

More specifically a point \\(x^{\min} \\) is guaranteed to be a minimum of some function \\(f \\) if \\(f'(x^{\min}) = 0 \\) which is called the first order condition and if \\(f^2(x) > 0 \\) which is called the second order condition. In other words the first condition which you're probably already familiar with, is a necessary but not sufficient condition for finding minima.


In any optimization algorithm we're dealing with distances to a feasible set or an optimal solution but we have some flexibility in how to choose our distance functions. Distance functions are functions that take as parameters two points in our space. You're already familiar with different distance functions if you've ever used a GPS. There's a birdeye view distance between two points called the Euclidean distance function and there's the distance of the street level physical path between two points called the Manhattan distance

 We can also have discrete distance functions which have a combinatorial structure such as the "friendship proximity function" which assumes that the proximity between two people is the inverse of the total number of people they know in commmon. 

In particular there's a special class of distance functions called metrics which obey a few properties if we take \\(x_1, x_2, x_3 \in X \\) where \\(X \times X \\) is the domain of the metric. 

1. Non-negativity: \\(d(x_1, x_2) \geq 0 \\) -> negative distances don't make sense
2. Identity of indescernibles: \\(d(x_1, x_2) = 0 \Leftrightarrow x_1 = x_2 \\) -> two points are the same if they are at distance 0 from each other
3. Symmetry: \\(d(x_1,x_2) = d(x_2,x_1) \\) -> distance is the same from source to destination as destination to source
4. Triangle indequality: \\(d(x,z) \leq d(x,y) + d(y,z) \\) -> direct distance is the shortest distance between two points


# Gradient descent
Talk about this next

# Trust region absolute and relative improvement
* Lipschitz

Lipschitz continuous function are well behaved from an optimization standpoint because they put a bound on the how fast a continuous function can change. Specifically for a distance function.

\\(d(f(x_2) - f(x_2)) \\)

Lipschitz functions become important once you consider that during the process of gradient descent you're taking some initial guess at a minimum as \\(x_0 \\) and then at every step \\(i \\) you update according to \\(x_i = x_{i-1} - \epsilon h(.) \\) where \\(h \\) is our update function and \\(\epsilon \\) is the update step size. If a function has large spikes what will happen is that small changes in our parameters will cause huge changes in our output and make the training highly unstable. Unstable training means slow with weird predictions

# Multi objective learning
Suppose now you want to minimize not just one objective function \\(f \\) but \\(n \\) of them, we can index each of them using \\(f_i \\) where \\(i \in 1,2 \cdots n \\)

So how do we minimize \\(n \\) functions \\(f_1, f_2 \cdots f_n \\)

Theoretically this is not really possible since different functions will have different parameters that minimize them but we can decide the weight to give to each function and take a weighted sum of them and minimize that to get

\\(\min w_1 f_1 + w_2 f_2 + \cdots + w_n f_n \\)

# Supervised learning

I'm assuming you've read some sort of introduction to machine learning blog post or book you probably came accross an expression like Machine Learning tries to minimize the difference between  and maybe you've seen an expression like \\(\min f(x) - y \\) where 
* \\(x \\) is your data
* \\(f \\) is your model
* \\(y \\) is your labels

If we assume that we're working with the euclidean metric \\(l_2 \\) which is by far the most common one we get back the unconstrained least squares which you've used if you've linearized a bunch of points in a 2d plot on Excel for example.

\\( \|Ax - b\|_2^2 = x^T A^T A x - 2b^T Ax + b^Tb \\)

# Extra stuff
* Evolutionary algorithms (can just mention this in passing)
* bounding variance chebyshev and markov inequality

Suppose

In many cases we can't compute the derivatives explicitly and we resort to an iterative approach to compute

* Markov chain Monte Carlo

Once you know what your objective function is it's easy to find an optimizer for it in most situations. We can even use objective functions as a tool to shape the kind of behavior we want. For example we could have an objective function be responsible

I Have more ideas from this in the representation theory blog post

Up until last year I would have probably written this chapter in Python but I've seen switched to Julia and have been very happy with it. Julia is a first class scientific language and delving into optimization and numeric optimization will make it very clear why that's the case.

Topics that need to be covered
* Convex space and functions
* MEtrics L1, L2, L0 with pictures
* Trust region absolute and relative improvement
* Gradient descent
* Summary of different descent algorithms including both first order and second order ones
* Lipschitz and using it to traverse spaces more efficiently
* How to find good hyperparms. Use some sort of Bayesian model that repreesnts whta you know about the tasks. The above does sound really abstract which is why for the most part people either use the best hyperparams theyve seen in someone elses project or they spend millions of dollars on compute just brute forcing all the different hyperparms to see what's best (not great if you're an independent researcher)
* Evolutionary algorithms, they work fine - similar to a sort of random search over the space - not using any particular structure
* Constraints: very important for machine learning and physics problems - can be done using Lagrangian multipliers and need to talk about optimality conditions using KKT constraints. Constraints can be different rules we we'd like to encode in a learning problem
* Multi objective learning
    * Give a weight for each learning function
    * Take a vote
    * Ideas expanded on in detail in [Boosting](https://www.amazon.com/Boosting-Foundations-Algorithms-Adaptive-Computation/dp/0262526034/ref=sr_1_4?keywords=boosting&qid=1570752396&sr=8-4)



Need to also write a brief Julia tutorial including
* Types and composite types
* Unicode support, math keyboard, it looks like what math papers would use -> minimal path from research to application until we come up with better languages to encode these problems
* Easy function overloading
* adding packages is trivial and very modular
* Symbolic and automatic differentiation example code available in Algorithms for optimization book


## References
* [Algorithms for optimization](https://www.amazon.com/Algorithms-Optimization-Press-Mykel-Kochenderfer/dp/0262039427/ref=sr_1_3?keywords=convex+optimization&qid=1570751960&sr=8-3) beautiful book with concise explanations, code and figures - this was my favorite

* [Convex optimization](https://www.amazon.com/Convex-Optimization-Corrections-2008-Stephen/dp/0521833787/ref=sr_1_1?keywords=convex+optimization&qid=1570751960&sr=8-1) - an excellent theoretical book, needs to to be read alongside code to really make sense or else it can seem abstract on a first read. This is the most mathematically rigourous treatment of convex optimization problems that I know of. The problems are also of very high quality and will help you work through formulating various problems as convvex optimization problems
* [Convex.jl](https://github.com/JuliaOpt/Convex.jl) library to solve convex optimization problems
* [JuMP](https://github.com/JuliaOpt/JuMP.jl) Mamba: Markov chain Monte Carlo (MCMC) for Bayesian analysis in julia
* [Boosting]()