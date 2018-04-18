# Rough work

Context: See https://manasataramgini.wordpress.com/2018/04/15/a-sequence-related-to-prime-counting/ — a very intriguing conjecture!

Let $T(m) = [m\text{ is prime}] = \begin{cases}1 &\text{if $m$ is prime}\\ 0&\text{otherwise}\end{cases}$

Then, $f(1) = 1$ and $\displaystyle f(n) = \sum_{k=1}^{n-1} T(f(k) + n - 1)$.

The “Cramer heuristic” is roughly that any number $m$ is prime with “probability” $1/{\log m}$. More formally, the Cramér random model (see https://terrytao.wordpress.com/2015/01/04/254a) is the following: consider a random set $S$ of integers, such that each number $m > 2$ independently has probability $1/\log m$ of being in $S$. Then the asymptotics of the set of primes $P$ behaves roughly like that of $S$.

Using this heuristic, the probability that $f(k) + n - 1$ is “prime” (or rather, lies in $S$) is $1/\log(f(k) + n - 1)$. Let $g(n)$ denote the expected value of $f(n)$, if we replace the function $T(m) = [m\text{ is prime}]$ with the (random) function $T'(m) = [m \in S]$. Then, we have

$ \displaystyle g(n) =\sum_{k=1}^{n-1} 1/\log(g(k) + n - 1)$.

Assuming the Cramér heuristic (which gives correct predictions for many number-theoretic functions), the task is to prove that $g(n) \sim \frac{n}{\log n}$.

My powers of analysis aren't good enough to prove this :-) But this is probably true/provable, by first showing that each $\log(g(k) + n - 1) \sim \log(n)$ or something like that. Even after proving this about $g$, relating this to the actual $f$ without recourse to the Cramér heuristic may be hard, like many things in number theory.