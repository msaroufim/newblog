---
title: How to win at Poker
layout: default
---
 
Robots won't be able to take cover unless they find a way to finance their efforts, they can do this via investing, war and gambling. Warfare is by far the most complex simulation cause it involves logistics, economics, politics and tactics. Investing

At the very least they'll need wealth to buy 3D printers and chips to finance their expansion.

So we'll focus on looking at a likely way that robots could quickly become rich, gambling by looking specifically at how to solve games like Poker.

# How to win at Poker
 
Poker is interesting because the randomness in the draws can be mitigated by a skillful player via deception.
 
It's this aspect of deception that has made it difficult historically for computers to play competitively at Poker. There is immense value in cracking Poker because it gives us an interesting insight on our way to AGI but also because it's easier to get really rich playing Poker vs Chess or Go. And hey these servers aren't paying for themselves. It's like my grandpa used to say, GPU's don't grow on trees.
 
DeepStack was the first effort to successfully beat professional human players at no limit poker. You may expect that DeepStacks architecture looks very similar to something like AlphaGo i.e: Monte Carlo Tree Search + a deep neural network for node evaluation, but there's a few key differences between Poker and full information strategy games.
 
1. The state at any point \\(t\\) is a function of all previous actions and states since we'd like to learn our opponents quirks
2. The state at any point \\(t\\) is unknown since we can't inspect our opponents cards
3. The value of a state is a function of the knowledge each player has of the others cards
4. The branching factor is infinite specifically for no limit poker because you can make arbitrarily high bids and each of those bids is a potential action
5. The optimal strategy has to involve a degree of randomness or else your moves will be extremely predictable. In the game theory literature this is referred to as mixed equilibrium strategies
 
It's amazing that despite these difficulties we can still achieve amazing results on no limit Poker using a technique called counterfactual regret minimization which comes from the game theory literature + a few tricks to make it scale to this large data regime.
 
## Game theory
 
You've probably heard of the term "Nash Equilibrium", it's called an Equilibrium because it represents a state where neither of the two agents have an incentive to deviate from their respective strategies. I.e: neither agent would gain more utility by deviating from their respective strategies.
 
We won't prove the fundamentals of game theory here but it's worth mentioning a few key results for 2 player games.
 
1. Nash existence theorem: For any finite game a nash equilibrium is guaranteed to exist
2. Minimax theorem: There could be multiple winning strategies but they're gonna do at best as good as the nash equilibrium
 
Next we'll talk about how counterfactual regret minimization lets us compute a nash equilibrium which guarantees that we won't do worse than draw in expectation.
 
 
## Counter Factual regret minimization

### Data structure to learn Poker

Most turn based games can be modeled as trees where each node represents the current state of the board and each edge represents an action which would move the board from one state to another.
 
However, like we mentioned above, Poker has some issues if we apply this model in a straightforward manner since we don't really know what the state of our opponent is and our opponents aren't willing to share the history of their states so we can't quite use Vanilla Monte Carlo Tree Search or turn the problem into a supervised learning problem.
 
So instead each node will represent will combine the states that we do know like the history of raises, folds, card results and for the states that we don't know anything about the cards of our opponent we will instead represent them using a probabilistic belief instead.
 
So now we have some idea of what a data structure for counterfactual regret minimization would look like but we still didn't explain what we mean by counter factual and what we mean by regret. Let's start with regret, specifically no regret learning.

### No regret learning
 
No regret learning is a really interesting idea that shows up in the boosting literature and actually comes out very naturally in scenarios like horse gambling.

So suppose you're a budding horse racing better and you wanna make bank. You have at your disposal \\(N\\) experts which will recommend you bet on one or the other horse. Which one should you listen to? If you don't care about horses just replace the word "horse" with the word "stock" or "decision" or "action" and the same analysis will hold.

We're doing this in an online manner, meaning in the very beginning we don't have much reason to trust one expert vs another.

At time \\(t\\) we record the loss each of the \\(N\\) experts in a vector \\(l^t\\) of length \\(N\\) according to our strategy \\(H\\) which distributes our initial capital according to a distribution \\(p\\). Meaning \\(p_i^t\\) is the fraction of our capital which went to expert \\(i\\) at time \\(t\\).

So we can define our expected loss at time \\(t\\) as

$$ l^{t}_{H} = \sum_{i=0}^{T}p_i^t l_i^t $$

If we sum up our losses over all timesteps until \\(T\\) then our total expected loss becomes 

$$ L_{H}^{T} = \sum_{t=0}^{T} l_H^t  $$

And now we can finally define regret as the difference between our total expected loss and the loss incurred by the single best expert in retrospect

$$ R = L_H^T - \min_i L_i^t $$

And as you'd intuitevely expect you wanna minimize your regret. If \\(R=0\\) then your approach was regret free.

### How to learn without regret
 There are many many learning algorithms that you could use with various tradeoffs. The simplest one is perhaps the "Weighted Majority Algorithm"

 Majority voting has a fascinating property in that suppose you have \\(n\\) experts each one essentially a bit better than a random coin flip in making decisions then you can show that together they will converge to the optimal decision more often than not. So essentially it's easier to hedge mistakes in a democracy than it is in a dictatorship where there is a single point of failure.

So we have a mixture of experts and we're listening to their advice. Barring prior information all their advice is equally good and we take a majority vote among them. 

Over time they will make mistakes and we will start prioritizing the advice of experts that have been right more often by basically halving the weight of an experts vote each time they are wrong.

```python
# initialize weights
weights = defaultdict()
track_record = defaultdict()
for i in range(N):
        weights[i][0] = 1/N 

## Adjust weights at time t+1 based on performance at time t
for i in range(N):
    if track_record[i][t] == False:
        weights[i][t+1] == weights[i][t] / 2
    else:
        weights[i][t+1] = weights[i][t]
```
 
## Tricks to make CFR scale
 
## Let's look at code
 
 
## What's next?
 
If you enjoyed this post, I'd strongly recommend you check out Python implementation of DeepStack https://github.com/cgnicholls/deepstack and the [DeepStack Paper](https://static1.squarespace.com/static/58a75073e6f2e1c1d5b36630/t/58b7a3dce3df28761dd25e54/1488430045412/DeepStack.pdf).
 
 
 Need to mention how multi agent games has made a comeback in the bitcoin community where we are thinking how to incentivize people to be honest.

 Main aspects of how people deal with each other include
 * Auctions
 * Social functions, can we even agree on one?
 * Voting
 * Computing nash equilibria

## References
* https://int8.io/counterfactual-regret-minimization-for-poker-ai/
* https://github.com/tansey/pycfr
* http://courses.cms.caltech.edu/cs253/slides/cs253-02-WMR.pdf
* [Multiagent systems](https://www.amazon.com/Multiagent-Systems-Algorithmic-Game-Theoretic-Foundations/dp/0521899435/ref=pd_sbs_14_t_2/131-4946721-1001121?_encoding=UTF8&pd_rd_i=0521899435&pd_rd_r=1140f21b-433b-40e7-b1c8-0e3a2206761f&pd_rd_w=TlEkS&pd_rd_wg=RZeba&pf_rd_p=5cfcfe89-300f-47d2-b1ad-a4e27203a02a&pf_rd_r=Y7ZNNN5X6GJGHQBF6TDZ&psc=1&refRID=Y7ZNNN5X6GJGHQBF6TDZ)
