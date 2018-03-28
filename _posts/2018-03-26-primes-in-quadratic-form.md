---
layout: post
title: Primes in quadratic sequences
excerpt: Are there more primes of the form $n^2 + 21n + 1$ than of the form $n^2 + n + 1$?
date: 2018-03-26
---

Here's the question we're going to try to answer: if we consider the values taken by a quadratic function $f(n) = an^2 + bn + c$ for $n = 1, 2, 3, \dots$, how frequently is $f(n)$ a prime?

Specifically, my motivation for this question originally comes from [Raziman's Google+ post](https://plus.google.com/+RazimanTV/posts/ZG1DHvi7pRu) (ultimately from [a Quora question](https://www.quora.com/The-sequence-n-2-21n-1-n-1-2-3-cdots-seems-to-produce-more-than-twice-as-many-primes-as-the-sequence-n-2-n-1-n-1-2-3-cdots-How-can-I-make-this-precise-and-prove-it-or-is-it-even-true)):

> The sequence $n^2+21n+1$, for $n=1,2,3,\dots$, seems to produce more than twice as many primes as the sequence $n^2+n+1$, for $n=1,2,3,\dots$. How can I make this precise and prove it (or is it even true)?

#### Formal problem

For simplicity, let's assume that, as in the two quadratic polynomials above, the coefficients $(a, b, c)$ are such that $f(n)$ is always a positive integer, and that the polynomial is not something like $n^2 + n + 2$ which is always even (or in general always divisible by $p$ for some prime $p$).

#### Formal proof is hard

A fully formal proof of the statement itself will be hard: we cannot even prove that there are infinitely primes of the form $n^2+1$ yet, let alone estimate their number!

#### Ok let's try

Consider the polynomial $f(n) = n^2 + 21n + 1$ (I'll treat this one first, as $n^2 + n + 1$ is simpler). For how many values of $n \le N$ is $f(n)$ prime?

Recall the [prime number theorem](https://en.wikipedia.org/wiki/Prime_number_theorem): the number of primes less than $N$ is about $N / \log N$, or (a better approximation) about $\int\limits_2^{N} (1/\log t)\, dt$, or for that matter $\sum\limits_{m=2}^{N} 1/\log m$. Based on the prime number theorem, one heuristic model of the prime numbers is that every number $m$ is “prime” with probability $1 / {\log m}$.

This heuristic would say that $f(n) = n^2 + 21n + 1$ is prime with probability $\displaystyle \frac{1}{\log(n^2 + 21n + 1)} \sim \frac{1}{2 \log n}$, so for $n \le N$, the expected number of primes is $~ \sum_{n=2}^{N} 1/(2 \log n) \sim N/(2 \log N)$. This of course 





> _I don’t know whether the constraints for higher primes can eventually switch the balance back in favour of n^2+n+1, but seems unlikely and I can’t prove it either way._

More precisely, we can say exactly how many such constraints there will be for (which) large primes.

Consider f(n) = n^2 + 21n + 1. For a given prime p, if it has any such constraint, i.e. if there is any solution to f(n) = 0 mod p, then (basically by “completing the square”) we have 0 = 4f(n) = (2n + 1)^2 - 437, i.e. the number of solutions to f(n) = 0 mod p is the number of solutions to x^2 = 437 mod p. And using quadratic reciprocity etc., we can prove that the number of solutions to x^2 = 437 mod p is:

* 1 if p = 19 or p = 23
* 2 if p mod 437 lies in a certain set of 198=9×11×2 numbers mod 437 (p should either be a residue mod both 19 and 23, which gives 99 values, or nonresidue mod both, which gives another 99)
* 0 otherwise (if p lies in the set of other 198 possible remainders for primes mod 437)

(This means that for half the primes p ≠ 19, 23, we have 2/p possible values of n “knocked out” by such constraints, while for the other primes p we have no values knocked out.)

Similarly, for g(n) = n^2 + n + 1, the number of solutions to g(n) = 0 mod p is:

* 1 if p = 3
* 2 if p = 1 mod 3
* 0 otherwise

(This means that for half the primes p ≠ 3 we have 2/p possible values of n “knocked out” by such constraints, while for the other primes p we have no values knocked out.)

And using this, we can estimate the number of primes in either polynomial. The final answer (heuristically / based on conjectures) turns out to be:

* The number of primes of the form n^2 + n + 1, for n <= N, is about 1.25 N/log N
* The number of primes of the form n^2 + 21n + 1, for n <= N, is about 2.79 N / log N
* So the ratio is about 2.23

For more, see:

* https://en.wikipedia.org/w/index.php?title=Ulam_spiral&oldid=821475153#Hardy_and_Littlewood's_Conjecture_F
* https://en.wikipedia.org/w/index.php?title=Bunyakovsky_conjecture&oldid=830234069
* https://en.wikipedia.org/w/index.php?title=Bateman%E2%80%93Horn_conjecture&oldid=828694748









----

Earlier version of this post:

I'm sure number-theorists have studied questions like this: e.g. there's an entire book titled _Primes of the form $x^2 + ny^2$_, so presumably “primes of the form $n^2+21n+1$” is easier and well-studied. But this is what I know to say about this.

Note the fact that (here $\nmid$ stands for “does not divide”)

$$[m\text{ is prime}] = [2 \nmid m]\, [3 \nmid m] \, [5 \nmid m] \cdots \label{eq:sepprimes} \tag{*}$$

for all primes less than $m$ (or, enough to say: all primes not greater than $\sqrt{m}$).

## Divisibility by $p$

Consider the equation $f(n) \equiv 0 \pmod p$, where  $f(n)$ is either $n^2 + n + 1$ or $n^2 + 21n + 1$. This is an equation modulo $p$, and let $\epsilon(p)$ be the number of solutions modulo $p$. The equation has at most $2$ solutions modulo $p$ (or in other words, among the first $p$ numbers $0, 1, 2, \dots, p - 1$).

The statement $[p \nmid m]$ is equivalent to $[n^2 + n + 1 \not\equiv 0 \pmod p]$ or in words, that $n$ is not a solution modulo $p$ to the equation $x^2 + x + 1 \equiv 0 \mod p$.

So among the first $kp$ numbers of the form $f(n)$, the number of numbers divisible by $p$ is $k\epsilon(p)$. In other words, a fraction $\epsilon(p)/p$ of numbers of the form $f(n)$ are divisible by $p$.

Now if we consider the equation $\eqref{eq:sepprimes}$, then, for numbers “near” $m$, then roughly:

* a fraction $\epsilon(2)/2$ of the numbers are divisible by $2$,
* a fraction $\epsilon(3)/3$ of the numbers are divisible by $3$,
* a fraction $\epsilon(5)/5$ of the numbers are divisible by $5$,

etc.

So the fraction of numbers “near” $m$ that are not divisible by any of the primes $2, 3, 5, \dots, P$, where $P = p_{\pi(\sqrt{m})}$, is:

$$(1 - \frac{\epsilon(2)}{2}) (1 - \frac{\epsilon(3)}{3}) (1 - \frac{\epsilon(5)}{5}) \cdots (1 - \frac{\epsilon(P)}{P})$$

— this is roughly the “probability” that $m$ is prime.

## Number of solutions: $n^2 + n + 1$

If $n^2 + n + 1 \equiv 0 \pmod p$, then, assuming $p \neq 2$, we have $$4n^2 + 4n + 4 = (2n + 1)^2 + 3 \equiv 0 \pmod p,$$ or in other words $(2n + 1)^2 \equiv -3 \pmod p$. For any solution to $x^2 \equiv -3 \pmod p$, we can solve $2n + 1 \equiv x$ to get $n = 2^{-1}(x - 1)$ (and these solutions are distinct). So the number of solutions to $n^2 + n + 1 \equiv 0 \pmod p$ is the number of solutions to $x^2 \equiv -3 \pmod p$. 

If $p = 3$, then this means $x = 0$. For other $p$, we have (see [here](https://en.wikipedia.org/w/index.php?title=Legendre_symbol&oldid=805985930#Properties_of_the_Legendre_symbol)):

$$\left(\frac{-3}{p}\right) = \left(\frac{-1}{p}\right)\left(\frac{3}{p}\right) = (-1)^{[p \not\equiv 1 \pmod 6]} $$

In other words, the number of solutions to $n^2 + n + 1 \equiv 0 \pmod p$ is:

* $0$, if $p = 2$,
* $1$, if $p = 3$,
* $2$, if $p \equiv 1 \pmod 3$,
* $0$ otherwise, i.e. if $p \equiv 2 \pmod 3$

So the fraction of numbers of the form $n^2 + n + 1$ not divisible by any of the primes $2, 3, 5, 7, 11, 13, \dots$ is 

$$\def\({\big(} \def\){\big)} \(1\)_2 \(\frac23\)_3 \(1\)_5 \(\frac57\)_7 \(1\)_{11} \(\frac{11}{13}\)_{13}$$

## Number of solutions: $n^2 + 21n + 1$

For the other polynomial, if $n^2 + 21n + 1 \equiv 0$, then again assuming $p \neq 2$, we have $0 \equiv 4n^2 + (4\cdot21)n + 4 = (2n + 21)^2 - 437$, and for any solution to $x^2 \equiv 437$ we can solve for $n$.

As $437 = 19 \times 23$, we have (for $p \neq 19, 23$), 

$$\left(\frac{437}{p}\right) = \left(\frac{19}{p}\right)\left(\frac{23}{p}\right) = (-1)^{(p-1)/2}\left(\frac{p}{19}\right)(-1)^{(p-1)/2}\left(\frac{p}{23}\right)$$

that is, $437$ is a quadratic residue mod $p$ if and only if either $p$ is a quadratic residue modulo both $19$ and $23$, or modulo neither. This means that either

* $p$ is one of $9$ certain values mod $19$, and one of $11$ certain values mod $23$, so one of $99$ certain values mod $437$, or
* $p$ is one of $9$ certain values mod $19$, and one of $11$ certain values mod $23$, so one of $99$ certain values mod $437$.

That is, $p$ is one of $99 + 99 = 198$ values mod $437$.

When $p = 19$, we have $2n + 21\equiv 0$ or $n \equiv -1$.

When $p = 23$, we have $2n + 21 \equiv 0$ or $n \equiv 1$.

## Putting them together

Now we have a concrete way to count the number of values of $n$ modulo $p$ that are “knocked out” from $f(n)$ being prime, for each prime $p$ and for both functions $f$.



----
