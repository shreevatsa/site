---
layout: post
title: Primes in quadratic sequences (Part 1)
excerpt: Are there more primes of the form $n^2 + 21n + 1$ than of the form $n^2 + n + 1$?
date: 2018-03-26
---

Here's the question we're going to try to answer. Consider a quadratic polynomial $f(n) = an^2 + bn + c$ with integer coefficients $a, b, c$. If we consider the values taken by $f(n)$ for $n = 1, 2, 3, \dots$, how frequently is $f(n)$ a prime? That is, if we consider the values of $f(n)$ for $1 \le n \le N$, and count the number $P(N)$ of prime numbers among these values, what are the asymptotics of $P(N)$ as $N \to \infty$?

## Trivial cases

Some trivial cases are easy to dispose of:

* If $\gcd(a, b, c) = g > 1$ then $g$ always divides $f(n)$, so there can be at most one prime (namely $g$, if $g$ is a prime) in the sequence.
* Even without $\gcd(a, b, c) > 1$, it can happen that $f(n)$ is always even. When exactly does this happen? Modulo $2$, the value of $an^2 + bn + c \equiv an + bn + c = (a+b)n + c$ and this happens precisely when $(a + b)$ and $c$ are both even. So even in this case, $f(n)$ can take at most one prime value (namely $2$).

These are the only trivial cases, where all values of $f(n)$ are divisible by the same prime. For, suppose a prime $p$ always divides $an^2 + bn + c$.  (We've already considered the case of $p = 2$, so let's assume $p$ is an odd prime.) Then, from the fact that $p$ divides both $f(n)$ and $f(n+1)$ we can conclude that it divides $f(n + 1) - f(n) = a(2n + 1) + b$. Similarly, $p$ divides $f(n) - f(n-1) = a(2n - 1) + b$. So $p$ also divides *their* difference, which is $2a$.  So (as $p$ is an odd prime) $p$ divides $a$, and what we have (modulo $p$) is just a linear polynomial $f(n) \equiv bn + c \pmod p$. Further, if $p$ always divides this $f(n)$, then repeating the argument, we get $p$ divides $b$ and thence $c$, so we're in the $\gcd(a, b, c) > 1$ case that we considered earlier.

## Claim

So, to recap: we assume that $\gcd(a, b, c) = 1$ and that $a + b$ and $c$ are not both even. (If we don't want to treat negative integers as prime, let's further assume that $a > 0$, so that $f(n)$ is, at least eventually, always positive.) Under these assumptions, standard number theory conjectures state that:

* $P(N) \sim C \frac{N}{\log N}$, where the constant $C$ depends on $(a, b, c)$.

We'll see below how to calculate $C$.

## Heuristic argument and the constant C

We will not prove this formally. (No one has proved it yet; that's why it's called a conjecture.) In fact, it is beyond the reach of present-day mathematics to prove even that $P(N) \to \infty$, and even for a specific polynomial like $f(n) = n^2 + 1$.

Fortunately, a heuristic argument that gives those asymptotics (including the precise value of the constant) is rather easy to understand.

