---
layout: default
title: PyTorch needs great Systems Engineers
---

> If you're excited about optimizing code that runs equally well on a single or thousands of GPUs and if you have the ability to submit a single substantial PR to a major OSS library, we want you on the PyTorch team - especially if you're early in your career.

## Why PyTorch?
Both LLaMA and ChatGPT pretraining rely on our infrastructure, so do thousands of other AI workloads and companies. If your ideas are good, why limit your reach to a single company? You’ll be a better engineer if you can get your ideas adopted by all sorts of research labs. We are running into hard physics limitations when programming large clusters. We're rewriting everything to scale to 100K+ GPUs, and we need fresh ideas to actually pull it off.

## We're hiring juniors when others aren't
We know the job market for junior engineers is tough right now. While other companies are freezing junior hiring, we're doubling down. Junior engineers often question assumptions that experienced engineers take for granted. One of PyTorch's founding authors Adam Paszke was an undergraduate when he wrote PyTorch.

## The crazy low-level ML Systems stuff you’ll work on
If you're impatient and hate waiting weeks for training runs, if you believe good ideas should help others, and if you want to understand how computers really work - ML Systems is the perfect career start and PyTorch is one of the most succesful ML Systems projects of all time.

If you’re early career and smart you should not be vibe coding, you should be working on harder problems. Here is a random list of projects we’ve been up to in PyTorch.
* Rewriting core collectives to introduce fault tolerance with RDMA and GPUDirect, allowing training to continue even when nodes fail
* Building a custom Python bytecode interpreter so you can capture PyTorch graphs without forcing users to rewrite their Python code
* Rewriting PyTorch Distributed from scratch so you can pdb across a training job
* Rewriting all of our C++ code so it’s ABI compatible for another 20 years
* Fixing performance problems by changing a single register value from 1 to 0 

These aren't theoretical problems – for example, when we built FSDP, it triggered a wave of new distributed training papers so your work determines the shape of next gen research.

## What we're actually looking for

We don't care about which university you went to. Instead, show us what you've built, even if it's small. If you've never contributed to open source before, make a small PR to PyTorch and then apply!

## Why you should NOT apply
This job isn't for everyone, and that's okay. You probably won't enjoy working with us if:
* You prefer clear direction and well-defined tasks. We're not hierarchical, and engineers find their own projects. This freedom is exhilarating for some and paralyzing for others.
* You dislike interacting with the broader community. Working in open source means engaging with users, contributors, and sometimes critics on GitHub, Discord and X
* You're fixated on a single metric like "make models the biggest" or "make training the fastest." We balance many trade-offs: usability, performance, compatibility, and maintainability. Single-minded optimization doesn't work here.
* You're not interested in long-term ownership. Thousands of projects depend on our code. You can't write something clever and walk away - you'll need to support it, fix bugs, and improve it over time.

## The open-source advantage
You work with users directly. There are no manufactured problems, you need to work on the actual bottlenecks preventing AI progress. Open source means you're building in public, getting feedback in public, and earning a public reputation for your work. Your GitHub commits become your resume and we hope to be the last leetcode interview you ever need to go through.

## How can I apply
If you're smart and curious we should talk. Express your interest on [https://workwithpytorchmeta.com/](https://workwithpytorchmeta.com/). It should take no more than 5 minutes.
