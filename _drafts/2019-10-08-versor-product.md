---
layout: default
title: Versor product
---

# Linear Algebra refresher

If you're like me, the first time you were introduced to linear algebra you were told something along the lines of.

A vector is a container with a bunch of values \\(v = [v_1, v_2 \cdots v_n] \\)

A matrix is a bunch of vectors stacked on top of each other

$\begin{bmatrix}a & b\\c & d\end{bmatrix}$

The determinant of a matrix is a scalar \\(ac - db \\) which represents the area spanned by the shapes of the rows or columns.


> Why are that those are the right definitions? Why do they only work for specific shapes? Is there an underlying geometric representation we're missing

Because your professors said so isn't a great justification. In the same that social scientists "debate" the merits of different political and economic policies, math also has various schools of thought. The Linear Algebra formalism became widespread especially after Maxwell publicized his equations but in parallel we had people like Grassman and Clifford work on different formalisms for space which make some operations much simpler.

Even though I'd been working with Linear Algebra professionaly for most of my life, I've always found some its operations confusing. In particular

1. Why does computing the determinant look so weird? Why does it only work for square matrices?
2. Why is it that \\(ab \neq ba \\)? If they're not equal then what's the relationship between them?
3. The cross product \\(a \times b = \|a \| \| b \| \sin(\theta) n \\) is used to find the area of the parallelogram spanned by the two vectors \\(a, b \\). Why do I need to use my fingers to figure out what \\(n \\) is and why doesn't the cross product work in dimensions higher than 3? Dimensions higher than 3 are not armchair philosophizing, in fact you use them all them the time whenever you work with a dataset with more than 3 columns.


## Exterior product


We'll define the exterior product as \\(a \wedge b \\) in some vector space \\(V \\) where \\(a, b \\) are vectors in \\(V \\). The exterior product needs to fulfill 2 properties
1. Antisymmetric: \\(a \wedge b = -b \wedge a \\)
2. Bilinear: \\(a \wedge (b + \lambda c) = a \wedge b + \lambda a \wedge c  \\)

And while these properties seem abstract, they show up fairly naturally in geometry and make sense once look at one example. Let's try to look at the algebra of areas of parallelograms with side lengths \\(a, b \\) and see if anything sticks out.

Can add pictures here

1. Double one of the sides:\\(Area(a, 2b) = Area(a, -2b) = 2 Area(a,b) \\)
2. Add to the length of one side: \\(Area(a, b + c) = Area(a,b) + Area(a,c) \\)

We can already see hints of Antisymmetry and Bilinearity so we'll make this intuition more formal if we now assume that \\(Area \\) represents an oriented surface.

1. \\(Area(a,b) = -Area(b,a) \\)
2. \\(Area(\lambda a, b) = \lambda Area(a,b)  \\)
3. \\(Area(a, b + c) = Area(a,b) + Area(a,c) \\)

Now let's replace \\(Area(a,b) \\) by \\(a \wedge b \\) to get

1. \\(a \wedge b = - b \wedge a \\)
2. \\( (\lambda a) \wedge b = \lambda (a \wedge b)   \\)
3. \\( a \wedge (b + c) = a \wedge b + a \wedge c \\)

And this shows us how \\(Area() \\) is a specific application of the wedge product \\(\wedge \\). However, there are tons of different applications

In linear algebra we typically think of vectors as matrices as containers holding elements of \\(\mathbb{R} \\) so an \\(n\\) dimensional vector holds \\(n \\) elements of \\( \mathbb{R} \\). Instead we could think of an \\(n \\) dimensional vector as a single element of \\(\mathbb{R}^n \\)

Any vector can be expressed in terms of the basis vectors \\(e_1, e_2 \\) of the space its in. So if we have two vectors \\(a, b \\) we can express

\\(a = a_1 e_1 + a_2 e_2 \\)
\\(b = b_1 e_1 + b_2 e-2 \\)

And if we take \\(a \wedge b = (a_1 b_2 - a_2 b_1) e_1 \wedge e_2 \\) which if you ignore the term with the basis vectors you end up with the familar formula for a matrix determinant.

The geometric product is then the sum of the wedge product and the inner product

\\(ab = a \cdot b + a \wedge b \\)

Show the matrix determinant here

## Why care about geometric algebra

Geometric Algebra is an ideal programming language for geometry problems which includes anything involving robotic simulations, optimization and machine learning.

