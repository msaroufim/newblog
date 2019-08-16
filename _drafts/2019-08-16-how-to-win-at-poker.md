---
title: How to win at Poker
layout: default
---

# How to win at Poker

Poker is interesting because the randomness in the draws can be mitigated by a skillful player via deception.

It's this aspect of deception that has made it difficult historically for computers to play competitively at Poker. There is immense value in cracking Poker because it gives us interesting insight on our way to AGI but also because it's easier to get really rich playing Poker vs Chess or Go. And hey these servers aren't paying for themselves. It's like my grandpa used to say, GPU's don't grow on trees.

DeepStack was the first effort to succesfully beat professional human players at no limit poker. You may expect that DeepStack's architecture looks very similar to something like Alpha Go i.e: Monte Carlo Tree Search + a deep neural network for node evaluation, but there's a few key differences between Poker and full information strategy games.

1. The state at any point \\(t\\) is a function of all previous actions and states since we'd like to learn our opponents quirks
2. The state at any point \\(t\\) is unknown since we can't inspect our opponents cards
3 The value of a state is a function of the knowledge each player has of the others cards
4. The branching factor is infinite specifically for no limit poker

It's amazing that despite these difficulties we can still achieve amazing results on no limit Poker using a technique called counter factual regret minimization which comes from the game theory litterature + a few tricks to make it scale to this large data regime.

## Game theory intro

## Counter Factual regret minimization

## Tricks to make CFR scale

## Let's look at code


## What's next?

If you enjoyed this post, I'd strongly recommend you check out Python implementation of DeepStack https://github.com/cgnicholls/deepstack and the [DeepStack Paper](https://static1.squarespace.com/static/58a75073e6f2e1c1d5b36630/t/58b7a3dce3df28761dd25e54/1488430045412/DeepStack.pdf).


## References
* https://int8.io/counterfactual-regret-minimization-for-poker-ai/
* https://github.com/tansey/pycfr
