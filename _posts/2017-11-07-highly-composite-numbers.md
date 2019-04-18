
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

For any vector of nonnegative integers
$$
v = (e_1, e_2, \dots, e_j, \dots)
$$
in which at most finitely many components are nonzero, we can define two quantities
$$
D(v) = (e_1 + 1)(e_2 + 1)\cdots(e_j+1)\cdots
$$
and
$$
S(v) = 2^{e_1}3^{e_2}\cdots p_j^{e_j} \cdots
$$
(standing for “number of divisors” and “size”) where $p_j$ is the $j$th prime.

(By the fundamental theorem of arithmetic (unique factorization), the vectors $v$ are in 1-to-1 correspondence with the numbers $S(v)$, so specifying $v$ is the same as specifying $S(v)$ and vice-versa.)

Ramanujan introduced and defined as “highly composite numbers” all $S(v)$ for which any vector $v'$ with a smaller $S$, i.e. $S(v') < S(v)$, necessarily has a smaller $D$, i.e. $D(v') < D(v)$. He proved many properties of such numbers $S(v)$, or equivalently, such vectors $v$.

The problem asks to find, among all vectors $v$ with $D(v) \ge n$, the one with the smallest $S(v)$. 

Our strategy will be to prove/use more and more properties (proved by Ramanujan) about such an optimal $v$, thus further constraining the space of $v$’s we need to search, until we're left with having to search only a manageable number of all $v$.

First, we must have
$$
e_1 \ge e_2 \ge \dots \ge e_j \dots \tag 1
$$
because otherwise if some $e_i < e_j$ for $i < j$, then we could swap $p_i$ and $p_j$ to get a smaller $S(v)$ for the same $D(v)$.

Next, for the vector satisfying $D(v) \ge n$ and having the smallest $S(v)$, we must have
$$
e_j = 0 \text{ for }j > K = \lceil \log_2 n \rceil \tag 2
$$
 because for the vector $(1, 1, \dots, 1, 0, \dots)$ where $K$ is the number of $1$s, we already have $d(v) = 2^K \ge n$. And any other vector $v$ with even more nonzero components has strictly greater $S(v)$ than this one.

(This by itself, along with the obvious  $e_j < n$, already reduces the search space to less than $nK \sim n\log_2 n$, further reduced using $(1)$, but as that's exponential in the input size $\log n$, we won't dwell on it further.)

Next, for any indices $j < k$, if $p_j^c < p_k$, then increasing $e_j$ by $c$ and decreasing $e_k$ by $1$ (if possible) causes $S(v)$ to decrease, so $D(v)$ must decrease too: we must have
$$
(e_j + 1)(e_k + 1) > (e_j + c + 1)e_k \quad\text{where}\quad c = \lfloor \log_{p_j}p_k\rfloor
$$
which simplifies to
$$
e_j > ce_k - 1 \quad\text{where}\quad c = \lfloor \log_{p_j} p_k \rfloor \tag3
$$
Similarly, for any indices $j < k$, if $p_j^c > p_k$ then decreasing $e_j$ by $c$ (if possible) and increasing $e_k$ by $1$ causes $S(v)$ to decrease, so $D(v)$ must decrease too: we must have
$$
e_j < c \quad\text{or}\quad (e_j + 1)(e_k + 1) > (e_j - c + 1)(e_k + 2) \quad\text{where}\quad c = \lceil\log_{p_j} p_k\rceil
$$
which simplifies a little to
$$
e_j < ce_k + 2c - 1 \quad\text{where}\quad c = \lceil\log_{p_j} p_k\rceil \tag4
$$
Just this $(4)$ for the particular case when $k = K + 1$ (and so $e_k = 0$) gives $c = \left\lceil \frac{\log p_{K+1}}{\log p_j}\right\rceil$ and $e_j < 2c - 1$, i.e.,
$$
e_j < 2\left\lceil \frac{\log p_{K+1}}{\log p_j}\right\rceil - 1
$$
which leads to the analysis carried out by Lucia above.

Together, one has, for any $j, k$, the following relation:
$$
e_k \lfloor \log_{p_j} p_k \rfloor \le e_j < (1 + e_k)\lceil \log_{p_j} p_k \rceil - 1 \tag5
$$
This is equation xx of Ramanujan.

If $K$ is the last nonzero component, then $e_K \le 2$ (later improved).

$e_{K - 2} \le 4$ if $p_K \ge 5$.

If $p_K \ge 5$ then $(1 + 1/e_K)(1 + 1/e_{K-1}) > 12/5$ so $e_K = 1$.

So $e_K = 1$ always except for $v = (2, 0, \dots)$ and $v = (2, 2, 0, \dots)$.



