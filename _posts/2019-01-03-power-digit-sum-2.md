---
layout: post
title: More on the sum of digits of a power of a number
excerpt: Followup to -- How often does a number $N$ have some power $N^k$ whose sum of digits is exactly $N$?
date: 2019-01-03
tags: [done]

---

In [the previous post](power-digit-sum) we tried to find how frequently a number $n$ (switching notation to lowercase now) has some power $k$ such that the sum of digits of $n^k$, which we denoted $S(n^k)$, is exactly $n$. We had a heuristic argument for why the number of such $n$ below a certain limit $x$ should be on the order of $x/\log x$, or in fancier terms, $\def\Li{\operatorname{Li}}$ $\Li(x)$.

Let's explore further. 

## Program

First, to count this for larger $n$, we need a faster program, so I switched from Python to C++, using [GMP](https://en.wikipedia.org/w/index.php?title=GNU_Multiple_Precision_Arithmetic_Library&oldid=871792237) to make up for losing Python's built-in large integer support. In hindsight I'm unsure if this was really necessary; most of the speedup probably comes from trying fewer $k$. Specifically, if at all $S(n^k) = n$ for some $k$, then it probably happens for $k$ around $n / (4.5 \log n)$ (see function `best_k` in the code below), so we only try a few $k$ in the neighbourhood of that value. (We grow this neighbourhood to cover twice the maximum deviation from `best_k` seen so far; in principle this may leave out a few $n$ but in practice the results seem to match and even if a few $n$ were “lost”, they are probably not enough to affect the results.)

```c++
#include <iostream>
#include <cmath>
#include <gmpxx.h>

const int MAXN = 10000000;
const int MAX_LEN = MAXN; // Something like MAXN / (4.5 log MAXN) will do
char str[MAX_LEN + 2]; // To hold the string representation of n^k
int lowest_k = 0, highest_k = 0;

int best_k(int n) {
  // If n = 10m, then S(n^k) = S(m^k)
  int m = n;
  while (m % 10 == 0) m /= 10;
  // S(m^k) which is roughly k * 4.5 * log10(m) should be n,
  // so k should be roughly n / (4.5 * log10(m))
  return n / (4.5 * std::log10(m));
}

int main() {
  std::ios::sync_with_stdio(false);
  for (int n = 2; n < MAX_LEN; ++n) {
    bool good = false;
    int K = best_k(n);
    int which_k;
    // TODO: Replace with an interval based on estimated variance 
    // (higher if n is a multiple of 10) etc.
    for (int k = std::max(0, K + 2*lowest_k - 5); k <= K + 2*highest_k + 5; ++k) {
      which_k = k - K;
      mpz_class nk;  // Declare "nk" to hold n^k
      mpz_ui_pow_ui(nk.get_mpz_t(), n, k);  // Set nk to n^k
      mpz_get_str(str, 10, nk.get_mpz_t()); // Put digits into str
      int sum = 0;
      for (int i = 0; str[i] != '\0'; ++i) {
        sum += str[i] - '0';
      }
      if (sum >= n) {
        lowest_k = std::min(lowest_k, which_k);
      }
      if (sum <= n) {
        highest_k = std::max(highest_k, which_k);
      }
      if (sum == n) {
        good = true;
        break;
      }
    }
    if (good) {
      std::cout << n << " " << which_k << " " << lowest_k << " " << highest_k << std::endl;
    }
  }
}
```

(a slightly cleaned-up version of the [actual]({{ "/assets/powers/find.cc" | absolute_url }}) program I used). Compile and run with something like:

```sh
clang++ -std=c++17 -lgmp -lgmpxx -O2 find.cc -o find
```

This one more quickly gets to the tens of thousands, so we have more numbers to examine growth.

## Comparison

Secondly, one can look for this sequence on OEIS: searching for “17, 18, 20, 22, 25, 26, 27, 28” gives [A124359 Numbers n for which the sum of the digits of n^k, for some k, is equal to n](http://oeis.org/A124359) (added in 2006, extended in 2018), and [A247889](http://oeis.org/A247889) for the (smallest) $k$s. There's nothing stated about the growth of the sequence, so we seem to be in new territory (or at least unknown to the OEIS), but we can use their list of the first 3600 values (up to 20034) to verify that our program hasn't missed anything (it hasn't, except for $n=0$ and $n=1$).

## Argument

Finally, some details were wrong in the previous post, so let's restate the argument and try to get the details right.

### The value of $S(n^k)$ modulo $9$

As before, let $S(m)$ denote the sum of the digits of a number $m$. As $10 \equiv 1 \pmod 9$, we know that $ S(m) \equiv m \pmod 9$ for all $m$. Further, we can say something about $S(n^k)$ depending on $n \bmod 9$, namely:

- If $n \equiv 0 \pmod 9$, then $S(n^k) \equiv n^k \equiv 0^k \equiv 0 \pmod 9$
- If $n \equiv 1 \pmod 9$, then $S(n^k) \equiv n^k \equiv 1^k \equiv 1 \pmod 9$
- If $n \equiv 2 \pmod 9$, then $S(n^k) \equiv 2^k \pmod 9$, and this cycles every six $k$, i.e. is $\equiv 1, 2, 4, 8, 7, 5 \pmod 9$ for $k \equiv 0, 1, 2, 3, 4, 5 \pmod 6$ respectively
- If $n \equiv 3 \pmod 9$, then $S(n^k) \equiv 3^k \pmod 9$, and this is $\equiv 0$ for $k \ge 2$.
- If $n \equiv 4 \pmod 9$, then $S(n^k) \equiv 4^k \pmod 9$ and this cycles every three $k$, i.e. is $\equiv 1, 4, 7 \pmod 9$ for $k \equiv 0, 1, 2 \pmod 3$ respectively.
- If $n \equiv 5 \pmod 9$, then $S(n^k) \equiv 5^k \pmod 9$ and this cycles every six $k$, i.e. is $\equiv 1, 5, 7, 8, 4, 2 \pmod 9$ for  $k \equiv 0, 1, 2, 3, 4, 5 \pmod 6$ respectively
- If $n \equiv 6 \pmod 9$, then $S(n^k) \equiv 6^k \pmod 9$ and this is $\equiv 0$ for $k \ge 2$.
- If $n \equiv 7 \pmod 9$, then $S(n^k) \equiv 7^k \pmod 9$ and this cycles every three $k$, i.e. is $\equiv 1, 7, 4 \pmod 9$ for $k \equiv 0, 1, 2 \pmod 3$ respectively.
- If $n \equiv 8 \pmod 9$, then $S(n^k) \equiv 8^k \mod 9$, and this cycles every other $k$, i.e. is $\equiv 1, 8\pmod 9$ for $k \equiv 0, 1 \pmod 2$ respectively.

### Peeling off powers of $10$

If $n = 10^c m$ for some $c$, then as $n^k = 10^{ck} m^k$, the digits of $n^k$ are the digits of $m^k$ followed by $ck$ zeroes. From now on, let's talk primarily of the digits in $m^k$, where $m$ is $n$ with all powers of $10$ removed. This does not affect anything from the previous section, as $n \equiv m \pmod 9$ and $n^k \equiv m^k \pmod 9$.

### The number of digits in $m^k$

For a fixed $m$, let $d_k = \lfloor 1 + k \log_{10} m\rfloor$. Then $m^k$ has $d_k$ digits.

Why? Because by definition of $\lfloor \cdot \rfloor$, and writing $\log$ for the base-$10$ logarithm,

$d_k \le 1 + k \log m < d_k + 1$

$d_k - 1 \le k \log m < d_k$

$10^{d_k - 1} \le m^k < 10^{d_k}$

and this is precisely what it means for $m_k$ to have $d_k$ digits.

By the way, with $n = 10^c m$, the number of digits in $n^k$ is $ck + d_k$.

### The random model

Finally we come to the heart of the heuristic argument. The hope is to come up with a random model about which we can make precise and rigorous remarks, but then (non-rigorously) appeal to the reader's judgment of whether these random numbers constitute a good model for the actual (non-random) numbers $n^k$ or $m^k$.

We'll in fact work with a few different random models, that may match reality to different exists.

#### $n^k$ as a random string of digits

Simplest is to model $n^k$ by a random string of digits of length $d_k$.

Fix a length $d$, and let $X_1, X_2, \dots, X_d$ be independent random variables each uniformly distributed on the set $\{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$ — that is, each $X_i$ is a random digit. Let $S = X_1 + X_2 + \dots + X_d$. Then what is the distribution of $S$?

The probability that $S$ takes a certain value $s$ is 

$$\Pr(S = s) = [z^s](1 + z + z^2 + \dots + z^9)^d/10^d$$

where “$[z^s]$” denotes “coefficent of $z^s$”.

This lets us calculate the probability for a fixed $k$: see [this question](https://math.stackexchange.com/questions/3063646/what-is-the-probability-that-the-sum-of-digits-of-a-random-k-digit-number-is) which confirms it.

Unfortunately, I'm not sure how to sum this over $k$, even though it ought to be summable.

The ordinary (probability-) generating function 

$$\displaystyle \mathbb{E}(z^S) = \sum_{s}\Pr(S=s)z^s = \big(\sum_{x}\Pr(X=x)z^x\big)^d = \mathbb{E}(z^X)^d$$

The moment-generating function

$$\displaystyle\mathbb{E}(e^{tS}) = \sum_{s}\Pr(S=s)e^{ts} = \mathbb{E}(e^{tX})^d = \big(\sum_{x}\Pr(X=x)e^{tx}\big)^d = \big(\sum_{x=0}^9\frac{e^{tx}}{10}\big)^d = \frac{(1 - e^{10t})^d}{10^d(1-e^t)^d}$$

The characteristic function

$$\displaystyle\phi_S(t) = \mathbb{E}(e^{itS}) = \sum_{s}\Pr(S=s)e^{its} = \big(\sum_{x}\Pr(X=x)e^{itx}\big)^d = \mathbb{E}(e^{itX})^d$$

#### $m^k$ as a random sum of digits

Similar to the previous model, with complications when $n$ being a multiple of $10$. Are multiples of $10$ frequent enough to matter? Note that we need a multiple of $10^c$ for $c$ of the digits to be non-random, and those are going to be rare. (Tautology: in all but $1 - 10^{-20}$ of cases, $c < 20$ so only at most $20$ digits are poorly modelled by the random distribution.)

#### n^k as a random string of digits subject to mod-$9$ constraints

This gets interesting. Given $n$, for any $k$, model $n^k$ by taking random strings of digits of the right length, and throwing away those that are not equal to one of the allowed values $\bmod 9$ for $n^k$ (ignore the dependence on $k$ itself). This seems to fit the data.

## The literature

I found a few papers by starting at this one: https://arxiv.org/pdf/1212.6697.pdf

Let's summarize the main ones, in chronological order.

Let $\alpha(x) = \text{sum of digits of $x$}$ and $A(y) = \text{sum of digits of all numbers up to $y$}$.

* 1940, L. E. Bush (10.2307/2304217): shows that ...
* 1977, K. B. Stolarsky (10.1137/0132060): shows that...
* 1998, [Drmota & Gajdosik](http://www.numdam.org/article/JTNB_1998__10_1_17_0.pdf): shows that...
* 1997, Dumont & Thomas (10.1006/jnth.1997.2044): ...
* 1977, [Diaconis](https://projecteuclid.org/download/pdf_1/euclid.aop/1176995891): ...
* 2013, G. Tennebaum (10.1007/978-1-4614-7258-2_19): (in French)....
* 2001, [Fang](http://www.ams.org/journals/proc/2002-130-06/S0002-9939-01-06303-1/S0002-9939-01-06303-1.pdf): ...
* 1986, [Cooper & Kennedy](http://www.kurims.kyoto-u.ac.jp/EMIS/journals/IJMMS/Volume9_4/846161.pdf): ...
* 1989, [Kennedy & Cooper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.388.1103&rep=rep1&type=pdf): ...
* 2014, Chen & Hwang [survey](https://arxiv.org/pdf/1212.6697.pdf): ...
* 1955, Cheo & Yien ([Chinese](http://en.cnki.com.cn/Article_en/CJFDTotal-SXXB195504001.htm)): ...
* 2010, Chen  (10.1007/s10114-010-8416-9): ...
* 



If we pick a random number from $1$ to $n^k$ and consider the sum of its digits,

mean is $\mathbb{E}(X_n) = \frac{10-1}{2}\log_{10}(n^k) + O(1)$ and

variance is $\mathbb{V}(X_n) = \sim \frac{10^2 - 1}{12} \log_{10}(n^k)$ per the notation of this paper:

https://arxiv.org/pdf/1212.6697.pdf#page=10

The paper also gives:

$$\mathbb{P}(X_n = m) \sim \frac{1}{n} \cdot \frac{(\log_{10} n)^m}{m!}$$

https://arxiv.org/pdf/1212.6697.pdf#page=8 and this is exactly what we care about. (Cites [this paper](http://en.cnki.com.cn/Article_en/CJFDTotal-SXXB195504001.htm).)







----
