
* Gradient descent
* Convex optimization 
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

* [Convex optimization](https://www.amazon.com/Convex-Optimization-Corrections-2008-Stephen/dp/0521833787/ref=sr_1_1?keywords=convex+optimization&qid=1570751960&sr=8-1) - an excellent theoretical book, needs to to be read alongside code to really make sense or else it can seem abstract on a first read
* [Convex.jl](https://github.com/JuliaOpt/Convex.jl) library to solve convex optimization problems
* [JuMP](https://github.com/JuliaOpt/JuMP.jl) Mamba: Markov chain Monte Carlo (MCMC) for Bayesian analysis in julia
* [Boosting]()