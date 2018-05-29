---
layout: post
title: Approximating $\lg (n!)$
tags: [draft, math]
excerpt: How can we compute the logarithm of the factorial?
date: 2018-03-19 10:00
---

Came up at [this question on math.SE](https://math.stackexchange.com/questions/2696344/is-there-a-way-to-find-the-log-of-very-large-numbers/2696487#2696487), and highlights my ignorance of floating-point issues. 

Suppose we want to compute $\lg (256!)$ or in general $\lg (n!)$ for some $n$. How do we (and can we) find the value to sufficient accuracy, or find the closest floating-point number to that value?

More specifically, consider these two approaches:

1. [“Sum approximation”] $$\displaystyle \lg (n!) = \sum_{i = k}^{n} \lg k$$
2. [Stirling's approximation] 
   $$\begin{align}\displaystyle \lg(n!) &= \frac{\ln n!}{\ln 2} \\\ &\sim n\lg n - \frac{n}{\ln 2} + \frac12\lg(2\pi n) +\frac{1}{12n\ln 2} - \frac{1}{360n^3\ln 2} + \frac{1}{1260n^5\ln 2} - \frac{1}{1680n^7\ln 2} + \cdots\end{align}$$



What is the floating-point error we can expect, in the two cases?

In code:

```python
"""Approximating lg(n!)."""

import math
import sys  # For detecting Python version

def ln(x): return math.log(x)
def lg(x): return math.log2(x) if sys.version_info >= (3, 3) else math.log(x, 2)

def sum_approx(n):
    return sum(lg(i) for i in range(1, n + 1))

def stirling_approx(n):
    return (n * lg(n)
            - n / ln(2)
            + 0.5
            + lg(n * math.pi) / 2
            + 1 / (n * 12 * ln(2))
            - 1 / (n**3 * 360 * ln(2))
            # + 1 / (n**5 * 1260 * ln(2))
            # - 1 / (n**7 * 1680 * ln(2))
           )

print('%.20f (sum)' % sum_approx(256))
print('%.20f (stirling)' % stirling_approx(256))
print('%.20f (best floating-point)' % 1683.9962872242146194061476793149931595240236431092583855)
print('1683.9962872242146194061476793149931595240236431092583855'[:25] + ' (exact digits)')
```

Output with Python 2.7:

```
1683.99628722421380189189 (sum)
1683.99628722421448401292 (stirling)
1683.99628722421471138659 (best floating-point)
1683.99628722421461940614 (exact digits)
```

Output with Python 3.6:

```
1683.99628722421357451822 (sum)
1683.99628722421448401292 (stirling)
1683.99628722421471138659 (best floating-point)
1683.99628722421461940614 (exact digits)
```

One-liner for the first few terms of the Stirling series approach, for Python 3.3+:

```python
(n*math.log2(n) - n/math.log(2) + math.log2(n*math.pi*2)/2 + 1/(n*12*math.log(2)) - 1/(n**3*360*math.log(2)))
```

In the first case (sum), we're adding a lot of floating-point numbers, and there's some potential error at each one, so the error accumulates. (Incidentally, as someone pointed out, the error would be more if we did the addition in the other direction, from largest number first.) And the algorithm takes $\Omega(n)$ time.

In the second case, there's error already in the computation of $\ln 2$, and on top of that were doing divisions, so there's scope of error there too.

Questions:

* How exactly do we estimate the error in the two cases? 
* How can we find the closest floating-point number to the actual answer?
* How can we compute the answer to arbitrary accuracy?

I have no idea how to answer questions like this. I need to learn. Maybe it's time to finally read that “What every … about floating point” by Goldberg, and think in terms of “ulp”s and all that.

For a function like this, if it comes up frequently, we'd probably want to implement a function that returns the closest floating-point number, and give it a name. (Then any further error would be smaller.) This I guess is one reason why math libraries implement things like `hypotl`. It [appears](https://math.stackexchange.com/a/2697902/205) that many libraries already do this in this case, by implementing a `lngamma` or similar function (see [Log Gamma function](http://mathworld.wolfram.com/LogGammaFunction.html) on MathWorld).

----
