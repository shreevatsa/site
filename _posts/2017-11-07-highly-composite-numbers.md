---
layout: post
title:  "Computing Highly Composite Numbers"
date:   2017-11-07 16:14:22 -0800
categories: mathematics programming done
tags: [done, maths, continue]
---

Context: Motivated by [this question](https://mathoverflow.net/questions/284577/computational-complexity-of-finding-the-smallest-number-with-n-factors).

----

For a number $n$ with factorization $n = p_1^{e_1} \cdots p_k^{e_k}$, its number of divisors is $d(n) = (e_1 + 1) \cdots (e_k + 1)$. Ramanujan [defined and](http://ramanujan.sirinudi.org/Volumes/published/ram15.pdf) studied [highly composite numbers](https://en.wikipedia.org/wiki/Highly_composite_number), which are numbers that have more divisors than any smaller number, i.e., numbers $n$ for which $d(n) > d(m)$ for all $1 \le m < n$. Let us use the notation $H_k$ to denote the $k$th highly composite number. (I know this notation $H_k$ is generally used for the harmonic numbers, but we will have no occasion for dealing with harmonic numbers here.)

Let us define $F(n)$ as the smallest number with at least $n$ divisors, i.e., the smallest number $m$ such that $d(m) \ge n$. (The question asked on Math Overflow excludes, among the factors of a number, $1$ and the number itself, so it asks for computing $f(n)$ defined as the smallest number $m$ for which $d(m) - 2 \ge n$. This just means $f(n) = F(n + 2)$, so we will use $F(n)$ as it's easier to work with the standard definition.)

Then, for any number $m < F(n)$, we can see that its number of divisors $d(m)$ satisfies $d(m) < n \le d(F(n))$ (both inequalities follow from the definition of $F(n)$), so every value $F(n)$ is a highly composite number. This suggests the following algorithm for computing $F(n)$:

* Compute the highly composite numbers $H_1, H_2, \dots$
* Stop when you reach one with at least $n$ divisors, that is, when you reach $m$ for which $d(H_m) \ge n > d(H_{m-1})$.

So we will be done if we have three things:

* An algorithm for computing the highly composite numbers $H_1, H_2, \dots, H_m$,
* An analysis of the running time of this algorithm (the time needed to compute the first $m$ highly composite numbers),
* An analysis of how large $m$ will be when reach $d(H_m) \ge n$.

I was going to carry this out and write it up here, but in the meantime a good answer to the original question has been posted (even if it doesn't quite achieve polynomial time, which I believe should be possible, nor is it accompanied by an efficient program), so I'll abandon this for now and take it up some other day. :-) Meanwhile, here are the references I was going to use:

References:

* [OEIS A002182](https://oeis.org/A002182), Highly composite numbers
* Wikipedia, [Highly composite number](https://en.wikipedia.org/wiki/Highly_composite_number) (see [permanent link](https://en.wikipedia.org/w/index.php?title=Highly_composite_number&oldid=805548219) to version I saw)
* Ramanujan, [Highly Composite Numbers](http://ramanujan.sirinudi.org/Volumes/published/ram15.pdf), 1915. The most important one, read and assimilate up to section 31 and maybe more.
* [_Highly Composite Numbers by Srinivasa Ramanujan_](http://math.univ-lyon1.fr/~nicolas/ramanujanNR.pdf) (1995/1996, JEAN-LOUIS NICOLAS and GUY ROBIN) (Continuation of Ramanujan's paper)
* Donald B. Siano, [Highly Composite Numbers: How can we calculate them?](https://web.archive.org/web/20021212080514/http://www.eclipse.net:80/~dimona/juliannum.html), and
* Siano, [An Algorithm for Generating Highly Composite Numbers](http://wwwhomes.uni-bielefeld.de/achim/julianmanuscript3.pdf) (Note: Good at elementary exposition, but Achim Flammenkamp says it has some mistakes)
* Achim Flammenkamp, [Highly Composite Numbers](http://wwwhomes.uni-bielefeld.de/achim/highly.html) The best. See especially:
  * [table of first 1200 HCNs](http://wwwhomes.uni-bielefeld.de/achim/highly.txt)
  * [C program](http://wwwhomes.uni-bielefeld.de/achim/composite.txt)
  * [C program for SHCN](http://wwwhomes.uni-bielefeld.de/achim/shcn.txt)
  * [List of first 124260 HCNs ("proved")](http://wwwhomes.uni-bielefeld.de/achim/HCNs.gz)
  * [List of first 779674 HCNs ("proven")](http://wwwhomes.uni-bielefeld.de/achim/HCN.bz2) (not clear what the distinction being made between "proved" and "proven" is)
  * [Asymptotics of Highly Composite Numbers](http://wwwhomes.uni-bielefeld.de/achim/hcn.dvi)
* Kedlaya, [An Algorithm for Computing Highly Composite Numbers]({{ "/assets/hcn/hcn-algorithm.pdf" | absolute_url }}) (generated from `.tex` file, from [here](http://web.archive.org/web/19980707133810/www.math.princeton.edu/~kkedlaya/math/hcn-algorithm.tex))
* G. Robin (1983), [Méthodes d'optimisation pour un problème de théorie des nombres](http://www.numdam.org/article/ITA_1983__17_3_239_0.pdf) (Note: Paper is in French, but [this other paper](http://www.numdam.org/article/JTNB_2008__20_3_625_0.pdf) cites this paper and says the method is similar)
* Erdős, [_On Highly Composite Numbers_](https://www.renyi.hu/~p_erdos/1944-04.pdf) (Shows the HCNs are close together, so there are a lot of HCNs)
* [Growth rate of number of divisors of highly composite numbers](https://mathoverflow.net/questions/296937/growth-rate-of-number-of-divisors-of-highly-composite-numbers) (posted recently...)

----

Edit [2019-04-17]: Another attempt to start writing this up.
$$
\def\tell#1{\quad\text{#1}\quad}
$$
For any vector of nonnegative integers
$$
v = (e_1, e_2, \dots, e_j, \dots)
$$
in which at most finitely many components are nonzero, we can define two quantities (think: number of divisors, and size)
$$
D(v) = (e_1 + 1)(e_2 + 1)\cdots(e_j+1)\cdots
$$
and
$$
S(v) = 2^{e_1}3^{e_2}\cdots p_j^{e_j} \cdots
$$
where $p_j$ is the $j$th prime. The fundamental theorem of arithmetic is that there is a 1-to-1 correspondence $v \leftrightarrow S(v)$.)

The problem asks to find, among all vectors $v$ with $D(v) \ge n + 2$, the one with the smallest $S(v)$. Ramanujan introduced, under the name of “highly composite numbers”, the set of all $v$ that can be answers to the question for some $n$. That is, these are $v$ such that decreasing $S$ in any way also decreases $D$, i.e. any $v'$ such that $S(v') < S(v)$ also has $D(v') < D(v)$. He proved many properties of such $v$, of which we'll use only a few.

If $p_i^{a_i} < p_j^{a_j}$, then bumping up the $i$th coordinate of $v$ by $a_i$ and bumping down the $j$th coordinate by $a_j$ (if that's possible) will cause $S(v)$ to decrease, so $D(v)$ must decrease too: we must have
$$
e_j < a_j \quad\text{or}\quad (e_i + 1)(e_j + 1) > (e_i + a_i + 1)(e_j - a_j + 1)
$$
which simplifies to
$$
e_j < a_j \quad\text{or}\quad a_j(e_i + a_i + 1) > a_i(e_j + 1)
$$
or as we're working with integers where $m > n$ means $m \ge n + 1$, we can write
$$
e_j < a_j \quad\text{or}\quad a_j(e_i + a_i + 1) \ge a_i(e_j + 1) + 1
$$
Although this particular way of decreasing $S(v)$ is itself a special case, two special cases are convenient:

* $a_j = 1$: then the result is that if $p_i^{a_i} < p_j$ and $e_j > 0$, then
  $$
  e_i \ge a_i e_j
  $$
  i.e.
  $$
  e_i \ge \lfloor \log p_j / \log p_i \rfloor e_j
  $$

* $a_i = 1$: then the result is that if $p_i < p_j^{a_j}$ then
  $$
  e_j < a_j \quad\text{or}\quad a_j(e_i + 2) \ge e_j + 2
  $$
  i.e. (noticing that the former anyway implies the other, and swapping $i$ and $j$ as they're just labels)
  $$
  e_i \le \lceil \log p_j / \log p_i \rceil (e_j + 2) - 2 = \lfloor \log p_j / \log p_i \rfloor (e_j + 2) + e_j
  $$
  where both are the same.

* $a_i = 1$ and $a_j = 1$: then the result is that if $p_i < p_j$ then $e_i \ge e_j$, i.e. the exponents form a nonincreasing sequence.

Together these give bounds for $e_i$ in terms of $e_j$ (or the other way around).

Let's say the length is $K$, i.e. $e_K > 0$ and $e_{K+1} = 0$. Then further specializing $j$ above to $K$ or to $K+1$, we get
$$
\lfloor \log p_K / \log p_i \rfloor \le e_i \le 2\lfloor \log p_{K+1} / \log p_i \rfloor
$$
using the fact that $e_K = 1$ (except for the two small exceptions when $e_K = 2$) and $e_{K+1} = 0$.

What are the possible options for the first and last places where the exponent $e_j$ takes on a particular value $c$ (if at all it does)? If $e_i = c$ then by the above we must have
$$
\lfloor \log p_K / \log p_i \rfloor \le c \le 2\lfloor \log p_{K+1} / \log p_i \rfloor
$$
which means that firstly
$$
\log p_K / \log p_i < c + 1 \tell{so} \log p_i > \log p_K / (c+1)
$$
so $p_i > p_K^{1/(c+1)} = \sqrt[c+1]{p_K}$ and secondly
$$
c / 2 < \log p_{K+1} / \log p_i \tell{so} \log p_i < (2/c) \log p_{K+1}
$$
or $p_i < p_{K+1}^{2/c}$.

-----

From earlier...

Our strategy will be to prove/use more and more properties (proved by Ramanujan) about such an optimal $v$, thus further constraining the space of $v$’s we need to search, until we're left with having to search only a manageable number of all $v$.

Next, for the vector satisfying $D(v) \ge n$ and having the smallest $S(v)$, we must have
$$
e_j = 0 \text{ for }j > K = \lceil \log_2 n \rceil \tag 2
$$
 because for the vector $(1, 1, \dots, 1, 0, \dots)$ where $K$ is the number of $1$s, we already have $d(v) = 2^K \ge n$. And any other vector $v$ with even more nonzero components has strictly greater $S(v)$ than this one.

(This by itself, along with the obvious  $e_j < n$, already reduces the search space to less than $nK \sim n\log_2 n$, further reduced using $(1)$, but as that's exponential in the input size $\log n$, we won't dwell on it further.)

which leads to the analysis carried out by Lucia above.

$e_{K - 2} \le 4$ if $p_K \ge 5$.

If $p_K \ge 5$ then $(1 + 1/e_K)(1 + 1/e_{K-1}) > 12/5$ so $e_K = 1$.

So $e_K = 1$ always except for $v = (2, 0, \dots)$ and $v = (2, 2, 0, \dots)$.

----

OK, I'm abandoning this here. Let me summarize what I understand so far.

There is the paper by Ramanujan, available online in the usual places and public-domain in any case; though note that one of them is a re-typeset copy with some typos. In an [earlier paper](http://ramanujan.sirinudi.org/Volumes/published/ram08.html), he had investigated what the largest possible value of $d(N)$ is, as a function of $N$ (the main results are equations $9$ and $(20)$ which is the last one in that paper). In [this](http://ramanujan.sirinudi.org/Volumes/published/ram15.html) (his 15th) paper, somewhat motivated by the same question, he studies the set of “record values” of $d(N)$, those where it's greater than any earlier value, and calls the set of such $N$ as “highly composite numbers”.

He proves a few facts about such numbers, or more precisely their exponent vectors. The ones he calls out in the introduction to the paper are:

* The components $e_i$ of the vector form a non-increasing sequence,

* For large $N$, they have a “strictly decreasing part” at the beginning, and an “all values covered” part at the end. An example: after about 779674 HCNs (according to Achim Flammenkamp's site/data), we have the exponent vector of length 4094 or 4095 that look like:

  ```
  (length 4094)     21 13 8 7 5^2 4^3 3^13 2^72 1^4000 
  (length 4095)     22 13 9 7 6 5 4^4 3^12 2^69 1^4004 
  (length 4094)     21 14 8 7 5^2 4^4 3^11 2^73 1^4000
  ```

  where there's a strictly decreasing part like $21 > 13 > 8 > 7 > 5$, and an “all values covered part” (like everything in $1$ to $5$ above).

  Not sure if Ramanujan's results imply they overlap.

* The exponent $e_i$ associated with the $i$th prime $p_i$ satisfies, for small $i$, the relation $e_i \log p_i \sim \log p_K / \log 2$ where $K$ is the length of the exponent vector, while for large $i$ we can write it down precisely with an error of at most $\pm 1$.

* Then he moves on to “superior highly composite numbers” which along with the Riemann hypothesis helps him with his initial question, but we don't have to go there unless we want to.

From his initial section, see his equations 3, 10, 15, then 28. After that, consider 