---
layout: default
title: Why can neural networks solve so many different kinds of problems
---

Work in progress

See if interface of either Flux.jl or Keras make the input and output sizes really obvious




# Why can neural networks solve so many different kinds of problems

I often have friends that don't work in Machine Learning but have some interesting startup ideas that ask me

> Can I solve X with Machine Learning

My answer usually goes something like

> Can you frame your problem as a supervised learning problem? i.e: do you have well defined inputs and outputs? Do you have some structured data (or some way to collect it) with examples of inputs and labels of their outputs? if so sure you can solve it

I've found neural networks to also be a great educational tool to illustrate this point where you can pretty much encode any supervised learning problem as long as you know the sizes of your inputs and outputs.

All of the above diagrams involve minimizing f(output, prediction) but while introductory ML treatments often treat output and prediction as either real numbers or categories, the truth is that output and prediction can be be vectors which means they can be data structures which substantially opens up the scope of applications we can cover.

Many neural net architectures will use different constraints on the hidden layer to increase accuracy but what a neural net can express is mostly determined by its input and output dimensions so we'll be treating the hidden layers as a blackbox. All we need to know about these black boxes is that they "bias" our outputs towards favorable representations.

Can represent a neural network as some arbitray continuous differentiable function of input and output f(x) = y where x can be R, a vector, a tensor and same for y. Can also display a contin


Let's consider a concrete example in Keras

```python
# Multilayer Perceptron
from keras.layers import Input
from keras.layers import Dense
visible = Input(shape=(10,))
hidden1 = Dense(10, activation='relu')(visible)
hidden2 = Dense(20, activation='relu')(hidden1)
hidden3 = Dense(10, activation='relu')(hidden2)
output = Dense(1, activation='sigmoid')(hidden3)
model = Model(inputs=visible, outputs=output)
# summarize layers
print(model.summary())
# plot graph
plot_model(model, to_file='multilayer_perceptron_graph.png')
```

Print the model definition

In the above example the input is of size 10 and the output of size 1

Let's refactor the above example


```python
# Multilayer Perceptron
from keras.layers import Input
from keras.layers import Dense
visible = Input(shape=(10,))
hidden1 = Dense(10, activation='relu')(visible)
hidden2 = Dense(20, activation='relu')(hidden1)
hidden3 = Dense(10, activation='relu')(hidden2)
output = Dense(1, activation='sigmoid')(hidden3)
model = Model(inputs=visible, outputs=output)
# summarize layers
print(model.summary())
# plot graph
plot_model(model, to_file='multilayer_perceptron_graph.png')
```


```python
from keras.layers import Input
from keras.layers import Dense

def create_network(input_size, output_size):
    visible = Input(shape=(input_size,))
    hidden1 = Dense(10, activation='relu')(visible)
    hidden2 = Dense(20, activation='relu')(hidden1)
    hidden3 = Dense(10, activation='relu')(hidden2)
    output = Dense(1, activation='sigmoid')(hidden3)
    model = Model(inputs=visible, outputs=output)
    return model
    
model = create_network(10, 1)
# summarize layers
print(model.summary())
# plot graph
plot_model(model, to_file='multilayer_perceptron_graph.png')
```

Now the input and output sizes are parameters we can control

So far we've limited ourselves to thinking about inputs and outputs as sizes or dimensions but we can also think of them as types in the programming language sense. So we could try a notation that looks like sets of sets.

```python
from keras.layers import Input
from keras.layers import Dense

def create_network(input_size, output_size):
    visible = Input(shape=(input_size,))
    hidden1 = Dense(10, activation='relu')(visible)
    hidden2 = Dense(20, activation='relu')(hidden1)
    hidden3 = Dense(10, activation='relu')(hidden2)
    output = Dense(1, activation='sigmoid')(hidden3)
    model = Model(inputs=visible, outputs=output)
    return model

inputs = [[5,10], [5]]
outputs = [[1], [20]]
model = create_network(inputs, outputs)
# summarize layers
print(model.summary())
# plot graph
plot_model(model, to_file='multilayer_perceptron_graph.png')
```

