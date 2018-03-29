---
layout: post
title:  "Highly Composite Numbers"
date:   2017-11-07 19:02:24 -0800
categories: jekyll
---

Context: Motivated by [this question](https://mathoverflow.net/questions/284577/computational-complexity-of-finding-the-smallest-number-with-n-factors).

<hr/>

For a number $n$ with factorization $n = p_1^{e_1} \cdots p_k^{e_k}$, its number of divisors is $d(n) = (e_1 + 1) \cdots (e_k + 1)$. [Ramanujan](http://ramanujan.sirinudi.org/Volumes/published/ram15.pdf) defined and studied [highly composite numbers](https://en.wikipedia.org/wiki/Highly_composite_number), which are numbers that have more divisors than any smaller number, i.e., numbers $n$ for which $d(n) > d(m)$ for all $1 \le m < n$. Let us use the notation $H_k$ to denote the $k$th highly composite number. (I know this notation is generally used for the harmonic numbers, but we will have no occasion for dealing with harmonic numbers here.)

Let us define $F(n)$ as the smallest number with at least $n$ divisors, i.e., the smallest number $m$ such that $d(m) \ge n$. (The question excludes, among the factors of a number, $1$ and the number itself, so it asks for computing $f(n)$ defined as the smallest number $m$ for which $d(m) - 2 \ge n$. This just means $f(n) = F(n + 2)$, so we will use $F(n)$ as it's easier to work with the standard definition.)

Then, for any number $m < F(n)$, by the definition of $F(n)$ we can see that its number of divisors is $d(m) < n \le d(F(n))$, so every value $F(n)$ is a highly composite number. This suggests the following algorithm for computing $F(n)$:

* Compute the highly composite numbers $H_1, H_2, \dots$
* Stop when you reach one with at least $n$ divisors, that is, when you reach $m$ for which $d(H_m) \ge n > d(H_{m-1})$.

So we will be done if we have three things:

* An algorithm for computing the highly composite numbers $H_1, H_2, \dots, H_m$,
* An analysis of the running time of this algorithm (the time needed to compute the first $m$ highly composite numbers),
* An analysis of how large $m$ will be when reach $d(H_m) \ge n$.

<hr/>

References:

* [OEIS A002182](https://oeis.org/A002182), Highly composite numbers
* Wikipedia, [Highly composite number](https://en.wikipedia.org/wiki/Highly_composite_number) (see [permanent link](https://en.wikipedia.org/w/index.php?title=Highly_composite_number&oldid=805548219) to version I saw)
* Ramanujan, [Highly Composite Numbers](http://ramanujan.sirinudi.org/Volumes/published/ram15.pdf), 1915. The most important one, read and assimilate up to section 31 and maybe more)
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
* Kedlaya, [An Algorithm for Computing Highly Composite Numbers]({{ "/assets/hcn/hcn-algorithm.pdf" | absolute_url }}) (see also `.tex` file in same folder)
* G. Robin (1983), [Méthodes d'optimisation pour un problème de théorie des nombres](http://www.numdam.org/article/ITA_1983__17_3_239_0.pdf) (Note: Paper is in French, but [this other paper](http://www.numdam.org/article/JTNB_2008__20_3_625_0.pdf) cites this paper and says the method is similar)
* Erdős, [_On Highly Composite Numbers_](https://www.renyi.hu/~p_erdos/1944-04.pdf) (Shows the HCNs are close together, so there are a lot of HCNs)
