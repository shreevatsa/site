---
layout: post
title: What happens eventually when you apply the divisibilty test
excerpt: Follow-up to previous post, based on ideas someone showed me.
date: 2018-11-17
tags: [done]

---



**Table of contents**
* TOC
{:toc}
## Recap

In the [previous post](divisibility-tests) (inspired by [this post on the mAnasa-taraMgiNI blog](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/)), we considered the following procedure, which is said to be “a folk Hindu method that was known in South India”, and is also found in the “*Vedic Mathematics*” book:

Given a number $p > 1$ not divisible by $2$ or $5$, let $k$ be the smallest number such that $ 10k - 1$ is divisble by $p$. Then, given any number $n$, repeatedly apply the following step:

* Write $n$ as $n = 10b + a$ (i.e. let $a$ be the last digit of $n$ and $b$ everything but the last digit),
* Replace $n$ with $n' = b + ka$.

This procedure constitutes a divisibility test for $p$, but our interest this time is the procedure itself. We can form a directed graph with edges from $n$ to $n'$ for every $n$, and ask about this graph. That is, we can ask what happens to a number $n$ as we repeatedly apply this step?

At [the end of the previous post](divisibility-tests.html#analysis-of-iteration-modulo-p), I mentioned that:

* When we look at numbers modulo $p$, this procedure is simply that of multiplying the number $n$ by $k = 10^{-1} \bmod p$ each time, so we can conclude many things about the graph from this.
* When we look at the actual numbers (not modulo $p$), then this is not the case, the graphs have a richer structure that is harder to say things about, and pointed to [the original post](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/).

Soon after I posted it, Twitter user [`@raktagulikaa` pointed out](https://twitter.com/raktagulikaa/status/1062197567591608320), using three nontrivial (to me) insights, that if we restrict our attention to the “eventual” behaviour of any number $n$ under this procedure — i.e. the directed cycle (possibly of size $1$, i.e. a single node) obtained by following outgoing edges starting from $n$ — then in fact it is possible to say a great deal using modular arithmetic, *even though we're looking at actual numbers* (i.e. we're working in $\mathbb{Z}$, not [$(\mathbb{Z}/n\mathbb{Z})^\times$](https://en.wikipedia.org/w/index.php?title=Multiplicative_group_of_integers_modulo_n&oldid=860470333)). The rest of this post reproduces the idea by `@raktagulikaa` (see linked Twitter thread above) that leads to an elegant answer.

## Theorem

Let $d = mp$ be be $9p$, $3p$, $7p$ or $p$ respectively, depending on whether $p$ ends with $1$, $3$, $7$ or $9$. Let $n \equiv_{d} r$ where $1 \le r \le d$, i.e. let $r$ be the remainder when $n$ is divided by $d$ (except that we replace $0$ with $d$). Then, the eventual behaviour (cycle) of $n$ is the same as that of $r$.

## Idea

The **first** insight is that $k$, which we said is the smallest number such that $10k \equiv_p 1$, can actually be determined directly from the value of $ p$ modulo $10$, and does not require “searching” to find. In detail: Write $p$ as $10q + r$, where $r$ is the remainder when $p$ is divided by $10$ (in other words, $r$ is the “last digit” of $p$ in decimal notation). As we said that $p$ is not divisible by $2$ or $5$, $r$ must be one of $1$, $3$, $7$, $9$. Now, what we want is to find $k$ such that $10k - 1$ is a multiple of $p$, say $mp$. Well, $mp = m(10q + r)$, so what we have is $10k - 1 = m(10q + r)$. If we look at this modulo $10$ (not modulo $p$!), we see that $-1 \equiv_{10} mr$ (or in simpler words: $mr$ must have last digit $9$), which means that if $r = 1, 3, 7, 9$ then $m \equiv_{10} 9, 3, 7, 1$ respectively. Conversely, if we pick $m$ this way and consider $k = (mp + 1)/10$, then clearly $10k - 1 = mp$ and our property is satisfied. To conclude:

* If $p$ ends in $1$, then take $k = (9p + 1)/10$
* If $p$ ends in $3$, then take $k = (3p + 1)/10$
* If $p$ ends in $7$, then take $k = (7p + 1)/10$
* If $p$ ends in $9$, then take $k = (p + 1)/10$

In all cases, note that $k \le p$ as expected.

The **second** insight is about the size of the numbers for which we see the “eventual” behaviour. Note that when $n$ is large (e.g. when it has many more digits than $k$), if we go from $n = 10b + a$ to $n' = b + ka$, then we're removing the rightmost digit from $n$ and adding $k$ times a single-digit number, so the resulting number $n'$ is smaller. When does this happen, i.e. when is $b + ka \lt 10b + a$? This is equivalent to $(k-1)a \lt 9b$, or $(10k - 10)a \lt 90b$, which is the same as (as we know the value of $k$):

* if $p$ ends in $1$, then $(9p - 9)a \lt 90b$ or $(p - 1)a \lt 10b$ which is the same as $n \gt pa$
* if $p$ ends in $3$, then $(3p - 9)a \lt 90b$ or $(p - 3)a \lt 30b$ which is the same as $n \gt pa/3$
* if $p$ ends in $7$, then $(7p-9)a \lt 90b$ which is the same as $n \gt 7pa/9$
* if $p$ ends in $9$, then $(p - 9)a \lt 90b$ which is the same as $n \gt pa/9$

As the largest possible value of $a$ is $9$, this means that when $n$ is larger than $9p$, $3p$, $7p$, $p$ (respectively, in the above four cases), then $n$ necessarily gets smaller. Therefore, starting at any number $n$, we will eventually hit a number that is at most $9p$, $3p$, $7p$, or $p$ respectively. (Though in theory it could become larger again.)

The **third** insight is that we can “lift” the multiplication by $k$ modulo $p$ to a multiplication modulo a higher multiple of $p$. Specifically, let's say that going from $n = 10b + a$ to $n' = b + ka$ is a multiplication by $k$ not only modulo $p$ but also modulo some number $d$, i.e. $n' \equiv_d kn$. This means that $d$ divides $kn - n' = k(10b + a) - (b + ka) = (10k-1)b$, whatever the value of $b$, so it must divide $(10k-1)$. Depending on the last digit of $p$, this is saying:

* if $p$ ends in $1$, that $d$ divides $9p$
* if $p$ ends in $3$, that $d$ divides $3p$
* if $p$ ends in $7$, that $d$ divides $7p$
* if $p$ ends in $9$, that $d$ divides $p$

Conveniently (coincidence?), these are also the limits we found beyond which the number is guaranteed to get smaller.

Putting all this together, we can conclude the following:

* Let $d$ be $9p$, $3p$, $7p$ or $p$ respectively, depending on whether $p$ ends with $1$, $3$, $7$ or $9$.
* The operation from going from $n = 10b + a$ to $n' = b + ka$ is in fact a multiplication by $k$ modulo $d$.
* Eventually, this operation (on the integers) will result in a number that is between $1$ and $d$, inclusive — at this point, the operation (modulo $d$) woudl have reached the same number.
* Therefore, given any number $n$, if $n \equiv_d r$ where $1 \le r \le d$, then the eventual behaviour of $n$ is the same as that of $r$.

To make this even more precise, and to verify that our reasoning hasn't led to any sloppy errors, let's turn it into code.

## Code

Normally I like to just write free-standing functions, but in this case everything depends on a value $p$, so we'll use a class constructed using a given value $p$, and write most functions inside that class.

Given a number $p$, we can define $k$ and the operation representing a single step of our iteration. Python code:

```python
class P():
    def __init__(self, p):
        assert p % 2 != 0 and p % 5 != 0
        self.p = p
        self.m, self.k = self.find_k()

    def find_k(self):
        p = self.p
        # Slow method: try all k until 10k = 1 (mod p)
        ans1 = min(k for k in range(p) if (10 * k - 1) % p == 0)
        # Fast method: use the last digit of p
        m = {1: 9, 3: 3, 7: 7, 9: 1}[p % 10]
        assert (m * p + 1) % 10 == 0
        ans2 = (m * p + 1) // 10
        assert ans1 == ans2
        return m, ans2
    
    def step(self, n):
        """Given n = 10b + a, return n' = b + ka."""
        a = n % 10
        b = (n - a) // 10
        assert n == 10 * b + a
        return b + self.k * a
```

To find the eventual behaviour under iteration of a function (like the `step` above) that is known to eventually end up in a loop (possibly of length $1$), there is an [elegant idea](https://en.wikipedia.org/w/index.php?title=Cycle_detection&oldid=868883990#Floyd's_Tortoise_and_Hare) that uses constant memory and dates back to Floyd; known as “tortoise and hare” among other names. But for working with small primes, we won't bother with that:

```python
def find_cycle(a, f):
    """Records the evolution of `a` under repeated application of `f`,
    as a "tail" part and a "cycle" part."""
    x = a 
    seen = set()
    while x not in seen:
        seen.add(x)
        x = f(x)
    # x has been seen more than once, so it's part of a cycle
    # First get the part before x
    t = a
    tail = []
    while t != x:
        tail.append(t)
        t = f(t)
    # Now we want 'cycle' to be [x, f(x), f(f(x))....,]
    y = f(x)
    cycle = [x]
    while y != x:
        cycle.append(y)
        y = f(y)
    return tail, cycle
```

We can use this function to extend our class from earlier:

```python
    def print_evolution(self, n):
        tail, cycle = find_cycle(n, self.step)
        print("For p=%d (k=%d), evolution of %d: " % (self.p, self.k, n))
        print(' '.join(str(n) for n in tail), cycle)
```

We can verify this with a few cases, in an interactive Python shell (compare against Figure 2 and Figure 3 [in the original post](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/)):

```python
>>> P(13).print_evolution(199)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 199: 		199 55 [25, 22, 10, 1, 4, 16]

>>> P(13).print_evolution(167)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 167: 		167 44 [20, 2, 8, 32, 11, 5]

>>> P(13).print_evolution(158)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 158: 		158 47 [32, 11, 5, 20, 2, 8]

>>> P(13).print_evolution(119)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 119: 		119 47 [32, 11, 5, 20, 2, 8]

>>> P(13).print_evolution(198)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 198: 		198 51 [9, 36, 27, 30, 3, 12]

>>> P(13).print_evolution(143)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 143: 		143 [26]

>>> P(13).print_evolution(169)                                                                                                                                                                                                       
For p=13 (k=4), evolution of 169: 		169 52 [13]


>>> P(7).print_evolution(158)                                                                                                                                                                                                        
For p=7 (k=5), evolution of 158: 		158 55 [30, 3, 15, 26, 32, 13, 16, 31, 8, 40, 4, 20, 2, 10, 1, 5, 25, 27, 37, 38, 43, 19, 46, 34, 23, 17, 36, 33, 18, 41, 9, 45, 29, 47, 39, 48, 44, 24, 22, 12, 11, 6]

>>> P(7).print_evolution(119)                                                                                                                                                                                                       
For p=7 (k=5), evolution of 119: 		119 56 [35, 28, 42, 14, 21, 7]

>>> P(7).print_evolution(196)                                                                                                                                                                                                       
For p=7 (k=5), evolution of 196: 		196 [49]
```

(Note there is a minor difference relative to the post, in what we do with $p=7$ after reaching $7$: applying the rule again, with $k=5$, gives $35$ which eventually cycles back to $7$; while in the original post one stays at $7$ after reaching $7$. The latter makes sense as a divisibilty rule; the former makes sense as the mechanical application of the procedure.)

To avoid confusion caused by printing the same cycle in different ways (consider, for $p=13$, the cases of $n = 167$ and $n = 158$ above, where we printed the same cycle once as `[20, 2, 8, 32, 11, 5]` and once as `[32, 11, 5, 20, 2, 8]`), we'd like to print the cycle in a canonical form (considering cyclic shifts), say ending with the least element:

```python
def end_with_min(xs):
    """Cyclic shift of list xs, to end with its smallest element."""
    x = min(xs)
    i = xs.index(x)
    return xs[i + 1:] + xs[:i + 1]
```

Now let's write down the main theorem from this post, that we can get the eventual cycle without computing all the initial terms:

```python
    def eventual_cycle(self, n):
        if n == 0: return [0]
        d = self.m * self.p
        # Replace n with its representative mod d
        n = n % d
        if n == 0: n = d
        # Iterate starting at n
        # We want `cycle` to be [n, f(n), f(f(n)), ...]
        cycle = [n]
        y = self.step(n)
        while y != n:
            cycle.append(y)
            y = self.step(y)
        return end_with_min(cycle)    
```

To verify whether this is correct, we can compare the results of the two methods:

```python
    def verify(self, n):
        tail, cycle = find_cycle(n, self.step)
        print("Verifying p=%d (k=%d), n=%d: " % (self.p, self.k, n), end=" ")
        print(' '.join(str(n) for n in tail), cycle)
        slow = end_with_min(cycle); print("Cycle (slow): ", slow)
        fast = self.eventual_cycle(n); print("Cycle (fast): ", fast)
        return slow == fast
```

We can hack up a function to verify a dozen random $30$-digit numbers $n$ for a given $p$:

```python
def verify_p(p, num=12, exhaustive=False):
    import random
    c = P(p)
    if exhaustive:
        # Verify all nonzero numbers up to 10*p
        for n in range(1, 10*p + 1):
            assert c.verify(n)
    for attempt in range(num):
        n = int(''.join(random.choice('0123456789') for _ in range(30)))
        assert c.verify(n)
```

And a function to pick a few random $4$-digit numbers $p$ to verify:

```python
def verify_many():
    import random
    for _ in range(100):
        q = int(''.join(random.choice('0123456789') for _ in range(3)))
        r = random.choice([1, 3, 7, 9])
        verify_p(10 * q + r)
```

Putting all this together (verify numbers up to $100$ exhaustively, then a random hundred $4$-digit numbers with a dozen random samples each):

```python
if __name__ == '__main__':
    for p in range(3, 100):
        if p % 2 == 0 or p % 5 == 0: continue
        verify_p(p, exhaustive=True)
    verify_many()
```

(All these snippets are collected together as a single file in “appendix” below; when run as `python3 appendix.py` it runs for some 10 seconds.) Here is an example block of output from the program:

```
Verifying p=17 (k=12), n=544158072165504802875697337734:  544158072165504802875697337734 54415807216550480287569733821 5441580721655048028756973394 544158072165504802875697387 54415807216550480287569822 5441580721655048028757006 544158072165504802875772 54415807216550480287601 5441580721655048028772 544158072165504802901 54415807216550480302 5441580721655048054 544158072165504853 54415807216550521 5441580721655064 544158072165554 54415807216603 5441580721696 544158072241 54415807236 5441580795 544158139 54415921 5441604 544208 54516 5523 588 154 [63, 42, 28, 98, 105, 70, 7, 84, 56, 77, 91, 21, 14, 49, 112, 35]
Cycle (slow):  [84, 56, 77, 91, 21, 14, 49, 112, 35, 63, 42, 28, 98, 105, 70, 7]
Cycle (fast):  [84, 56, 77, 91, 21, 14, 49, 112, 35, 63, 42, 28, 98, 105, 70, 7]
```

What this example shows is that for $p = 17$, applying the rule starting with the $30$-digit number $n = 544158072165504802875697337734$ eventually results in a cycle of length $16$, and we can find this cycle directly as the cycle containing $98$ (as $n \equiv_{119} 98$), without having to carry out all the computation.

## Further conclusions

Now that the code gives us additional confidence that our theorem is indeed correct, let's state what else we can say about the eventual behaviour (cycle) of $n$.

Note that modulo $d = mp$, the number we're multiplying by, namely $k = (mp + 1)/10$, is such that $10k = (mp + 1) \equiv_{mp} 1$ as well. So the multiplicative order (call it $r$) of $k$ modulo $d$ is the same as the multiplicative order of $10$ modulo $d$. (In other words: $k \equiv_d 10^{-1}$ so multiplying by $k$ is the same as dividing by $10$, and that's what we're doing each time.)

Suppose we start with a number $n$. Then, modulo $d$, we cycle through $n, kn, k^2n, \dots$, until something repeats.

Let's say the repetitions are for $k^an \equiv_d k^bn$, where $0 \le a < b$. This means that $d$ divides $k^bn - k^an = k^a(k^{b-a}n - n)$, so $d$ must divide $k^{b-a}n - n$ (as $k$ is relatively prime to $d$). That is, the first element that repeats is already the one we started with — we can assume that $a = 0$.

Further, $d$ dividing $k^{b}n - n = (k^b - 1)n$ means that $\frac{d}{\gcd(n, d)}$ divides $(k^b - 1) \frac{n}{\gcd(n ,d)}$, and in fact its first factor (as it's relatively prime to the second). The first time this happens is for $b$ being the multiplicative order of $k$ (and remember, therefore of $10$) modulo $\frac{d}{\gcd(n, d)}$.

**Conclusion**: the eventual behaviour of $n$ is that it falls into a cycle whose length is the multiplicative order of $10$ modulo $\frac{mp}{\gcd(n, mp)}$, where $m$ is $9$, $3$, $7$ or $1$ depending on whether the last digit of $p$ is $1$, $3$, $7$ or $9$ respectively.

For example, for prime $p > 7$ ending in $7$ (and therefore $m=7$), the cases are:

* if $n$ is divisible by both $p$ and $7$, then it falls into a cycle of length $1$ (namely $[7p]$)
* if $n$ is divisble by $p$ but not $7$, then it falls into a cycle of length $6$ (namely, the one containing $p, 2p \dots, 6p$ in some order)
* if $n$ is divisible by $7$ but not $p$, then it falls into a cycle of length the order of $10$ modulo $p$
* if $n$ is divisible by neither $p$ nor $7$, then it falls into a cycle of length the order of $10$ modulo $7p$.

And we can make similar tables extending to other final digits of $p$, small $p$, non-prime $p$, etc.

This explains why, for example, for $p=17$, we see that $n=6$ falls into a cycle of length $48$ (which is the order of $10$ modulo $7 \times 17 = 119$), while $n = 7$ falls into a cycle of length $16$ (which is the order of $10$ modulo $17$).

----

## Appendix

Just repeating the code that is scattered across multiple snippets above, into a single file. The only change is that I moved `import random` to the top of the file.

```python
import random

def find_cycle(a, f):
    """Records the evolution of `a` under repeated application of `f`,
    as a "tail" part and a "cycle" part."""
    x = a 
    seen = set()
    while x not in seen:
        seen.add(x)
        x = f(x)
    # x has been seen more than once, so it's part of a cycle
    # First get the part before x
    t = a
    tail = []
    while t != x:
        tail.append(t)
        t = f(t)
    # Now we want 'cycle' to be [x, f(x), f(f(x))....,]
    y = f(x)
    cycle = [x]
    while y != x:
        cycle.append(y)
        y = f(y)
    return tail, cycle

def end_with_min(xs):
    """Cyclic shift of list xs, to end with its smallest element."""
    x = min(xs)
    i = xs.index(x)
    return xs[i + 1:] + xs[:i + 1]


class P():
    def __init__(self, p):
        assert p % 2 != 0 and p % 5 != 0
        self.p = p
        self.m, self.k = self.find_k()

    def find_k(self):
        p = self.p
        # Slow method: try all k until 10k = 1 (mod p)
        ans1 = min(k for k in range(p) if (10 * k - 1) % p == 0)
        # Fast method: use the last digit of p
        m = {1: 9, 3: 3, 7: 7, 9: 1}[p % 10]
        assert (m * p + 1) % 10 == 0
        ans2 = (m * p + 1) // 10
        assert ans1 == ans2, (self.p, m, ans1, ans2)
        return m, ans2
    
    def step(self, n):
        """Given n = 10b + a, return n' = b + ka."""
        a = n % 10
        b = (n - a) // 10
        assert n == 10 * b + a
        return b + self.k * a

    def print_evolution(self, n):
        tail, cycle = find_cycle(n, self.step)
        print("For p=%d (k=%d), evolution of %d: " % (self.p, self.k, n))
        print(' '.join(str(n) for n in tail), cycle)

    def eventual_cycle(self, n):
        if n == 0: return [0]
        d = self.m * self.p
        # Replace n with its representative mod d
        n = n % d
        if n == 0: n = d
        # Iterate starting at n
        # We want `cycle` to be [n, f(n), f(f(n)), ...]
        cycle = [n]
        y = self.step(n)
        while y != n:
            cycle.append(y)
            y = self.step(y)
        return end_with_min(cycle)    

    def verify(self, n):
        tail, cycle = find_cycle(n, self.step)
        print("Verifying p=%d (k=%d), n=%d: " % (self.p, self.k, n), end=" ")
        print(' '.join(str(n) for n in tail), cycle)
        slow = end_with_min(cycle); print("Cycle (slow): ", slow)
        fast = self.eventual_cycle(n); print("Cycle (fast): ", fast)
        return slow == fast

def verify_p(p, num=12, exhaustive=False):
    c = P(p)
    if exhaustive:
        # Verify all nonzero numbers up to 10*p
        for n in range(1, 10*p + 1):
            assert c.verify(n)
    for attempt in range(num):
        n = int(''.join(random.choice('0123456789') for _ in range(30)))
        assert c.verify(n)

def verify_many():
    for _ in range(100):
        q = int(''.join(random.choice('0123456789') for _ in range(3)))
        r = random.choice([1, 3, 7, 9])
        verify_p(10 * q + r)

if __name__ == '__main__':
    for p in range(3, 100):
        if p % 2 == 0 or p % 5 == 0: continue
        verify_p(p, exhaustive=True)
    verify_many()
```

----

