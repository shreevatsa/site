---
layout: post
title: Divisibility tests via modular arithmetic
excerpt: Using modular arithmetic, and a new trick (found in "Vedic Mathematics"), to finally get good divisibility tests
date: 2018-11-11
tags: [done]

---

(This starts with a lot of obvious stuff you probably already know; skip to the section titled [A new idea](#a-new-idea) for the interesting bits.)

**Table of contents**
* TOC
{:toc}

## Background: definition of modular equivalence

Consider a nonzero integer $p$. We'll say that two integers $x$ and $y$ are **congruent modulo $p$**

* if they leave the same remainder when divided by $p$, 

  or equivalently,

* if $p$ divides their difference $x - y$.

Let's denote this by $x \equiv_p y$. That is, $x$ may not be **equal** to $y$, but when viewed through a “mod p” lens (thus the $p$ subscript on the $\equiv$), they are **equivalent**.[^fnmodnotation] Each integer is equivalent to infinitely many others, e.g. modulo $7$, we have $10 \equiv_7 3 \equiv_7 17 \equiv_7 -4 \equiv_7 -11 \equiv_7 80 \equiv_7 101 \equiv_7 \dots$ — the difference between any two of those numbers ($10$, $3$, $-11$, etc) is divisible by $7$.

[^fnmodnotation]: In number theory this is usually written as $x \equiv y \pmod p$, or even (when “$\bmod p​$” is implicit from context) simply $x \equiv y​$, but I've found that this notation confuses people unfamiliar with number theory, so trying this new notation… not sure if it will be better or worse.

Looking at numbers in this way (through this “mod p lens”) is called *modular arithmetic*, and many properties of usual arithmetic hold; for example the results when we add or multiply equivalent numbers are equivalent:

* If $a \equiv_p b$ and $x \equiv_p y$, then $a + x \equiv_p b + y$,

* If $a \equiv_p b$ and $x \equiv_p y$, then $ax \equiv_p by$.

(Both are easy exercises to prove.) The same is true of subtraction, and we can divide by some numbers:

* If $cx \equiv_p cy$ **and $\gcd(c, p) = 1$** then $x \equiv_p y$.

The connection with usual arithmetic is that $p$ divides $x$ if and only if $x \equiv_p 0$, and in general $x$ leaves a remainder $r$ when divided by $p$ (say $0 \le r < p$) if and only if $x \equiv_p r$. Note that if $x \equiv_p y$, then the subtraction rule gives $(x - y) \equiv_p 0$, which fits our definition of $\equiv_p$.[^fnpprime]

[^fnpprime]: For most of this post, $p$ can be any integer and need not be prime, despite the notation used here.

## A string of digits

The two simple properties mentioned above (of addition and multiplication) allow us to view a number, given in decimal notation as a string of digits, in a different light. For example, the six-digit number $\mathrm{[fedcba]}$ (the square brackets are to make clear that we mean a number whose digits are $f, e, d, c, b, a$ rather than the product $f$ times $e$ times...) is equal to

$$\mathrm{[fedcba]} = 10^5f + 10^4e + 10^3d + 10^2c + 10b + a$$

and if we replace each of $10, 10^2, 10^3, \dots$ with their mod-p equivalents, the result is equivalent mod $p$. Of course we can also write $\mathrm{[fedcba]} = 10^4\mathrm{[fe]} + \mathrm{[dcba]}$ or $\mathrm{[fedcba]} = 10\mathrm{[fedcb]} + a$, etc.

(I've given an example with six digits for concreteness, but you can generalize it in an obvious way to any number of digits.)

Specifically, this gives us some simple divisibility tests (easy ways to check by hand whether a number is divisible by $p$) for some numbers $p$:

## Divisibility by $2$ or $5$ (or $10$)

Whether $p=2$ or $ p=5$ (or $p = 10$), we have $10 \equiv_p 0$, and the same is true for higher powers of $10.$ In other words, the powers of $10$, namely $1, 10, 10^2, 10^3, 10^4, \dots$ are respectively equivalent to $1, 0, 0, 0, 0, \dots$, so we can replace a number $\mathrm{[fedcba]}$ with

$$\begin{align}\mathrm{[fedcba]} &= 10^5f + 10^4e + 10^3d + 10^2c + 10b + a \\ &\equiv_p 0f + 0e + 0d + 0c + 0b + a \\ &= a\end{align}$$

That is, modulo $2$ or $5$ (or $10$), a number is equivalent to its last digit. In particular,

* A number is divisible by $2$ if and only if its last digit is divisible by $2$ (i.e., is $0$, $2$, $4$, $6$ or $8$)
* A number is divisible by $5$ if and only if its last digit is divisible by $5$ (i.e., is $0$ or $5$)
* A number is divisible by $10$ if and only if its last digit is divisible by $10$ (i.e., is $0$)

## Divisibility by $4$ or $25$ (or $100$)

When $p = 4$ or $p = 25$ (or $p = 100$), the powers of $10$, namely $1, 10, 10^2, 10^3, 10^4, \dots$ are respectively equivalent to $1, 10, 0, 0, 0, \dots$ and so we can replace a number $\mathrm{[fedcba]}$ with

$$\begin{align}\mathrm{[fedcba]} &= 10^5f + 10^4e + 10^3d + 10^2c + 10b + a \\ &\equiv_p 0f + 0e + 0d + 0c + 10b + a = 10b + a \\&= \mathrm{[ba]}\end{align}$$

That is, modulo $4$ or $25$ (or $100$), a number is equivalent to the number formed by its last two digits. (Mod 4 we can simplify further as $10 \equiv_4 2$, so we could take $2b + a$ instead of $\mathrm{[ba]}$, though in practice checking the divisibility of a two-digit number by $4$ is so easy that there's not much point.)

## Divisibility by $8$ or $125$ (or $1000$)

When $p =8$ or $p = 125$ (or $p = 1000$), the powers of $10$, namely $1, 10, 10^2, 10^3, 10^4, \dots$ are respectively equivalent to $1, 10, 100, 0, 0, \dots$ and so we can replace a number $\mathrm{[fedcba]}$ with

$$\begin{align}\mathrm{[fedcba]} &= 10^5f + 10^4e + 10^3d + 10^2c + 10b + a \\ &\equiv_p 0f + 0e + 0d + 100c + 10b + a \\ &= 10b + a \\ &= \mathrm{[ba]} \end{align}$$

That is, modulo $8$ or $125$ (or $1000$), a number is equivalent to the number formed by its last three digits.

## Divisibility by powers of $2$ or $5$ (or $10$)

You get the idea by now: a number is divisible by $2^k$ or $5^k$ (or $10^k$) if and only if the number formed by its last $k$ digits is divisible by that number.

## Divisibility by $3$ or $9$

When $p=3$ or $p = 9$, we have $10 \equiv_p 1$, so the powers of $10$, namely $1, 10, 10^2, 10^3, 10^4, \dots$ are respectively equivalent to $1, 1, 1, 1, 1, \dots$, so a number like

$$\begin{align}\mathrm{[fedcba]} &= 10^5f + 10^4e + 10^3d + 10^2c + 10b + a \\ &\equiv_p f + e + d + c + b + a\end{align}$$

That is, every number is equivalent to the sum of its digits. 

(This is also the basis of the [“casting out nines” method](https://en.wikipedia.org/w/index.php?title=Casting_out_nines&oldid=832611086#Checking_calculations_by_casting_out_nines) of sanity-checking arithmetic calculations by replacing each number by its mod-$9$ equivalent, what Ibn Sīnā called the “Hindu method”.)

## Divisibility by $11$

This gets slightly more interesting: when $p=11$, we have $10 \equiv_p -1$, so the powers of $10$, namely $1, 10, 10^2, 10^3, 10^4, \dots$ are respectively equivalent to $1, -1, 1, -1, 1, \dots$, so a number like

$$\mathrm{[fedcba]} = 10^5f + 10^4e + 10^3d + 10^2c + 10b + a \equiv_p -f + e - d + c - b + a$$

That is, a number is divisible by $11$ if and only if the number formed by the alternating sum of its digits (i.e. alternately adding and subtracting the digits) is. Note that, to be strictly equivalent modulo $11$, we should be careful that the last digit gets a positive sign (e.g. start from the right), but in practice if we only care about whether a number is divisible by $11$, we can simply start from the left: even if we end up with (something equivalent to) $-n$ instead of $n$, it does not affect divisibility by $11$. There's actually an insight here which I had missed before today. We'll encounter it shortly.

## Divisibility by $7$ (first attempt)

Here is where the story gets no longer so pleasant: when $p = 7$, we have $10 \equiv_p 3$, and $10^2 \equiv_p 2$, and $10^3 \equiv_p 6$, and $10^4 \equiv_p 4$, and $10^5 \equiv_p 5$, and $10^6 \equiv_p 1$ (and then this sequence of remainders repeats). In other words, the powers of $10$, namely $1, 10, 10^2, 10^3, 10^4, \dots$ are respectively equivalent modulo $7$ to $1, 3, 2, 6, 4, 5, 1, 3, 2, 6, 4, 5, 1, 3, 2, 6, 4, 5, \dots$ and so on repeating. What can we do with this information?

**One**, we could take a large number like $\mathrm{[onmlkjihgfedcba]}$ and rewrite it as

$$\mathrm{[onmlkjihgfedcba]} \equiv_p a + 3b + 2c + 6d + 4e + 5f + g + 3h + 2i + 6j + 4k + 5l + m + 3n + 2o$$

and so on, so that we're working with smaller numbers. But this arithmetic is really not very pleasant, and requires us to remember (or recalculate) quite a bit of information (the entire cycle of digit equivalents).

**Two,** we could retain just the information that $10^6 \equiv_p 1$, and use that to replace working with long numbers with working with (at most) six-digit numbers: 

$$\begin{align}\mathrm{[onmlkjihgfedcba]} &= 10^{12}\mathrm{[onm]} + 10^6\mathrm{[lkjihg]} + \mathrm{[fedcba]} \\ &\equiv_p \mathrm{[onm]} + \mathrm{[lkjihg]} + \mathrm{[fedcba]}\end{align}$$

so we need only “simple” addition of (up to) six-digit numbers.

**Three,** we could be slightly smarter and notice that as $10^3 \equiv_p 6 \equiv_p -1$, so we could either get by with half the amount of stuff to remember (in “One”, above) — the sequence of powers of $10$ is $1, 3, 2, -1, -3, -2, 1, 3, 2, -1, -3, 2, \dots$. Or, we could retain just this one piece of information, and use it to convert any given long number into an alternating sum of (at most) three-digit numbers.

$$\begin{align}\mathrm{[ponmlkjihgfedcba]} &= 10^{12}\mathrm{[onm]} + 10^9\mathrm{[lkj]} + 10^6\mathrm{[ihg]} + 10^3\mathrm{[fed]} + \mathrm{[cba]} \\ &\equiv_p\mathrm{[onm]} -\mathrm{[lkj]} + \mathrm{[ihg]} - \mathrm{[fed]} + \mathrm{[cba]}\end{align}$$

Thus we have an alternating sum of (up to) three-digit numbers. This is still not entirely comfortable to work with, at least for people (like me) of average arithmetic ability.

So far, it seems that there's no divisibility test by $7$ that's easier to execute than simply dividing by $7$.

## A new idea

This was the extent of my knowledge since childhood, until today: of the numbers $1$ to $16$, there are reasonably simple divisibility tests for $1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16$, but not really very good ones for $7$ or $13$ (and therefore $14$).

Today, I encountered an elegant idea implicit in [this post](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/). Note that so far, all the divisibility tests we encountered were always retaining a number equivalent (i.e. congruent modulo $p$) to the original number — in other words, they actually give the remainder when the original number is divided by $p$ (and remainder being $0$ is the “divisible” case). But if we only care about whether a number is divisible by $p$ or not, there's a further trick we can use, which was implicit in the test of divisbiility by $11$ but not fully utilized so far.

Namely: if we pick a constant $k$ such that $\gcd(k, p) = 1$, then a number $n$ is divisible by $p$ if and only if the number $kn$ is divisible by $p$.

This is how we use it: consider a number $\mathrm{[fedcba]} = 10\mathrm{[fedcb]} + a$. When we multiply by $k$, we get $10k\mathrm{[fedcb]} + ka$. Now, if we had picked $k$ such that $10k \equiv_p 1$, then this $10k\mathrm{[fedcb]} + ka$ is simply equivalent to $\mathrm{[fedcb]} + ka$. That is, we can peel off the last digit (getting a number with one fewer digit), and simply add a small number based on the last digit.[^fnvm]

[^fnvm]: Apparently this trick occurs in the “Vedic Mathematics” book of Swami Bharati Krishna Tirtha, former Shankaracharya of the Govardhana Pitha in Puri. Although I encountered this book in childhood, I did not get very far as I found it a strange and frustrating book (compared to other mathematics books) — in hindsight I realize better what the author was trying to do and exactly what it was that frustrated me; may write more on that some other time. Also, according to [that post](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/), this divisibility test was apparently also a folk method known in India before the book too.

## Restating the test

To state it more precisely, the generalized rule for test of divisibility is:

1. Given a number $p$ that is not divisible by $2$ or $5$, find a number $k$ such that $10k \equiv_p 1$. (Such a number will always exist—it's the multiplicative inverse of $10$ modulo $p$—and moreover the number $k$ will have no common factors with $p$.)

2. Given an integer $n$, suppose its last digit is $a$, i.e. the integer $n$ is $10b + a$ for some integer $b$. Then replace $n$ with $b + ka$.

3. Repeat (go back to Step 2) until you have a number that is easy to test for divisibility by $p$.

Of course, at any time during this process you can replace any integer with any other integer that is equivalent modulo $p$. Also, in Step 1, we can pick any integer $k$, but the smaller it is, the easier the computation would be, so we might as well pick the smallest one.

Note: If you were initially given a number $p$ that is divisible by 2 or 5, first remove all factors of 2 and 5 (can test for divisibility by them separately) before going to Step 1.

Step 1 is “pre-processing”; we do it once for each $p$. Step 3 simply says to loop Step 2. And Step 2, which is the heart of the process, is equivalent (modulo $p$) simply to a multiplication by $k$.

## Example: divisibility by $7$ (second attempt)

For $p = 7$, the smallest $k$ such that $10k \equiv_p 1$ is $k = 5$, as $50 - 1 = 7\times 7$. This (finding $k=5$) is Step 1. So given a number $n$ like $\mathrm{[fedcba]}$, we can replace it (Step 2) with:

$$\mathrm{[fedcba]} \rightarrow \mathrm{[fedcb]} + 5a$$

and iterate on this, whatever its new last digit. Note that this is equivalent to a multiplication by $k=5$, i.e. our replaced number $\mathrm{[fedcb]} + 5a \equiv_7 5\mathrm{[fedcba]}$, which is easy to verify with a simple subtraction: $5(10x + y) - (x + 5y) = 49x \equiv_7 0$, so $x + 5y \equiv_7 5(10x + y)$.

As a concrete example, given the number $826417$, we can replace it with 

$$\begin{align}826417 &\rightarrow 82641 + 5\times7 = 82641 + 35 = 82676 \\ &\rightarrow 8267 + 5\times6 = 8267 + 30 = 8297 \\ &\rightarrow 829 + 5\times7 = 829 + 35 = 864 \\ &\rightarrow 86 + 5\times4 = 86 + 20 = 106 \\ &\rightarrow 10 + 5\times6 = 10 + 30 = 40\\&\rightarrow 4\end{align}$$

which is not zero, so the number $826417$ is not divisible by $7$. 

In practice we can use two further shortcuts:

* as mentioned before, we can always replace any number by something equivalent mod $7$,
* in particular, there's no requirement that $k$ be positive, so we could also take $k = -2$, as $10k \equiv_7 1$ in that case as well (or another way of saying this: $5 \equiv_7 -2$, so even for multiplication we can at any time multiply by $-2$ instead of multiplying by $5$).

So in practice, one could replace digits larger than $7$ with their equivalents, and also multiply by either $5$ or $-2$ depending on which looked easier (to add / subtract). For example, one might instead do:

$$\begin{align}826417 &\equiv_7 126410 \leftrightarrow 12641 \\ &\rightarrow 1264 - 2\times7 = 1264 - 14 = 1250 \leftrightarrow 125 \\ &= 125 \equiv_7 55 \equiv_7 -1\end{align}$$

with less computation, where:

* we replaced $8$ with $1$ and $7$ with $0$ (on the first line) and $12$ with $ 5$ (on the last line) as they are equivalent modulo $7$, 
* we cast out trailing $0$s (denoted by $\leftrightarrow$) using the fact that $7$ divides $10x$ if and only if $7$ divides $x$ (as $\gcd(10, 7) = 1$), and 
* only once needed to use Step 2, and even there we noticed that $1264$ was easy to subtract $14$ from, so we chose to use $k=-2$ instead of (the equivalent) $k=5$.

All in all, this gives a highly comfortable (for hand computation) test for divisibility by $7$ (much easier than directly dividing by $7$), something we were lacking earlier.

## Divisibility by $13$

For $p = 13$, we can take $k=4$ (check that $10k = 40 \equiv_{13} 1$), so (with the same example for $n$), we get:

$$\begin{align}826417 &\rightarrow 82641 + 4\times7 = 82641 + 28 = 82669 \\ &\rightarrow 8266 + 4\times9 = 8266 + 36 = 8302 \\ &\rightarrow 830 + 4\times2 = 830 + 8 = 838 \\ &\rightarrow 83 + 4\times8 = 83 + 32 = 115 \\ &\rightarrow 11 + 4\times5 = 11 + 20 = 31\\&\rightarrow 3 + 4\times1 = 3 + 12 = 15\end{align}$$

and this is probably a good place to stop as it's obvious that $15 \equiv_{13} 2$ is not divisible by $13$. (Incidentally, if we blindly iterated the procedure from here, we'd actually end up with a *higher* number before reaching a $1$-digit number: $15 \rightarrow 1 + 4\times5 = 21 \rightarrow 2 + 4\times1 = 6$.)

Again, in practice, we'd be more free with casting out multiples of $13$, or other irrelevant numbers, or switching between $k=4$ and $k = -9$; for example the computation may instead go:

$$\begin{align}826417 &\equiv_{13}826404 \\ &\rightarrow 82640 - 9\times4 = 82640 - 36 = 82604 \\ &\rightarrow 8260 + 4\times4 = 8260 + 16 = 8276 \\ &\rightarrow 827 + 4\times6 = 827 + 24 = 851 \\ &\equiv_{13}201 \\ &\rightarrow 20 + 4\times1 = 24\end{align}$$

which we can see is not divisible by $13$.

## Divisibility by $19$

This is a particularly easy case for the method as $k = 2$ works, so we can get, for example:

$$\begin{align}826417 &\rightarrow 82641 + 2\times7 = 82641 - 14 = 82655 \\ &\rightarrow 8265 + 2\times5 = 8265 + 10 = 8275 \\ &\rightarrow 827 + 2\times5 = 827 + 10 = 837 \\ &\rightarrow 83 + 2\times7 = 83 + 14 = 97 \\ &\rightarrow 9 + 2\times7 = 9 + 14 = 23 \end{align}$$

which we can see is not divisible by $19$. (Or we might have stopped one step earlier, if we remember that $95$ is a multiple of $19$.)

## Analysis of iteration: modulo $p$

We can ask: if we strictly follow the method, i.e. iterate “Step 2”, what happens to a starting number $n$?

As noted before, when viewed through a “mod p” lens, our “Step 2” is simply a multiplication by $k$. 

When $n$ is actually divisible by $p$ (i.e. when $n \equiv_p 0$), then multiplication by $k$ changes nothing: our number was $0$ and remains $0$; it just becomes clearer as the number gets turned into a smaller equivalent number.

Otherwise, as $10k \equiv_p 1$ and therefore $\gcd(k, p) = 1$, there exists a smallest number $r$ such that $k^r \equiv_p 1$. This number $r$ is called the multiplicative order of $k$ modulo $p$. (Incidentally, as $10 \equiv_p k^{-1}$ and therefore $10^m \equiv_p k^{-m}$, this $r$ is also the multiplicative order of $10$ modulo $p$.)

Here for the first time in this post, let's assume that $p$ is prime, for simplicity. So the number $n$ will, on iteration, cycle through the $r$ distinct values $n, kn, k^2n, \dots, k^{r-1}n$, before landing at $k^rn = n$ again. (If $p$ is not prime, it could happen that these values are not distinct, and that needs more analysis.) Thus, if we construct a directed graph with an edge from each number mod $p$ (each equivalence class) to the number (equivalence class) it is taken by a single iteration of “Step 2”, then the $p-1$ numbers not divisible by $p$ fall into cycles of length exactly $r$ each, while the number $0$ is on its own.

For example:

* for $p = 19$, we have $k = 2$, and its multiplicative order is $18$, so every number other than $0$ returns to itself in $18$ steps of the iteration (and not before),
* for $p =13$, we have $k =4 $, and its multiplicative order is $6$, so every number other than $0$ returns to itself in $6$ steps of the iteration (and not before) — in other words the $13$ nodes of the graph are partitioned into the single node $0$, and two cycles of $6$ nodes each.

Incidentally, note that $k \equiv_p 10^{r-1}$ (where $r$ is the multiplicative order of $k$ and of $10$), i.e. $k$ is the last number in the sequence of powers of $10$ before we hit $1$ again.

Also, note that the sum of all numbers in any cycle is (picking $n$ to be any number in the cycle) congruent to $n(1 + k + k^2 + \dots + k^{r-1}) = n(k^r - 1)/(k - 1) \equiv_p 0$, as by definition, $k^r - 1\equiv_p 0$. 

## Analysis of iteration: *not* modulo $p$

If instead of looking at numbers through this “mod p” lens we care about the actual values obtained on iteration, then the analysis becomes more involved, and there are more details. For example, starting from some number $n$, even though after $r$ steps we will have returned to (something congruent to) $n$, the actual value may be a different number, so we may need more steps before we return to the *actual* value $n$, if at all. (The length of the cycle will always be a multiple of $r$ though, as underneath, modulo $p$ we're still cycling after every $r$ nodes.)

This requires more care, and there are more possibilities, and as we take larger numbers $n$ we get larger graphs. For an exploration of all this, see [the post linked earlier](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/). An illustration of the difference: for $p = 7$, when viewed through a “mod 7” lens, there are only $7$ possible nodes in the graph: the node $0$ by itself, and the other nodes which fall into a directed cycle $1 \rightarrow 5 \rightarrow 4 \rightarrow 6 \rightarrow 2 \rightarrow 3 \circlearrowleft$. But when *not* viewed modulo $p$, then for example $1$ has many representatives ($8$, $15$, $22$, etc), similarly $3$ has many representatives ($10$, $17$, $24$, etc.) and distinguishing them gives a much richer graph: see Figure 5 in [that post. Enjoy!](https://manasataramgini.wordpress.com/2018/11/11/visualizing-the-hindu-divisibility-test/)


----
