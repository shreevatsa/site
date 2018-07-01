---
layout: post
title: Possible way to approach a conjecture about A114897
tags: [done, maths]
excerpt:  Possible way of attacking a conjecture from https://manasataramgini.wordpress.com/2018/04/15
date: 2018-04-17
---

Let $$\displaystyle T(m) = [m\text{ is prime}] = \begin{cases}1 &\text{if $m$ is prime}\\ 0&\text{otherwise}\end{cases}$$

Then, define $f(1) = 1$ and $\displaystyle f(n) = \sum_{k=1}^{n-1} T(f(k) + n - 1)$.

This comes from <https://manasataramgini.wordpress.com/2018/04/15/a-sequence-related-to-prime-counting/> — which has a very intriguing conjecture: that $f$ grows like $\frac{n}{\log n}$ (more closely than $\pi(n)$ the prime-counting function). Read the post for details! The sequence is also recorded at [OEIS A114897](http://oeis.org/A114897).

The “Cramer heuristic” is roughly that any number $m$ is prime with “probability” $1/{\log m}$. More formally, the Cramér random model (see <https://terrytao.wordpress.com/2015/01/04/254a>) is the following: consider a random set $S$ of integers, such that each number $m > 2$ independently has probability $1/\log m$ of being in $S$. Then the asymptotics of the set of primes $P$ behaves roughly like that of $S$. This heuristic gives correct predictions for many number-theoretic functions.

(On heuristics: see also <http://www.utm.edu/~caldwell/preprints/Heuristics.pdf> and <https://projecteuclid.org/euclid.ijm/1255631807>.)

Similar to
$$T(f(k) + n - 1) = [f(k) + n - 1\text{ is prime}],$$
the indicator function for $f(k) + n - 1$ lying in $P$, consider instead
$$T'(f(k) + n - 1) = [f(k) + n - 1 \in S],$$
whose expected value is the probability of $f(k) + n - 1$ lying in $S$. This is $1/\log(f(k) + n - 1)$.

Let $g(n)$ denote the expected value of $f(n)$ if we replace the function $T(m) = [m\text{ is prime}]$ with the (random) function $T'(m) = [m \in S]$. That is, let $g(1) = 1$ and

$$\displaystyle g(n) =\sum_{k=1}^{n-1} \frac{1}{\log(g(k) + n - 1)}.$$

Assuming the Cramér heuristic, the task is to prove that $g(n) \sim \frac{n}{\log n}$.

My powers of analysis aren't good enough to prove this :-) But this is probably true/provable, by first showing that each $\log(g(k) + n - 1) \sim \log(n)$ or something like that. Even after proving this about $g$, relating this to the actual $f$ without appealing to the Cramér heuristic may be hard, like many things in number theory.