Let's say you want to find the intersection point of
* a line \\(l \\) and a sphere \\(s \\): \\(l \wedge s \\)
* two lines \\(l_1, l_2 \\): \\(l_1 \wedge l_2 \\)
* two spheres \\(s_1, s_2 \\): \\(s_1 \wedge s_2 \\)
* three spheres \\(s_1, s2, s3 \\): \\(s_1 \wedge s_2 \wedge s_3 \\)
* two spheres \\(s_1, s_2 \\) and a plane \\(p \\): \\(s_1 \wedge s_2 \wedge p \\)
* Doesn't matter what the shapes are or how many of them \\( \wedge \\) will work

Because geometric algebra has more elegant algebra for intersections this can help us create tiny libraries that are more expressive than most physics engines out there today. Most existing game engines were a monumental effort, some requiring thousands of people to collaberate but if you need a tenth of the usual code to write a game engine in geometric algebra that means you need a tenth amount of the effort to get something working AND you also have an easier to debug and more interpretable language for all your computational geometry problems. 

The main operation in geometric algebra is a rotation about a line \\(L \\) through the origin which can be represented as a rotor \\(R = e^{\frac{\phi}{2}L} \\) 


Because geometric algebra has more elegant algebra for intersections and other primitive geometric operations this can help us create tiny but full fledged libraries for geometry. With more expressive and concise code we can express more complicated geometric operations but we still need to make sure geometric algebra is as performant as its linear algebra counterparts. 

## Calculating intersections

Another area where Geometric Algebra shines is in computing intersections of different surfaces and shapes. This comes up a lot in physics engine where you need to be able to tell whether two objects collide with each other to either move them according to the laws of your physics engine.

So suppose that \\(a, b \\) are both spheres then we can describe their intersection using

\\(a \wedge b \\)

## References

* [Linear Algebra Done Right](https://www.amazon.com/Linear-Algebra-Right-Undergraduate-Mathematics/dp/3319110799/ref=sr_1_1?keywords=linear+algebra+done+right&qid=1570576924&sr=8-1) is in my mind the best introduction to theoretical aspects of Linear Algebra that I've read. It really made the idea of interpreting Matrices as linear maps really obvious to me
* [Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares ](https://www.amazon.com/Introduction-Applied-Linear-Algebra-Matrices/dp/1316518965/ref=pd_sbs_14_6/131-4946721-1001121?_encoding=UTF8&pd_rd_i=1316518965&pd_rd_r=d709bbc8-8dbd-4fcf-8eec-c71269c9779d&pd_rd_w=31Q4B&pd_rd_wg=CBGVR&pf_rd_p=d66372fe-68a6-48a3-90ec-41d7f64212be&pf_rd_r=S5YJ3AAJ9H10G8C1NZA3&psc=1&refRID=S5YJ3AAJ9H10G8C1NZA3) is another great traditional linear algebra reference that focuses on numerical linear algebra and applications to optimizations and machine learning. It comes with a free online companion of all the algorithms in Julia which is about as long as the main book.
* [Linear algebra via Exterior products](https://www.amazon.com/Linear-Algebra-via-Exterior-Products/dp/140929496X/ref=sr_1_1?keywords=linear+algebra+via+the+exterior+product&qid=1570577186&s=books&sr=1-1) is an excellent reference that reproves all the main theorems of Linear Algebra using the exterior product.
* [Geometric algebra for computer science](https://www.amazon.com/Geometric-Algebra-Computer-Science-Revised/dp/0123749425/ref=sr_1_8?keywords=geometric+algebra&qid=1570577296&s=books&sr=1-8) is a good second book on geometric algebra. One amazing thing about this book is that goes over all the details around building an efficient geometric algebra library which the authors provide alongside a rich rendering experience.
* [Ganja.js](https://github.com/enkimute/ganja.js) is a fully fledged geometric algebra library in Javascript. You'll learn a lot by checking out the demos and the README.
* [The power of Geometric Algebra Computing for Mathematica](https://www.youtube.com/watch?v=1cWGV2qaBHo) is a short talk that discusses some applications of geometric algebra.
* [Joan Lasenby on Applications of Geometric Algebra in Engineering](https://www.youtube.com/watch?v=ikCIUzX9myY&t=1005s)
* [An Introduction to Geometric Algebra over R^2](https://bitworking.org/news/ga/2d) which is an excellent first introduction to Geometric Algebra. I strongly suggest you also inspect source when checking the animations to see how everything works
* [Foundations of Game Engine Development, Volume 1: Mathematics](https://www.amazon.com/Foundations-Game-Engine-Development-Mathematics/dp/0985811749) which covers all the math you need for 3D graphics, the last section of the book is dedicated to Cliford and Grassmanian algebras. This book is concise and clear with loads of good illustrations
* https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?referer=&httpsredir=1&article=7943&context=etd_theses
* http://www.jaapsuter.com/geometric-algebra.pdf