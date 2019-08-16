---
layout: default
title: Applications of Reversible Computing
---

# Applications of Reversible Computing

I first came across reversible computing back when I was helping organize a quantum computing seminar back in grad school. At the time I didn't think much of it, I knew that for some quantum mechanical reason gates had to be reversible but I didn't really appreciate why that was such a powerful idea at the time until I came accross reversible computing again when I was studying how automatic differentiation works in deep learning libraries like Tensorflow or Flux.

Fast forward 6 years and I can now tell you why I believe reversible computation is an extremely useful and practical feature to have in all sorts of different computational paradigms.

## What is reversible computation?

To make this discussion more concrete let's take a simple python function \\(f(a)\\)

{% highlight python %}
def f(a):
    return a + 1
{% endhighlight %}

This is the simplest kind of function we can invert (don't worry more interesting applications are coming next)

{% highlight python %}
def f_inverse(a):
    return a - 1
{% endhighlight %}


If you've used any sort of functional programming language or have read up on real analysis then you'll recognize\\(f\\) as being reversible if there exists a function \\(f^{-1}\\) s.t \\(f \circ f^{-1} = 1\\)

This is great and all but why should you care? I ask myself the same question whenever someone introduces me with new terminology. It's very fortunate that the number of applications is frankly staggering.

## List of applications

### Automatic differentiation

I am planning on writing an entire blog post on this topic but the general idea is that Automatic Differentiation is different from both numerical and symbolic differentiation.

Let's say you're designing a neural network architecture with billions of layers or whatever. You might even have some discrete functions in there, some control flow, you're going crazy cause you're trying to beat the SOTA.

It's easy to go crazy designing the forward step but now when you need to do backprop you need to compute these fancy derivatives which can be a pain for more complex architectures. Thankfully, libraries like Tensorflow, Pytorch and Flux just give you that for free essentially rendering computing derivatives as intereting as doing division in longform.

Also if you thought this was only possible for numerical code then you're in for a surprise, it's possible to design reversible turing machines to simulate an arbitrary application in a reversible manner.

### Distributed Computation

General distributed networks are bottlenecked by their communication costs so many paradigms eliminate communication entirely to provide certain guarantees. The challenge stems from the synchronization overhead of having several machines each with their own clock having to occasinally halt all productive computation so they can synchronize.

However, with reversible computation there is no need to synchronize because if a conflict is found the incorrect computation can be reversed

### Databases

In databases READS are EZ-PZ, they don't mutate any state. If people are only reading from a static database then you don't need to do anythign special to make sure people are reading the correct data.

However, WRITES is where things get tricky. If two people are writing to the same databases then it's possible for any of the two parties to READ stale data or even worse corrupt data.

To alleviate the WRITE problem some schemes eliminate WRITES entirely opting for APPEND only schemes and while this works in practice, it ends up constraining application developers.

Another solution to the WRITE problem is to wait for some window of time and then synchronize all WRITES to make sure there are no conflicts. The issue here is that this synchronization time can be quite long especially once you introduce many users to the system.

Yet another is to lock the database WRITES to a single user a time. Again this means most users are waiting a ton of time.

A reversible database means clients can just execute their WRITES immediately but if a conflict is later found we can reset the database to a non conflicting state and merge the changes.

### Reversible circuits

Reversible computing applies to both software and hardware. Similar to the famous Toffoli gate (fancy name for a NOT gate controlled by a special bit) in Quantum Computing you can design.

This becomes interesting once you consider that hardware often needs to wait on software to continue the results of different operations but if hardware can just go full steam ahead and correct its actions only if it mispredicted what software wanted then it becomes easier to implement.

If this sounds weird then you can compare it mentally to branch prediction and that's pretty much a must these days.


### Fault detection
Let's say you wanna make sure that a certain function \\(f\\) is deterministic. As in given an input \\(x\\) you always get the same output \\(y\\).

Today this is mostly done via check bits but instead you could take the output you get \\(y\\), apply \\(f^{-1}\\) and make sure you get \\(x\\).
 
## How to implement reversible computing

There are two core techniques and which one you pick will depend on your constraints 
1. Save a history of all variables - good when you have lots of storage
2. Save all inverse operations - good when you have lots of compute

## What's next?

If you enjoyed this post, I'd highly recommend you check out [Introduction to Reversible Computing](https://www.amazon.com/Introduction-Reversible-Computing-Chapman-Computational/dp/1439873402/ref=sr_1_1?keywords=reversible+computing&qid=1565943389&s=gateway&sr=8-1) by Kalyan Perumalla which goes over more applications and libraries that support these applications.

And stay tuned for a followup post on Automatic differentiation!