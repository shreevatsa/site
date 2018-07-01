---
layout: post
title: The distribution of least prime divisors
excerpt: How frequently is 3 the smallest prime factor of $2p_n-1$? Etc.
date: 2018-05-20
tags: [done, maths, better]

---

Inspired by / based on: <https://manasataramgini.wordpress.com/2018/05/20/a-note-on-the-least-prime-divisor-sequences-of-2p-plus-or-minus-1/>

Consider a number $m$. If we consider the sequence $q_n = 2p_n - 1$ where $p_n$ denotes the $n$th prime number, how frequently is $m$ the smallest factor (other than $1$) of $q_n$?

One thing to note immediately is that the smallest factor of a number ([A020639](http://oeis.org/A020639)) is always a prime number. Further, in our case as $q_n$ is always odd, this least prime factor can't be even. So the answer is $0$ unless $m$ is one of the odd prime numbers ($3, 5, 7, 11, \dots$). (The sequence of values of smallest prime factors of $q_n$ is [A023585](http://oeis.org/A023585); we want to know the frequency with which the different odd primes $m$ occur in the sequence.)

If one wants a more formal statement of the problem: let

$$\displaystyle f_N(m) = \frac{|\{n \le N: m\text{ is the smallest prime factor of $q_n$\}}|}{N}$$

What is the value of $f(m) = \lim\limits_{N \to \infty} f_N(m)$?

---

Let's fix a particular value of $m$, say $m = 3$. How frequently is $3$ the smallest prime factor of a number $q_n = 2p_n - 1$?

$3$ divides $q_n$ if and only if $2p_n - 1 \equiv 0 \pmod 3$ which is the same as $p_n \equiv 2 \pmod 3$. As all primes (other than $3$ itself) are either $1$ or $2$ mod $3$, and are not expected to favour either of these congruence classes over the other*, in the long run exactly half the numbers $p_n$ are $2$ modulo $3$, so we should expect to see the number $3$ about **half** the time as the least prime factor.

$$\displaystyle f(3) = \frac{1}{2} = 0.5$$

<sub>[*An important footnote here: the fact that the primes fall into each possible residule class modulo a number $n$ (i.e. those $\phi(n)$ residue classes relatively prime to $n$) with equal frequency is known as [the prime number theorem for arithmetic progressions](https://en.wikipedia.org/w/index.php?title=Prime_number_theorem&oldid=841269264#Prime_number_theorem_for_arithmetic_progressions). This has been proved; the frequency of primes in each of the classes is exactly the same. But if we care about the exact value down to which residue class is the “winner” (not a bigger ratio in the limit, but a bigger absolute number at some finite point), then there exists such a thing as the [Chebyshev bias](https://en.wikipedia.org/wiki/Chebyshev%27s_bias). But that is a second-order effect and we don't have to care about it here...]</sub>

---

Next consider $m = 5$. Again, $5$ divides $q_n$ if and only if $2p_n - 1 \equiv 0 \pmod 5$, which is the same as $p_n \equiv 3 \pmod 5$. Now, again, of all the primes (other than $5$ itself), on average exactly $1/4$th of them fall into each residue class. *However*, for $5$ to be the smallest prime factor, we first need the number $q_n$ to *not* be divisible by $3$, which only happens half the time. Thus, $f(5) = (1 - f(3))/4$, or

$$\displaystyle f(5) = \frac{1}{8} = 0.125$$

----

Next consider $m = 7$. Half the numbers $q_n$ are divisble by $3$. Of the remaining numbers, $1/4$th are divisible by $5$. (That is, $1/4$th of all the numbers $q_n$ are divisible by $5$, and this remains the case even if we consider just the numbers $q_n$ not divisible by $3$.) So by a similar argument, $f(7) = (1 - \frac12)(1 - \frac14)/6$, thus

$$\displaystyle f(7) = \frac{1}{16} = 0.0625$$

----

By exactly a similar argument, we get

$$\displaystyle f(11) = \left(1 - \frac{1}{2}\right)\left(1 - \frac{1}{4}\right)\left(1 - \frac{1}{6}\right) \frac{1}{10} = \frac{1}{32} = 0.03125$$

$$\displaystyle f(13) = \left(1 - \frac{1}{2}\right)\left(1 - \frac{1}{4}\right)\left(1 - \frac{1}{6}\right) \left(1 - \frac{1}{10}\right) \frac{1}{12} = \frac{3}{128} = 0.0234375$$

$$\displaystyle f(17) = \left(1 - \frac{1}{2}\right)\left(1 - \frac{1}{4}\right)\left(1 - \frac{1}{6}\right) \left(1 - \frac{1}{10}\right)  \left(1 - \frac{1}{12}\right) \frac{1}{14} =\frac{33}{2048} = 0.01611328125$$

$$\displaystyle f(19) = \left(1 - \frac{1}{2}\right) \dots \left(1 - \frac{1}{12}\right) \left(1 - \frac{1}{16}\right) \frac{1}{18} =\frac{55}{4096} = 0.013427734375$$

$$\displaystyle f(23) = \left(1 - \frac{1}{2}\right) \dots \left(1 - \frac{1}{16}\right) \left(1 - \frac{1}{18}\right) \frac{1}{22} = \frac{85}{8192} = 0.0103759765625$$

$$\displaystyle f(29) = \left(1 - \frac{1}{2}\right) \dots \left(1 - \frac{1}{18}\right) \left(1 - \frac{1}{22}\right) \frac{1}{28} = \frac{255}{32768} = 0.007781982421875$$

$$\displaystyle f(31) = \left(1 - \frac{1}{2}\right) \dots \left(1 - \frac{1}{22}\right) \left(1 - \frac{1}{28}\right) \frac{1}{30} = \frac{459}{65536} = 0.0070037841796875$$

and in general, when $m$ is a prime number,

$$\displaystyle f(m) = \frac{1}{m-1}\prod_{2 < p < m}\left(1 - \frac{1}{p-1}\right)$$

where the product is taken over prime numbers $p$.

(In case one is wondering: when $f(m)$ is expressed as a fraction, the denominator is not always a power of $2$ as it was in the above early examples; for example $f(47) = \frac{788307}{192937984}$ where the denominator is divisible by $23$.)

------

This same formula for $f(m)$ holds if the sequence $q_n = 2p_n - 1$ is replaced by the sequence $q_n = 2p_n + 1$ or $q_n = 2^kp_n + 1$ or $q_n = 2^kp_n - 1$ for any integer $k$.

And a similar formula holds (and computation can be carried out) for the frequency of least prime divisors of the sequence $q_n = ap_n + b$ for any integers $a$ and $b$:

- if either $\gcd(a, b) > 1$ or they are both odd, the question becomes trivial: all $q_n$ (at least after the first one) are divisible by a common prime,
- else, the calculation is as above, and the only difference is that one must exclude factors in the product for primes $p$ that divide either $a$ or $b$.

----

A note on the asymptotics of $f(m)$: [Mertens proved in 1874](https://terrytao.wordpress.com/2013/12/11/mertens-theorems/#mertens-3) that $\displaystyle  \prod_{p \leq x} (1-\frac{1}{p}) = \frac{e^{-\gamma}+o(1)}{\log x}$. Here we have $\prod_{2 < p < m}\left(1 - \frac{1}{p-1}\right)$ which we can expect will have a similar rate of growth: namely, $\frac{c}{\log m}$ for some $c$, so that $f(m) \sim \frac{c}{(m-1)\log m}$. And (thanks to [asking about it](https://math.stackexchange.com/questions/2789800/the-asymptotics-of-the-products-over-primes-prod-limits-2p-le-n-left1-f) on math.SE), it turns out that it is indeed the case: we have

$$
f(m) \sim \frac{2C_2e^{-\gamma}}{m\log m} = \frac{0.74130822439192108...}{m\log m}
$$

where $\gamma \approx 0.57721566490153286…$ is [the Euler-Mascheroni constant](https://en.wikipedia.org/wiki/Euler%E2%80%93Mascheroni_constant), and $C_2 \approx 0.66016181584686957…$ is the [twin prime constant](http://primes.utm.edu/glossary/xpage/TwinPrimeConstant.html). For example, for $m = 91781$, we have

$$
\begin{align}
f(m) &\approx 0.00000070667704\dots \\
\frac{0.741308224}{m\log m} &\approx 0.00000070681817\dots
\end{align}
$$

(Convergence is slow: near $m=100000$ we still barely get three significant digits of accuracy. But we have proof.)
