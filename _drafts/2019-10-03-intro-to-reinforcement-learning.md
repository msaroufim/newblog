
# Board games

# Reinforcement learning in discrete space

# Reinforcement learning in continuous space


# Notes

* Highlight main ideas from each different RL approach
* MCMC for action sampling in board game space, not as easy to do for continuous domains
* Mention how RL algorithm can output both a value and a state and how this idea gets expanded on later

# References
* https://distill.pub/2019/paths-perspective-on-value-learning/

Reinforcement learning is a declarative way to teach machines certain behaviors. You specify some high level reward function like winning at Chess or Go and via self play they can beat human world champions at those games.

Typically in supervised learning you have some dataset which has labeled examples and you're trying to predict labels on unlabeled examples. Game simulators are unique in the sense that they don't strictly need labeled data (although it doesn't hurt) since game simulators generate their own training data. This is an immensely powerful property because for the most algorithmic advances in supervised learning are overshadowed by collecting more data. Collecting data is expensive, hard, often violates privacy, requires an entire BI infrastructure with support, alerting, monitoring, product managers and a bunch of other stuff that's not really realistic for smaller teams.

Training a supervised learning problem is generally easy so even in the case of Reinforcement Learning we will discuss how to turn an RL problem into a supervised learning problem and hence make it easy.

However, in the case of Reinforcement Learning you essentially program a video game such that it respects an interface which makes Reinforcement Learning training easy.

First time I saw a clean interface was by [Open AI](https://github.com/openai/gym/blob/master/gym/core.py), I've removed the non essentials to make what's going on crystal clear.

So idea is you already have some game running in an arbitrary game engine and you'd like to add to your game the ability to do Reinforcement Learning training. While this is interesting in of itself from a research standpoint where we'd like to figure out which games our current algorithms struggle with and why, there's also applications in gaming where you'd like to for e.g: build a training a buddy, strong coop AI, swap in players that have disconnected etc..

So we need to setup a base class ```Env``` in Python (this would be called an interface in other languages) which will correspond to a Reinforcement Learning interface. The 3 main methods we need to lsupport are

1. ```step()``` which is the main logic of the simulator. Think of the game as running in discrete timesteps where at every timestep the game is in some state and given a player action will move to another state
2. ```reset()``` which will help us stop the simulation if an agent is taking too long to learn or has already achieved its goal
3. ```render()```: which will help us render the simulation on our monitor so we can debug what's going on. One advantage of Reinforcement Learning is that bug have a strong visual impact which is easier to spot then variations in a Precision/Recall curve

```python
class Env(object):

    def step(self, action):
        """
        Accepts an action and returns a tuple (observation, reward, done).
        Args:
            action (object): an action provided by the agent
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
        """
        raise NotImplementedError

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        raise NotImplementedError

    def render(self, mode='human'):
        """Renders the environment which can be in a variety of modes
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image
        """
        raise NotImplementedError
```


## The Different Reinforcement Learning algorithms

The general problem definition of reinforcement learning doesnt' change all that much in the different kinds of algorithms but the different algorithms are better suited for different kinds of environments so it's worth highlighting some of their key differences.

For a comprehensive overview of most of them, I'd highly recommend
* [A long peek into reinforcement learning by Lilian Weng](https://lilianweng.github.io/lil-log/2018/02/19/a-long-peek-into-reinforcement-learning.html)
* [Reinforcement Learning: An Introduction by Sutton and Barto](http://incompleteideas.net/book/the-book-2nd.html)

RL algorithms differ across various parameters
1. Model based vs model free vs hybrid methods:
2. On policy vs off policy:
3. Markovian vs non Markovian: 

Define a policy

Define a value function

### Markovian property
The Markovian property is usually stated as 

\\P(S_{t+1} | S_1 ... S_t) = (P(S_{t+1} | S_t) = \\)

Some examples

The advantage is that when it holds we can only consider the current state and the next action to find out the next state or in other words there is no dependence on the history of all past events. For most games the Markovian property holds, 

In games of imperfect information such as Poker it doesn't sicne you need to know the history of all the moves of the players to figure out what their style is and come up with the best strategy in response. 

Policy Evaluation, Iteration and IMprovement

Monte Carlo methods -> Talk about chess

TD learning, Sarsa, Q learning

Deep Q network

Policy Gradient, A3C

Hindsight experience replay

# Issues with Reinforcement learning

Before we move on there's a few important issues with reinforcement learning that need to be discussed

The first issue is the tradeoff between exploration and exploitation


The second issue is that reinforcement learning training is unstable, different hyperparam changes may make a problem converge or not and it's very difficult to say a priori which algorithms and hyperparameters will be best without


# https://distill.pub/2019/paths-perspective-on-value-learning/
The natural value of a state is the average discounted return from obsering that state. Monte Carlo averages over trajectories that intersect.

The full evolution of a system according to some policy \\( \pi \\) can be described as a vector \\(S_1, S_2 ... S_n \\). We'll call the value of a path \\(V(s_t) \\) and define it as the immediate reward \\(r_t \\) you get at timestep \\(t \\) and the sum of all future values we'll get in future states \\(S_{t+1}, S_{t+2} \mathellipsis \\). Algebraically this comes down to.

\\(V(s_t) = R_t = r_t + \sum_{i=t+1}^{\infty}V(s_i) \\)

The sum above is infinite and doesn't have a general closed form solution so one trick we'll use to make it work is to add a discount factor \\(\gamma_t \\) for each timestep \\(t \\) that decays exponentially. The idea being that the same reward in the present is worth more than the same reward in the future. You may have already heard of this idea as the time value of money, same thing, you can call it time value of rewards.

Direct quote: First off, TD learning never averages over fewer trajectories than Monte Carlo because there are never fewer simulated trajectories than real trajectories. On the other hand, when there are more simulated trajectories, TD learning has the chance to average over more of the agent’s experience. This line of reasoning suggests that TD learning is the better estimator and helps explain why TD tends to outperform Monte Carlo in tabular environments.

An alternative to estimating Value function is a Q function where we estimate the value of a state and an action \\(Q(s,a) \\)


Off policy learning lets us weigh Q values by an arbitrary policy as opposed to the policy we're currently using for exploration

\\( \uppi^off \\) and \\(\uppi^on \\)

Make sure to give 1 line explanations of SARSA vs MC vs TD learning vs Q learning


## References
* [A long peek into reinforcement learning by Lilian Weng](https://lilianweng.github.io/lil-log/2018/02/19/a-long-peek-into-reinforcement-learning.html)
* [Reinforcement Learning: An Introduction by Sutton and Barto](http://incompleteideas.net/book/the-book-2nd.html)
* Deep Reinforcement Learning in ACtion
* Deep Learning and the Game of Go
* Grokking Deep Reinforcement Learning
* https://distill.pub/2019/paths-perspective-on-value-learning/