---
layout: post
title: Primes in quadratic sequences (Part 2)
excerpt: Computing the proportion of prime values of a quadratic polynomial
date: 2018-04-14
---



----

## Story so far





## An expression for $k_p$ (and $C$)

The above algorithm/program works, and of course the `is_prime` function could be improved, but most of its time taken is because of the fact that for each $p$, it takes $\Theta(p) $ time to compute $k_p$, the number of solutions modulo $p$ to $an^2 + bn + c \equiv 0$. With some theory, we can do better.

**First**, for $p=2$, we have $n^2 \equiv n$ always, so $an^2 + bn + c \equiv (a+b)n + c$, and either $(a + b) \equiv 1$, in which case $k_2 = 1$, or $(a + b) \equiv 0$ (and $c \not\equiv 0$ by assumption that $f(n)$ is not always even) in which case $k_2 = 0$. So $k_2$ is very easy to compute: it is

$$\displaystyle k_2 = \begin{cases}0 &\text{if }a+b \equiv 0 \pmod 2, \\ 1&\text{otherwise} \end{cases}$$

**Next**, if $p$ divides $a$, then we have $an^2 + bn + c \equiv bn + c \pmod p$, and now either $p$ divides $b$ as well (in which case $k_p = 0$ by assumption that $f(n)$ is not always divisible by $p$), or it does not, in which case $bn + c \equiv 0 \pmod p$ has a unique solution $n \equiv b^{-1}(-c)$. So again, when $p$ divides $a$, we have:

$$\displaystyle k_p = \begin{cases}0 &\text{if } p\text{ divides }b \\ 1&\text{otherwise}\end{cases}$$