The prime number theorem states that the number of primes less than $N$ is $\sim \frac{N}{\log N}$ or (equivalently) $\sim \int_{2}^{N} \frac{dt}{\log t}$. This leads to the “Cramer heuristic”, that every number $m$ is prime with probability $\frac{1}{\log m}$. (See [notes by Terence Tao](https://terrytao.wordpress.com/tag/cramers-random-model/): the more formal statement is that the asymptotics of the primes resemble that of a random set where each number $m$ is chosen with probability $\frac{1}{\log m}$.)

Applying that heuristic here, if we consider the values of $f(n)$ for $1 \le n \le N$, then each $f(n) = an^2 + bn + c$ is prime with probability $\frac{1}{\log(an^2 + bn + c)}$, so the expected number of primes for $1 \le n \le N$ is $\sum_{n = 1}^{N} \frac{1}{\log(an^2 + bn + c)} \sim \sum_{n=1}^{N} \frac{1}{2\log n} \sim \frac{N}{2\log N}$.

This gives the right rate of growth, but to get the correct constant factor, we need to make some corrections to account for the fact that our situation of considering $f(1), f(2), \dots f(N)$ is not exactly like the situation of considering $1, 2, \dots, N$. Why?

* [$p=2$] In the situation of $1, 2, \dots, N$, half the numbers are even, and therefore (except possibly the single number $2$ itself) ruled out from being prime. But in the situation of $f(1), f(2), \dots, f(N)$, where $f(n) = an^2 + bn + c \equiv (a+b)n + c \pmod 2$, it may either happen that
  * $a+b$ is odd: then $f(n) \equiv n + c \pmod 2$ is odd half the time, the same as before (no corrections to make), or
  * $a + b$ is even: then $f(n) \equiv c \pmod 2$ is always odd (as we assumed $f(n)$ is not always even), so none of the numbers are ruled out from being even. So, considering divisibility by $2$ in isolation, we should have about twice the number of primes in this case.
* [$p=3$] In the situation of $1, 2, \dots, N$, a third of the numbers are divisible by $3$, and ruled out from being prime (apart from of course $3$ itself). But in the situation of $f(1), f(2), \dots, f(N)$, we'll have $f(n) = an^2 + bn + c \equiv 0 \pmod 3$ only if $n$ is a solution modulo $3$ to $an^2 + bn + c \equiv 0$. There may be $0$, $1$, or $2$ such solutions (mod $3$). If $k_3$ is the number of solutions to $an^2 + bn + c\equiv 0 \pmod 3$, then instead of ruling out a fraction $\frac13$ of numbers, we're instead ruling out a fraction $\frac{k_3}{3}$ of numbers. Thus, we have to correct our expression for the number of primes by a factor of $\frac{1 - k_3/3}{1 - 1/3}$.
* [General $p$] In general, if there are $k_p$ solutions modulo $p$ to $an^2 + bn + c \equiv 0$, then we multiply by a correction factor of $\frac{1-k_p/p}{1 - 1/p}$.

Putting all this together suggests that the constant $C$ should be:

$$C = \displaystyle \frac12 \prod_{p} \frac{1 - k_p/p}{1 - 1/p} = \frac12 \prod_{p} \frac{p-k_p}{p -1}$$

And in fact, that's what the standard number-theory conjectures say.

## Examples

Let's write a program for computing $C$, for a given $a$, $b$, and $c$:

```python
def slow_kp(p, f):
    """Number of solutions to f(n) == 0 (mod p)."""
    return len(n for n in range(p) if f(n) % p == 0)

def is_prime(p):
    for d in range(2, p):
        if p % d == 0: return False
        if d * d > p: break
    return True

def C(a, b, c):
    f =	lambda n: a * n	** 2 + b * n + c
    p =	1
    ans	= 0.5
    while True:
		p += 1
        if not is_prime(p): continue
        kp = slow_kp(p,	f)
        num = p	- kp
		den = p	- 1
		ans *= num
		ans /= den
		print('For p=%s, kp=%s so factor: (%s/%s) Now: %s' % (p, kp, num, den, ans))

if __name__ == '__main__':
    from builtins import input
    line = input('Enter a, b, c: ')
    a, b, c = [int(n) for n in line.strip().split()]
    print(C(a, b, c))
```

with an associated shell script:

```sh
function c() {  echo "$@" | gtimeout 5s python3 restart.py ; }
```

With this, we can get a few examples (invoke like `c 1 1 1` on the commandline):

* For $f(n) = n^2 + n + 1$, the constant is:
  $$ C = \frac12 \frac{2}{2} \frac{5}{4} \frac{5}{6} \frac{11}{10} \frac{11}{12} \frac{17}{16} \frac{17}{18} \frac{23}{22} \frac{29}{28} \cdots \approx 1.1$$

  ```
  For p=14639, kp=0 so factor: (14639/14638) Now: 1.1200882532554748
  For p=14653, kp=2 so factor: (14651/14652) Now: 1.120011807155744
  ```

  For $f(n) = n^2 + 21n + 1$, the constant is:

  $$C = \frac12 \frac{3}{2} \frac{5}{4} \frac{7}{6} \frac{11}{10} \frac{13}{12} \frac{17}{16} \frac{18}{18} \frac{22}{22} \frac{29}{28} \frac{31}{30} \frac{35}{36} \frac{41}{40} \frac{43}{42} \frac{45}{46} \frac{51}{52} \cdots \approx 2.8$$

  ```
  For p=14431, kp=2 so factor: (14429/14430) Now: 2.7957964457890743
  For p=14437, kp=2 so factor: (14435/14436) Now: 2.795602777429017
  ```

* For $f(n) = n^2 + n + 41$, the constant is $C \approx 3.3$:

  ```
  For p=14083, kp=2 so factor: (14081/14082) Now: 3.3226171521137924
  For p=14087, kp=2 so factor: (14085/14086) Now: 3.3223812712993586
  ```

  More exact value (per Cohen) is $\approx 3.319773177471421665323556857649887966468554585653\dots$.

* For $f(n) = n^2 + n + 75$, the constant is $C \approx 0.3$:

  ```
  For p=14087, kp=2 so factor: (14085/14086) Now: 0.3101518564741563
  For p=14107, kp=0 so factor: (14107/14106) Now: 0.310173843703454
  ```

  More exact value (per Cohen) is $\approx 0.310976679925987170004356287429628414529121902600\dots$.

## Context, references, etc.

Originally, my motivation for this question came from [Raziman's Google+ post](https://plus.google.com/+RazimanTV/posts/ZG1DHvi7pRu) (which linked to his answer to [a Quora question](https://www.quora.com/The-sequence-n-2-21n-1-n-1-2-3-cdots-seems-to-produce-more-than-twice-as-many-primes-as-the-sequence-n-2-n-1-n-1-2-3-cdots-How-can-I-make-this-precise-and-prove-it-or-is-it-even-true)):

> The sequence $n^2+21n+1$, for $n=1,2,3,\dots$, seems to produce more than twice as many primes as the sequence $n^2+n+1$, for $n=1,2,3,\dots$. How can I make this precise and prove it (or is it even true)?

The value of $\gcd(a, b, c)$ is known as the [content of the polynomial](https://en.wikipedia.org/wiki/Primitive_part_and_content).

It is beyond current mathematics to even prove that there are infinitely many primes of the form $n^2 + 1$: this is [Landau's Problem 4](https://en.wikipedia.org/w/index.php?title=Landau%27s_problems&oldid=825792061), presumably open for a long time but stated by Landau in 1912. For more general polynomials $f$ (including the quadratic polynomials considered here) the claim that $P(N) \to \infty$ is known as the [Bunyakovsky conjecture](https://en.wikipedia.org/w/index.php?title=Bunyakovsky_conjecture&oldid=830234069) and has been open since 1857.

The second part (along with the determination of the constant $C$) is [Hardy–Littlewood Conjecture F](https://en.wikipedia.org/w/index.php?title=Ulam_spiral&oldid=821475153#Hardy_and_Littlewood's_Conjecture_F) and has been open since 1923, and is a special case of the [Bateman–Horn conjecture](https://en.wikipedia.org/w/index.php?title=Bateman%E2%80%93Horn_conjecture&oldid=828694748) (1962).