Let's zoom in on the new lines

```python
inputs = [[5,10], [5]]
outputs = [[1], [20]]
model = create_network(inputs, outputs)
```

We can translate the above as 
* inputs consists of two different inputs, the first input is an array of size \\(5 \times 10 \\) and the second input is of size \\(5 \\)
* output consists of two different outputs, the first output is an array of size 1 and the second output is an array of size 20

We can add as many inputs and outputs as we want. We can nest arrays inside arrays to predict tree like data structures but the key idea is the following.

> Input and output uniquely define WHAT a neural network can represent or which problems it can solve. The layer configuration and the weights of each hidden layer node determine HOW good the neural network will be on a sample task.

Two neural networks with the same exact inputs and outputs model the same problem. They will differ in performance characteristics due to their hidden layers.

If we think about the structure of input and output their types encode a specific application. For example, in graphics your input is a 3D scene equipped with a camera (which can be encoded as a vector) and your output is a 2D image rendering (which can be encoded as a tensor). So if we represent a neural network as a function \\(f \\) that solves the graphics rendering problem then \\(f^{-1}) is a function that solves the inverse graphics problem. Inverse graphics is the problem of taking an input 2D image and outputting a 3D scene. Neural networks solve 2 problems at once, the original forward problem and the inverse problem.

So enough abstractions, let's go over some examples.

![simple](/assets/images/simple.svg)

# Examples

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

## How to solve complex problems by combining neural networks that solve simpler problems

Compositional or hierarchical learning papers often talk about end to end learning and what it means exactly is best explained via an example.

Suppose your goal is to train a humanoid robot to play soccer

There's a few subskills that seem more basic but crucial to be able to succeed
1. Learning to balance
2. Learning to walk
3. Learning to run
4. Learning to kick a ball
5. Learning if an action in given circumstances is against the rules
6. Learning where opponents and teammates are
etc...

> Is there any way we can combine knowledge gained from all subskills to get better at the end goal of kicking a soccer ball?


Let's rephrase the above question from a type theoretic view of neural networks.

> Can we combine each of the trained neural networks from the smaller tasks to create a larger network that solves the larger task

The point of this section is to then think about what it means to "combine neural" networks and what are the options we have at our disposal. We'll be borrowing ideas from the functional programmaing, category theory and group theory communities here.

A neural network for a task \\(i \\) can be modeled as a function \\(f_i \\), the function can be arbitrarily complicated but for all intents and purposes it doesn't matter at all since we're only looking at the inputs and outputs.

Let's go over some examples

What does \\(f_i^{-1} \\) mean
* Flip input and output
* Do backprop for inference


What does \\(f_i^{-1} f_i \\) mean
* Encoder decoder architecture - noop at training time

What does \\(f_i \times f_i  \\) mean
* Create a tuple of size 2 of the output

What does \\(f_i \times f_j \\) mean
* Create a tuple, first element from first network and second element from second network

What does \\(f_i + f_j \\) mean
* Concatenate the outputs of two networks

What does \\(f_i - f_j \\) mean
* Remove the output associated with the second network

What does \\(f_i / f_j \\) mean
* Not sure yet myself



What does \\(f - \\) mean

What does \\(f + )

At the very least a neural network is a group? Ring? 

### Next steps

If you're looking for more examples to motivate you, I'd recommend you try to answer the following
1. How can I model problems with unspecified input and output sizes? Google RNN for this, the key idea is feedback and state
2. How would things like self play in reinforcement learning work in this setting since you don't really have labeled data? You can bootsrap off of your current best estimate which to me is one of the coolest idea I've encountered in ML

If you enjoyed this article you'll probably also enjoy [Neural Networks, Types, and Functional Programming](https://colah.github.io/posts/2015-09-NN-Types-FP/)


## References
* https://machinelearningmastery.com/keras-functional-api-deep-learning/
* Deep Learning and the game of Go