**For other** $p$ (odd primes that don't divide $a$), we can solve $an^2 + bn + c \equiv 0 \pmod p$ just like a regular quadratic equation, by completing the square: by multiplying by $4a$, the original equation is equivalent to $4an^2 + 4abn + 4ac \equiv 0$, so $(2an+b)^2 - b^2 + 4ac \equiv 0$, or $(2an+b)^2 \equiv b^2 - 4ac$. Let $D$ stand for the discriminant, $b^2 - 4ac$. Now, given any solution to $x^2 \equiv D$, we can solve $2an + b \equiv x$ to get $n = (2a)^{-1}(x - b)$.

This means that $k_p$ is precisely the number of solutions (modulo $p$) to $x^2 \equiv D \pmod p$. This is

$$k_p = \displaystyle \begin{cases} 0&\text{if }D\text{ is not a quadratic residue mod }p \\ 1 &\text{if }p\text{ divides }D \\ 2 &\text{otherwise}\end{cases}$$

In number theory there exists the [Legendre symbol](https://en.wikipedia.org/w/index.php?title=Legendre_symbol&oldid=805985930) that has a very similar definition, and in fact we can see that

$$\displaystyle k_p = 1 + \left(\frac{D}{p}\right) $$

So our expression for $C$ becomes:

$$\displaystyle \begin{align}C &= \frac12\prod_p\frac{p-k_p}{p -1} \\ &= \frac12\prod_{p\mid 2a} \frac{p-k_p}{p -1} \prod_{p \nmid 2a} \frac{p-k_p}{p -1} \\&=  \frac12\prod_{p\mid 2a} \frac{p-k_p}{p -1} \prod_{p \nmid 2a} \frac{p-1 - (D/p)}{p -1} \\ &= C_0 C' \end{align}$$

where the first factor 

$\displaystyle C_0 = \left(\frac{1 + [(a+b)\text{ is even}]}{2} \mathop{\prod_{p\mid (a,b)}}_{p > 2} \frac{p}{p -1}\right)$

is a product over just a few primes (those dividing both $a$ and $b$) and can be computed quickly, and

$\displaystyle C' = \prod_{p \nmid 2a} \left(1 - \frac{(D/p)}{p -1}\right).$

Though we won't use it immediately, we can also write this $C'$ as 

$\displaystyle C'  = \prod_{p > 2} \left(1 - \frac{(D/p)}{p -1}\right) / \prod_{p \mid a, p > 2} \left(1 - \frac{(D/p)}{p -1}\right) = \prod_{p > 2} \left(1 - \frac{(D/p)}{p -1}\right) \mathop{\prod_{p\mid a}}_{p \nmid 2b} \frac{p-1}{p-2}$

We can test that this is equivalent to our previous code, by replacing the code (note changes to `slow_kp`) with the following functions:

```python
def legendre_symbol(D, p):
    if D % p == 0: return 0
    return 1 if any((x*x - D) % p == 0 for x in range(p)) else -1

def slow_kp(p, a, b, c):
    """Number of solutions to an^2+bn+c == 0 (mod p)."""
    assert (2*a) % p != 0
    D = b * b - 4 * a * c
    return 1 + legendre_symbol(D, p)

def is_prime(p):
    return all(p % d != 0 for d in range(2, p))

def C(a, b, c):
    p = 1
    ans = 1.0
    while True:
        p += 1
        if not is_prime(p): continue
        if p == 2:
            num = 1 + int((a + b) % 2 == 0)
            den = 2
        elif a % p == 0:
            (num, den) = (p, p - 1) if b % p == 0 else (1, 1)
        else:
            kp = slow_kp(p, a, b, c)
            num = p - kp
            den = p - 1
        ans *= num
        ans /= den
        print('For p=%s, factor: (%s/%s) Now: %s' % (p, num, den, ans))

if __name__ == '__main__':
    from builtins import input
    line = input('Enter a, b, c: ')
    a, b, c = [int(n) for n in line.strip().split()]
    print(C(a, b, c))
```

This tests slightly more primes in the same amount of time, but is otherwise equivalent.

## Faster computation of $k_p$

Recall the expressions we got earlier for $k_p$ and for $C$:

$$\displaystyle k_p = 1 + \left(\frac{D}{p}\right) $$

and

$$\displaystyle C = C_0 C'$$ where $\displaystyle C_0 = \left(\frac{1 + [(a+b)\text{ is even}]}{2} \mathop{\prod_{p\mid \gcd(a,b)}}_{p > 2} \frac{p}{p -1}\right)$ and $\displaystyle C' = \prod_{p \nmid 2a} \left(1 - \frac{(D/p)}{p -1}\right)$

As $C_0$ is trivial to compute, let's focus on $C'$. For a given prime $p$, we're still taking $\Theta(p)$ time to compute $(D/p)$, in the worst case (non-residue), which happens about half the time. With some theory, we can do better. The relevant theory is quadratic reciprocity. 

If $p$ divides $D$, then $(D/p)$ can be computed instantly, as $0$. Else, suppose that $D = d^2e$, where $e$ is square free (a product of distinct primes). Then, $x^2 \equiv d^2e \pmod p$ is equivalent to $(x/d)^2 \equiv e \pmod p$, i.e. $(D/p) = (e/p)$. Let's write $e$, the square-free part of $D$, as a product of distinct odd primes $q_1 q_2 \cdots q_r$ possibly multiplied by $-1$ and by $2$. Then quadratic reciprocity states that (if $q$ is an odd prime, as is $p$, and if $q \neq p$, as we've assumed):

$\displaystyle \left({\frac {q}{p}}\right)\left({\frac {p}{q}}\right)=(-1)^{\tfrac{p-1}{2}\cdot {\tfrac {q-1}{2}}}$

or 

$$\displaystyle \left({\frac {q}{p}}\right)=(-1)^{\tfrac {p-1}{2}\cdot {\tfrac {q-1}{2}}}\left({\frac {p}{q}}\right)$$

so we have:

$$\displaystyle \left(\frac{D}{p}\right) = \epsilon_{-1}\epsilon_{2}\prod_{i=1}^{r} (-1)^{\tfrac {p-1}{2}\cdot {\tfrac {q_i-1}{2}}}\left({\frac {p}{q_i}}\right)$$

where $\epsilon_{-1} = \left(\frac{-1}{p}\right)^{[D<0]} = (-1)^{[D<0]\frac{p-1}{2}}$ and $\epsilon_2 = \left(\frac{2}{p}\right)^{[2\mid D]} = (-1)^{[2\mid D]\frac{p^2-1}{8}}$.

Note that each $(p/q_i)$ only depends on the value of $p$ mod $q_i$, and thus can be pre-computed for each $q_i$ and each possible value. Even computing it with a very slow approach will do. The value of $(D/p)$ depends only on the value of $p$ modulo each of the $q_i$s and modulo $8$ (at most), so we could even pre-compute a list of size $8D$.

We can put together everything we've learned, into the following program (with a slightly faster `is_prime`):

```python
def is_prime(p):
    for d in range(2, p):
        if p % d == 0: return False
        if d * d > p: break
    return True

def factorize(D):
    """Return a list of distinct prime factors of D."""
    ans = []
    if D < 0:
        ans.append(-1)
        D = -D
    p = 1
    while p * p <= D:
        p += 1
        if not is_prime(p): continue
        while D % (p * p) == 0: D //= (p * p)
        if D % p == 0:
            ans.append(p)
            D //= p
            assert D % p != 0
    if D != 1: ans.append(D)
    return ans
    
D = None
factors = None
legendre_symbols = {}

def legendre_symbol_D(p):
    global D, factors, legendre_symbols
    if D % p == 0: return 0
    ans = 1
    for q in factors:
        cur = None
        if q == -1:
            cur = -1 if ((p - 1) / 2) % 2 else 1
        elif q == 2:
            cur = -1 if ((p * p - 1) / 8) % 2 else 1
        else:
            cur = (-1 if ((p - 1) / 2 * (q - 1) / 2) % 2 else 1) * legendre_symbols[q][p % q]
        ans *= cur
    # Before returning, check against the slow version
    # slow = 1 if any((x*x - D) % p == 0 for x in range(p)) else -1
    # assert slow == ans, 'Got %s instead of %s' % (ans, slow)
    return ans

def C(a, b, c):
    p = 1
    C0 = 1.0
    C1 = 1.0
    C2 = 1.0
    while True:
        p += 1
        if not is_prime(p): continue
        if p == 2:
            C0 *= 1 + int((a + b) % 2 == 0)
            C0 /= 2
        elif a % p == 0:
            (num, den) = (p, p - 1) if b % p == 0 else (1, 1)
            C0 *= num
            C0 /= den
        else:
            kp = 1 + legendre_symbol_D(p)
            dp = legendre_symbol_D(p)
            C1 *= p - dp
            C1 /= p
            C2 *= p * (p - 1 - dp)
            C2 /= (p-1) * (p - dp)
        ans = C0 * C1 * C2
        print('For p=%s, C0=%.12f C1=%.12f C2=%.12f Ans: %s' % (p, C0, C1, C2, ans))


def C(a, b, c):
    global D, factors, legendre_symbols
    p = 1
    ans = 1.0
    D = b * b - 4 * a * c
    factors = factorize(D)
    for q in factors:
        if q == -1 or q == 2: continue
        squares = set((x * x) % q for x in range(q))
        legendre_symbols[q] = {r: 1 if r in squares else -1 for r in range(q)}
    while True:
        p += 1
        if not is_prime(p): continue
        if p == 2:
            num = 1 + int((a + b) % 2 == 0)
            den = 2
        elif a % p == 0:
            (num, den) = (p, p - 1) if b % p == 0 else (1, 1)
        else:
            kp = 1 + legendre_symbol_D(p)
            num = p - 1 - dp
            den = p - 1
        ans *= num
        ans /= den
        print('For p=%s, factor: (%s/%s) Now: %s' % (p, num, den, ans))

if __name__ == '__main__':
    from builtins import input
    line = input('Enter a, b, c: ')
    a, b, c = [int(n) for n in line.strip().split()]
    print(C(a, b, c))
```

This time, we get (also showing the output from the earlier program, for comparison):

- For $f(n) = n^2 + n + 1$, the constant is: $C \approx 1.1$:

  ```
  For p=14639, kp=0 so factor: (14639/14638) Now: 1.1200882532554748
  For p=14653, kp=2 so factor: (14651/14652) Now: 1.120011807155744
  ...
  For p=418051, factor: (418049/418050) Now: 1.1205994914366477
  For p=418069, factor: (418067/418068) Now: 1.1205968110126703
  ```

  For $f(n) = n^2 + 21n + 1$, the constant is: $C \approx 2.8$:

  ```
  For p=14431, kp=2 so factor: (14429/14430) Now: 2.7957964457890743
  For p=14437, kp=2 so factor: (14435/14436) Now: 2.795602777429017
  ...
  For p=416623, factor: (416623/416622) Now: 2.792225965551853
  For p=416629, factor: (416629/416628) Now: 2.7922326675161124
  ```

- For $f(n) = n^2 + n + 41$, the constant is $C \approx 3.3$:

  ```
  For p=14083, kp=2 so factor: (14081/14082) Now: 3.3226171521137924
  For p=14087, kp=2 so factor: (14085/14086) Now: 3.3223812712993586
  ...
  For p=417311, factor: (417311/417310) Now: 3.320329680372263
  For p=417317, factor: (417317/417316) Now: 3.320337636764255
  ```

  More exact value (per Cohen) is $\approx 3.319773177471421665323556857649887966468554585653\dots$.

- For $f(n) = n^2 + n + 75$, the constant is $C \approx 0.3$:

  ```
  For p=14087, kp=2 so factor: (14085/14086) Now: 0.3101518564741563
  For p=14107, kp=0 so factor: (14107/14106) Now: 0.310173843703454
  ...
  For p=450403, factor: (450401/450402) Now: 0.31089670955477566
  For p=450413, factor: (450413/450412) Now: 0.31089739980439063
  ```

  More exact value (per Cohen) is $\approx 0.310976679925987170004356287429628414529121902600\dots$.

As we can see, we can consider a lot more primes than earlier, yet the convergence leaves something to be desired. To improve the convergence, we need more theory.

## Another expression for $C'$

Recall that, to compute $C = C_0 C'$, we're trying to compute $\displaystyle C' = \prod_{p \nmid 2a} \left(1 - \frac{(D/p)}{p -1}\right)$.

It turns out that, if instead of $p-1$ we replace the denominator by $p$, then the expression is something better known. That is, we can write our product as:

$$\displaystyle \prod_{p} \left(1 - \frac{(D/p)}{p -1}\right) = \prod_{p} \left(1 - \frac{(D/p)}{p}\right) \frac{\left(1 - \frac{(D/p)}{p -1}\right)}{\left(1 - \frac{(D/p)}{p}\right)} = \prod_{p} \left(1 - \frac{(D/p)}{p}\right) \prod_{p}\frac{\left(1 - \frac{(D/p)}{p -1}\right)}{\left(1 - \frac{(D/p)}{p}\right)}$$

where the products are taken over the same set of primes (like $p\nmid 2a$).

Let's incorporate this into our program: write $C = C_0 C'$ as $C = C_0C_1C_2$ where $C_0$ is as defined earlier, $\displaystyle C_1 = \prod_{p\nmid 2a} \left(1 - \frac{(D/p)}{p}\right)$ and $\displaystyle C_2 = \prod_{p\nmid 2a}\frac{\left(1 - \frac{(D/p)}{p -1}\right)}{\left(1 - \frac{(D/p)}{p}\right)}$. We change our `def C(a, b, c)` function to:

```python
def C(a, b, c):
    global D, factors, legendre_symbols
    D = b * b - 4 * a * c
    factors = factorize(D)
    for q in factors:
        if q == -1 or q == 2: continue
        squares = set((x * x) % q for x in range(q))
        legendre_symbols[q] = {r: 1 if r in squares else -1 for r in range(q)}
    C0 = 1.0
    C1 = 1.0
    C2 = 1.0
    p = 1
    while True:
        p += 1
        if not is_prime(p): continue
        if p == 2:
            C0 *= 1 + int((a + b) % 2 == 0)
            C0 /= 2
        elif a % p == 0:
            (num, den) = (p, p - 1) if b % p == 0 else (1, 1)
            C0 *= num
            C0 /= den
        else:
            kp = 1 + legendre_symbol_D(p)
            dp = legendre_symbol_D(p)
            C1 *= p - dp
            C1 /= p
            C2 *= p * (p - 1 - dp)
            C2 /= (p-1) * (p - dp)
        ans = C0 * C1 * C2
        print('For p=%s, C0=%f C1=%.12f C2=%.12f Ans: %s' % (p, C0, C1, C2, ans))
```

This gives output like:

```
% c 1 1 1
...
For p=402847, C0=1.000000 C1=1.102566103841 C2=1.016392177900 Ans: 1.1206395635608977
For p=402851, C0=1.000000 C1=1.102568840749 C2=1.016392177906 Ans: 1.1206423453396333
```

```
% c 1 21 1
...
For p=401507, C0=1.000000 C1=2.289689273579 C2=1.219571141267 Ans: 2.7924389605246103
For p=401519, C0=1.000000 C1=2.289683571011 C2=1.219571141259 Ans: 2.7924320058203116
```

```
% c 1 1 41
...
For p=434597, C0=1.000000 C1=2.710002676073 C2=1.225337546653 Ans: 3.320668030521408
For p=434611, C0=1.000000 C1=2.709996440606 C2=1.225337546646 Ans: 3.320660389951632
```

More exact value (per Cohen) is $\approx 3.319773177471421665323556857649887966468554585653\dots$.

```
% c 1 1 75
...
For p=403831, C0=1.000000 C1=0.458580612158 C2=0.677990091802 Ans: 0.3109131113352235
For p=403849, C0=1.000000 C1=0.458581747683 C2=0.677990091806 Ans: 0.31091388121178926
```

More exact value (per Cohen) is $\approx 0.310976679925987170004356287429628414529121902600\dots$.

As we can see, $C_2$ converges faster, so if we could compute $C_1$ to converge faster, then we'd have faster convergence of our answer. For this, we need more theory.

## Faster computation of $C_1$

We'd like to compute $\displaystyle C_1 = \prod_{p\nmid 2a} \left(1 - \frac{(D/p)}{p}\right)$.

As we saw earlier, $\displaystyle \left(\frac{D}{p}\right) = \epsilon_{-1}\epsilon_{2}\prod_{i=1}^{r} (-1)^{\tfrac {p-1}{2}\cdot {\tfrac {q_i-1}{2}}}\left({\frac {p}{q_i}}\right)$ is (if we consider only the expression on the RHS and don't worry about $p$ being a prime or not) a periodic function of $p$, repeating with period at most $8D$. Let $q$ be its actual (minimal) period. (Based on what we saw earlier, $q$ is $\prod\limits_{i=1}^r q_i$ multiplied by either $1$, $2$, $4$ or $8$.) Let's write $\chi_D$ for this function, i.e. 

$\displaystyle \chi_D(n)= \epsilon_{-1}\epsilon_{2}\prod_{i=1}^{r} (-1)^{\tfrac {n-1}{2}\cdot {\tfrac {q_i-1}{2}}}\left({\frac {n}{q_i}}\right)$ 

so that $\chi_D(n) = \left(\frac{D}{n}\right)$ when $n$ is an odd prime. (Note that the equality does not hold for arbitrary $n$, because $\chi_D(n)$ is **not** the function $\left(\frac{D}{n}\right)$ but a periodic function that just happens to coincide on the primes.)

This $\chi_D(n)$ has some interesting properties:

- As mentioned, it's periodic with period $q$, i.e. $\chi_D(n + q) = \chi_D(n)$ for all $n$ (and it has no smaller period).
- $\chi_D(n)$ is nonzero precisely when $\gcd(n, q) = 1$.
- $ \chi_D(mn) = \chi_D(m)\chi_D(n)$(in words: $\chi_D$ is completely multiplicative)

A function with these properties is called a primitive Dirichlet character of modulus $q$. We can define a coressponding $L$-function  (or $L$-series) as:

$\displaystyle L(s,\chi_D) = \sum_{n=1}^\infty \frac{\chi_D(n)}{n^s}$

and we can write it as a Euler product, because it is completely multiplicative:

$$\begin{align} L(s,\chi_D) &= \sum_{n=1}^\infty \frac{\chi_D(n)}{n^s} \\ &= 1 + \frac{\chi_D(2)}{2^s} + \frac{\chi_D(3)}{3^s} + \frac{\chi_D(4)}{4^s} + \dots \\ &= \prod_p\left(1 + \frac{\chi_D(p)}{p^s} + \frac{\chi_D(p^2)}{p^{2s}} + \frac{\chi_D(p^3)}{p^{3s}} + \dots \right) \\ &=\prod_p\left(\frac{1}{1 - \frac{\chi_D(p)}{p^s}} \right) \end{align}$$

In other words,

$\displaystyle \frac{1}{L(s, \chi_D)} = \prod_p\left(1 - \frac{\chi_D(p)}{p^s}\right)$

and in particular, 

$\displaystyle C_1 = \prod_{p \nmid 2a} \left(1 - \frac{\chi_D(p)}{p}\right) = \frac{\prod\limits_{p} \left(1 - \frac{\chi_D(p)}{p}\right)}{\prod\limits_{p \mid 2a} \left(1 - \frac{\chi_D(p)}{p}\right)} = \frac{1}{\prod\limits_{p \mid 2a} \left(1 - \frac{\chi_D(p)}{p}\right)L(1, \chi_D)}$

so our original constant is

$\displaystyle C = C_0 C_1 C_2 = \left(\frac{1 + [(a+b)\text{ is even}]}{2} \mathop{\prod_{p\mid \gcd(a,b)}}_{p > 2} \frac{p}{p -1}\right) \frac{1}{\prod\limits_{p \mid 2a} \left(1 - \frac{\chi_D(p)}{p}\right)L(1, \chi_D)} \prod_{p\nmid 2a}\frac{\left(1 - \frac{(D/p)}{p -1}\right)}{\left(1 - \frac{(D/p)}{p}\right)}$

where the last product converges reasonably quickly (better than our original), most of the rest are finite products, and the main remaining challenge is to compute $L(1, \chi_D)$.

## Computing the $L$-function

The $L$-function is known to satisfy a few great properties. One is the functional equation: if we let $a$ denote $[\chi(-1) = 1]$, and $\tau(\chi)$ denote the “Gauss sum” 









##  



#### Ok let's try

Consider the polynomial $f(n) = n^2 + 21n + 1$ (I'll treat this one first, as $n^2 + n + 1$ is simpler). For how many values of $n \le N$ is $f(n)$ prime?

Recall the [prime number theorem](https://en.wikipedia.org/wiki/Prime_number_theorem): the number of primes less than $N$ is about $N / \log N$, or (a better approximation) about $\int\limits_2^{N} (1/\log t)\, dt$, or for that matter $\sum\limits_{m=2}^{N} 1/\log m$. Based on the prime number theorem, one heuristic model of the prime numbers is that every number $m$ is “prime” with probability $1 / {\log m}$.

This heuristic would say that $f(n) = n^2 + 21n + 1$ is prime with probability $\displaystyle \frac{1}{\log(n^2 + 21n + 1)} \sim \frac{1}{2 \log n}$, so for $n \le N$, the expected number of primes is $~ \sum_{n=2}^{N} 1/(2 \log n) \sim N/(2 \log N)$. This of course 





> _I don’t know whether the constraints for higher primes can eventually switch the balance back in favour of n^2+n+1, but seems unlikely and I can’t prove it either way._

More precisely, we can say exactly how many such constraints there will be for (which) large primes.

Consider f(n) = n^2 + 21n + 1. For a given prime p, if it has any such constraint, i.e. if there is any solution to f(n) = 0 mod p, then (basically by “completing the square”) we have 0 = 4f(n) = (2n + 1)^2 - 437, i.e. the number of solutions to f(n) = 0 mod p is the number of solutions to x^2 = 437 mod p. And using quadratic reciprocity etc., we can prove that the number of solutions to x^2 = 437 mod p is:

- 1 if p = 19 or p = 23
- 2 if p mod 437 lies in a certain set of 198=9×11×2 numbers mod 437 (p should either be a residue mod both 19 and 23, which gives 99 values, or nonresidue mod both, which gives another 99)
- 0 otherwise (if p lies in the set of other 198 possible remainders for primes mod 437)

(This means that for half the primes p ≠ 19, 23, we have 2/p possible values of n “knocked out” by such constraints, while for the other primes p we have no values knocked out.)

Similarly, for g(n) = n^2 + n + 1, the number of solutions to g(n) = 0 mod p is:

- 1 if p = 3
- 2 if p = 1 mod 3
- 0 otherwise

(This means that for half the primes p ≠ 3 we have 2/p possible values of n “knocked out” by such constraints, while for the other primes p we have no values knocked out.)

And using this, we can estimate the number of primes in either polynomial. The final answer (heuristically / based on conjectures) turns out to be:

- The number of primes of the form n^2 + n + 1, for n <= N, is about 1.25 N/log N
- The number of primes of the form n^2 + 21n + 1, for n <= N, is about 2.79 N / log N
- So the ratio is about 2.23

For more, see:

- https://en.wikipedia.org/w/index.php?title=Ulam_spiral&oldid=821475153#Hardy_and_Littlewood's_Conjecture_F
- https://en.wikipedia.org/w/index.php?title=Bunyakovsky_conjecture&oldid=830234069
- https://en.wikipedia.org/w/index.php?title=Bateman%E2%80%93Horn_conjecture&oldid=828694748







------

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

- a fraction $\epsilon(2)/2$ of the numbers are divisible by $2$,
- a fraction $\epsilon(3)/3$ of the numbers are divisible by $3$,
- a fraction $\epsilon(5)/5$ of the numbers are divisible by $5$,

etc.

So the fraction of numbers “near” $m$ that are not divisible by any of the primes $2, 3, 5, \dots, P$, where $P = p_{\pi(\sqrt{m})}$, is:

$$(1 - \frac{\epsilon(2)}{2}) (1 - \frac{\epsilon(3)}{3}) (1 - \frac{\epsilon(5)}{5}) \cdots (1 - \frac{\epsilon(P)}{P})$$

— this is roughly the “probability” that $m$ is prime.

## Number of solutions: $n^2 + n + 1$

If $n^2 + n + 1 \equiv 0 \pmod p$, then, assuming $p \neq 2$, we have $$4n^2 + 4n + 4 = (2n + 1)^2 + 3 \equiv 0 \pmod p,$$ or in other words $(2n + 1)^2 \equiv -3 \pmod p$. For any solution to $x^2 \equiv -3 \pmod p$, we can solve $2n + 1 \equiv x$ to get $n = 2^{-1}(x - 1)$ (and these solutions are distinct). So the number of solutions to $n^2 + n + 1 \equiv 0 \pmod p$ is the number of solutions to $x^2 \equiv -3 \pmod p$. 

If $p = 3$, then this means $x = 0$. For other $p$, we have (see [here](https://en.wikipedia.org/w/index.php?title=Legendre_symbol&oldid=805985930#Properties_of_the_Legendre_symbol)):

$$\left(\frac{-3}{p}\right) = \left(\frac{-1}{p}\right)\left(\frac{3}{p}\right) = (-1)^{[p \not\equiv 1 \pmod 6]} $$

In other words, the number of solutions to $n^2 + n + 1 \equiv 0 \pmod p$ is:

- $0$, if $p = 2$,
- $1$, if $p = 3$,
- $2$, if $p \equiv 1 \pmod 3$,
- $0$ otherwise, i.e. if $p \equiv 2 \pmod 3$

So the fraction of numbers of the form $n^2 + n + 1$ not divisible by any of the primes $2, 3, 5, 7, 11, 13, \dots$ is 

$$\def\({\big(} \def\){\big)} \(1\)_2 \(\frac23\)_3 \(1\)_5 \(\frac57\)_7 \(1\)_{11} \(\frac{11}{13}\)_{13}$$

## Number of solutions: $n^2 + 21n + 1$

For the other polynomial, if $n^2 + 21n + 1 \equiv 0$, then again assuming $p \neq 2$, we have $0 \equiv 4n^2 + (4\cdot21)n + 4 = (2n + 21)^2 - 437$, and for any solution to $x^2 \equiv 437$ we can solve for $n$.

As $437 = 19 \times 23$, we have (for $p \neq 19, 23$), 

$$\left(\frac{437}{p}\right) = \left(\frac{19}{p}\right)\left(\frac{23}{p}\right) = (-1)^{(p-1)/2}\left(\frac{p}{19}\right)(-1)^{(p-1)/2}\left(\frac{p}{23}\right)$$

that is, $437$ is a quadratic residue mod $p$ if and only if either $p$ is a quadratic residue modulo both $19$ and $23$, or modulo neither. This means that either

- $p$ is one of $9$ certain values mod $19$, and one of $11$ certain values mod $23$, so one of $99$ certain values mod $437$, or
- $p$ is one of $9$ certain values mod $19$, and one of $11$ certain values mod $23$, so one of $99$ certain values mod $437$.

That is, $p$ is one of $99 + 99 = 198$ values mod $437$.

When $p = 19$, we have $2n + 21\equiv 0$ or $n \equiv -1$.

When $p = 23$, we have $2n + 21 \equiv 0$ or $n \equiv 1$.

## Putting them together

Now we have a concrete way to count the number of values of $n$ modulo $p$ that are “knocked out” from $f(n)$ being prime, for each prime $p$ and for both functions $f$.

