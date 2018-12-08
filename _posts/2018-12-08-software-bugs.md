---
layout: post
title: Surely a bug
excerpt:
date: 2018-12-08
tags: [mathematics, software]

---

For another story about mathematics and software bugs, see [here](https://mathoverflow.net/a/11607):

> I don't know any interesting bugs in symbolic algebra packages but I know a true, enlightening and entertaining story about something that looked like a bug but wasn't.$\def\sinc{\operatorname{sinc}}$
>
> Define $\sinc x = (\sin x)/x$.
>
> Someone found the following result in an algebra package:
>
> $\int_0^\infty dx \sinc x = \pi/2$
>
> They then found the following results:
>
> $\int_0^\infty dx \sinc x \; \sinc (x/3)= \pi/2$
>
> $\int_0^\infty dx \sinc x \; \sinc (x/3) \; \sinc (x/5)= \pi/2$
>
> and so on up to
>
> $\int_0^\infty dx \sinc x \; \sinc (x/3) \; \sinc (x/5) \; \cdots \; \sinc (x/13)= \pi/2$
>
> So of course when they got:
>
> $\int_0^\infty dx \sinc x \; \sinc (x/3) \sinc (x/5) \; \cdots \; \sinc (x/15)$$=
> \frac{467807924713440738696537864469}{935615849440640907310521750000}\pi$
>
> they knew they had to report the bug. The poor vendor struggled for a long time trying to fix it but eventually came to the stunning realisation that this result is correct.
>
> These are now known as [Borwein Integrals](http://mathworld.wolfram.com/BorweinIntegrals.html).

by Dan Piponi answered Jan 13 '10 at 2:14 and comments:

> - The actual person at that "poor vendor" was me. I must have spent 3 days on this problem before I figured out that Jon had tricked me. And, indeed, I am an expert in computer algebra, but do not know much Fourier analysis. But Jon's proof for why this is 'correct' is quite geometrical. – Jacques Carette Feb 17 '10 at 4:03
> - @Voyska No, it was not reported as a bug, just as an 'oddity' (or something like that). Jon was not mean, but playful in a devious way. He will be missed. – Jacques Carette Aug 18 '16 at 18:18

See also <https://twitter.com/johncarlosbaez/status/1043161440545267713> → <https://johncarlosbaez.wordpress.com/2018/09/20/patterns-that-eventually-fail/> for more.

----
