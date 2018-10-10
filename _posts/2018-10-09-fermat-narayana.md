---
layout: post
title: Factorizing numbers using Fermat's method (Narayana's method)
excerpt: 
date: 2018-10-09
tags: [done, maths]

---

Fermat's method of factorization (which should properly be called Narayana's method; see below) is useful when trying to find the factors of a number $N$ that happens to have a factorization of the form $N = pq$, where $p$ and $q$ are very close to each other.

The idea is this: suppose we are given an odd number $N$ (for even numbers it's easy to find at least one factor, namely 2!) such that $N = pq$ (where $p$ and $q$ are unknown, but obviously both must be odd). Then if we let $a = (p + q)/2$ and $b = (q - p)/2$, then $p = a - b$ and $q = a + b$, and therefore $N = pq = (a - b)(a + b) = a^2 - b^2$. Conversely, if we can write $N$ in the form $N = a^2 - b^2$, then we can find $p$ and $q$ as $a - b$ and $a + b$ respectively.

This is what the method tries to do: write $N$ as

$$Label 'fermat1' multiply defined\begin{equation}N = a^2 - b^2 \tag{1}\label{fermat1}\end{equation}$$

How can we use $\eqref{fermat1}$, short of randomly trying integers $a$ and $b$? One way would be to rewrite $\eqref{fermat1}$ so that $a$ is on the right-hand side:

$$Label 'fermat2' multiply defined\begin{equation}N + b^2 = a^2\tag{2}\label{fermat2}\end{equation}$$

This would suggest trying successive values of $b$ until we find one for which $N + b^2$ is a square. Better is to rewrite $\eqref{fermat1}$ such that $b$ is on the RHS:

$$Label 'fermat3' multiply defined\begin{equation}a^2 - N = b^2\tag{3}\label{fermat3}\end{equation}$$

This suggests the following algorithm: Try successive values of $a$ (such that $a^2 \ge N$) until you find one for which $a^2 - N$ is a square. And this is Fermat's factorization method.

Actually, Pierre de Fermat, after whom it is named, lived from 1607 to 1665. The method occurs much earlier, in the work of Narayana Pandita. In the Sanskrit text *Gaṇita-kaumudī*, written around 1356, Nārāyaṇa describes exactly this method. In the algorithmic style that is typical of Indian mathematics,[^indcomp] the computational details are refined and worked out, and what is presented is a practical algorithm:

[^indcomp]: The algorithmic flavour of Indian mathematics is IMO not sufficiently appreciated. When Indian mathematics was first translated into English and other European languages, it was under-valued (among other reasons) as modern mathematics at the time was under the thrall of the Greek axiomatic method. With the rise of computer science, more attention today, by people with a computational mindset, would lead to better translations and understanding. Knuth has written somewhere about how he was reading a translation of some Sanskrit mathematical text and could relate to the author, even if the author didn't seem to have been understood properly by the translator.

- Square numbers can be (further) factorized using the factorization of their square root.

- So given a non-square number $N$, write it as $N = A^2 + r$, where $A^2$ is the closest square number less than $N$.

- (The idea, as mentioned earlier, is to try values of $a^2 - N$, for successive numbers $a = A + 1$, $a = A + 2$, etc., and check whether they are squares. Note that $(A + 1)^2 - r = A^2 + 2A+1 - r$ and so on. This Nārāyaṇa presents as follows.)

- If it so happens that $2A + 1 - r$ is a square (say $b^2$), then we are done: $N = (A + 1 - b)(A + 1 + b)$.

  > apada-pradasya rāśeḥ padam āsannaṃ dvi-saṅguṇaṃ saikam /
  >
  > mūlāvaśeṣa-hīnaṃ vargaś cet kṣepakaś ca kriti-siddhau //

- (Else, we have to move on, to trying $A + 2$, and so on. Note that $(A + 2)^2 - (A+1)^2 = 2A + 3$, and in general $(A+k)^2 - (A+k-1)^2 = 2k-1$. So we can move to successive squares by adding successive odd numbers. This Nārāyaṇa presents as follows.)

- Else, if $2A + 1 - r$ is not a square, add $(2A + 3)$ and so on, until and keep doing this until you get a square.

  > vargo na bhavet pūrvāsannapadaṃ dvi-guṇitaṃ tri-saṃyuktam /
  >
  > adyād uttara-vṛddhyā tāvad yavad bhaved vargaḥ //

### Example

Here is a worked-out example, using Nārāyaṇa's method. Consider the 309-digit number N = 10000 00000 00000 00738 95091 37611 64544 47082 96833 71185 86600 68128 90654 88870 73921 09201 08053 65341 56624 34024 61288 17909 55097 21638 67047 87165 76291 33813 53272 85613 36109 27478 66891 04494 71945 61369 77224 93690 66504 00823 90307 77919 04596 57524 86653 37281 26322 86420 48452 96156 70829 12176 87090 47243 84458 70151 97251 11825 42414 56911 69344 9233. (This number arises from [this nice post](https://manasataramgini.wordpress.com/2018/10/05/a-laymans-overview-of-the-arithmetic-of-encryption/).)

Normally, factoring such large numbers is beyond the reach of computers: there are [240-digit numbers](https://en.wikipedia.org/w/index.php?title=RSA_numbers&oldid=860651860#RSA-240) that haven't been factored since being offered as a [challenge](https://en.wikipedia.org/w/index.php?title=RSA_Factoring_Challenge&oldid=862587721) in 1991. But in this case, $N$ happens to be the product of two nearby primes, so it turns out we can factor it easily. We write $N$ as $A^2 + r$ where 

A = 10000 00000 00000 00369 47545 68805 82265 40980 91798 29842 68845 19227 78552 15054 36593 47219 59721 65131 09705 40832 74465 11753 68723 26673 14337 00334 95734 04171 04619 24482 75182 (has 155 digits), and 

r = 20000 00000 00000 00738 95091 37611 64530 81961 83596 59685 37690 38455 57104 30108 73186 94439 19443 30262 19410 81665 48930 23507 37446 53346 28674 00669 91468 08342 09238 48963 16109 (also has 155 digits).

Then we calculate $(2A + 1 - r)$. This works out to be just $234256$, which is exactly the square of $484$. The problem is already solved, in just the very first step! What we've found is that with $b = 484$ and $a = A + 1$, we have $N = a^2 - b^2 = (a - b)(a + b)$, so the factors are

$p = (a - b)$ which is 10000 00000 00000 00369 47545 68805 82265 40980 91798 29842 68845 19227 78552 15054 36593 47219 59721 65131 09705 40832 74465 11753 68723 26673 14337 00334 95734 04171 04619 24482 74699 (has 155 digits) and

$q = (a + b)$ which is 10000 00000 00000 00369 47545 68805 82265 40980 91798 29842 68845 19227 78552 15054 36593 47219 59721 65131 09705 40832 74465 11753 68723 26673 14337 00334 95734 04171 04619 24482 75667 (has 155 digits).

Both of these can be verified to be prime, so this is the complete factorization of $N$.

------



----
