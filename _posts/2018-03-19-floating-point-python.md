---
layout: post
title: Seeing floating-point numbers in Python
tags: [draft, maths, software]
excerpt: How to see a “raw” floating-point number, etc.
date: 2018-03-19 14:00
---

## The “exact” value of a floating-point number

In Python, to see how a floating-point number is stored, you can use `.hex()` which returns a string. For example, we have:

```python
float('2.2').hex() == float('2.2000000000000002').hex() == '0x1.199999999999ap+1'
```

In this output, the part from `0x` to `p` is in hexadecimal. For example (dropping the `.`):

```python
int('1199999999999a', 16) == 4953959590107546
```

so the string `'0x1.199999999999ap+1'` represents the fraction (dyadic rational)

$$\frac{4953959590107546}{2^{51}}$$

In other words, when you write `2.2` or `2.2000000000000002` in Python, the exact number stored internally is 4953959590107546 / 2^51, which is exactly `2.20000000000000017763568394002504646778106689453125`. (You can get this “exact” number more directly with something like `print '%.100f' % 2.2`.)

## Printing a floating-point number

In Python before 2.7, the printing routine was sub-optimal: it printed the above number as the longer `2.2000000000000002` instead of the shorter `2.2`, even though both of these round to the same exact value (`2.20000000000000017763568394002504646778106689453125`).

Printing numbers as their shortest decimal representation is a solved problem since 1990, although there continue to be developments even [in 2016](http://cseweb.ucsd.edu/~lerner/papers/fp-printing-popl16.pdf). (See [this post](https://shreevatsa.wordpress.com/2015/04/01/printing-floating-point-numbers/) for some links.) It's just that Python until 2.7 didn't bother to find shortest representation.

For references to this change, see

* <https://docs.python.org/2/whatsnew/2.7.html#python-3-1-features>:

  > The [`repr()`](https://docs.python.org/2/library/functions.html#repr) of a float `x` is shorter in many cases: it’s now based on the shortest decimal string that’s guaranteed to round back to `x`. As in previous versions of Python, it’s guaranteed that `float(repr(x))` recovers `x`.

* <https://docs.python.org/3/whatsnew/2.7.html#other-language-changes>:

  > Related to this, the [`repr()`](https://docs.python.org/3/library/functions.html#repr) of a floating-point number *x* now returns a result based on the shortest decimal string that’s guaranteed to round back to *x* under correct rounding (with round-half-to-even rounding mode). Previously it gave a string based on rounding x to 17 decimal digits.
  >
  > The rounding library responsible for this improvement works on Windows and on Unix platforms using the gcc, icc, or suncc compilers. There may be a small number of platforms where correct operation of this code cannot be guaranteed, so the code is not used on such systems. You can find out which code is being used by checking [`sys.float_repr_style`](https://docs.python.org/3/library/sys.html#sys.float_repr_style), which will be `short` if the new code is in use and `legacy` if it isn’t.
  >
  > Implemented by Eric Smith and Mark Dickinson, using David Gay’s `dtoa.c` library; [bpo-7117](https://bugs.python.org/issue7117).

* <https://bugs.python.org/issue7117>

* discussion at <https://mail.python.org/pipermail/python-dev/2009-October/092958.html>

## Next and previous floating-point numbers

Given a floating-point number `f`, can we find the next and previous floating-point numbers? See the answers on StackOverflow to [this question](https://stackoverflow.com/questions/10420848/how-do-you-get-the-next-value-in-the-floating-point-sequence) and to [this question](https://stackoverflow.com/questions/6063755/increment-a-python-floating-point-value-by-the-smallest-possible-amount). Below is the code by [Mark Dickinson](https://stackoverflow.com/users/270986/mark-dickinson):

```python
import math
import struct

def next_up(x):
    # NaNs and positive infinity map to themselves.
    if math.isnan(x) or (math.isinf(x) and x > 0):
        return x

    # 0.0 and -0.0 both map to the smallest +ve float.
    if x == 0.0:
        x = 0.0

    n = struct.unpack('<q', struct.pack('<d', x))[0]
    if n >= 0:
        n += 1
    else:
        n -= 1
    return struct.unpack('<d', struct.pack('<q', n))[0]

def next_down(x):
    return -next_up(-x)
```

For example, something like (with another function not shown here, because I haven't implemented it properly):

```python
f = 2.2
print('%.100f' % next_down(f))
print('%.100f' % f)
print('%.100f' % next_up(f))
```

outputs:

```
2.199999999999999733546474089962430298328399658203125000000000 4953959590107545/2**51
2.200000000000000177635683940025046467781066894531250000000000 4953959590107546/2**51
2.200000000000000621724893790087662637233734130859375000000000 4953959590107547/2**51
```

while the same with `f = 8.0` outputs:

```
7.999999999999999111821580299874767661094665527343750000000000 9007199254740991/2**50
8.000000000000000000000000000000000000000000000000000000000000 4503599627370496/2**49
8.000000000000001776356839400250464677810668945312500000000000 4503599627370497/2**49
```

Oh well, the improperly implemented function used above (only tested for positive and large (greater than $1/2^{1024}$) numbers is:

```python
def dyadic(f):
    """Given the float 2.2, returns the string "4953959590107546/2**51", etc."""
    s = f.hex()
    if f <= 0.0:
        raise NotImplementedError
    assert s.startswith('0x1.'), f.hex()
    s = '1' + s[4:]
    foo = 1
    if '+' in s:
        where = s.find('+')
    elif '-' in s:
        where = s.find('-')
        foo = -1
    else:
        raise NotImplementedError
    before = s[:where]
    after = s[where + 1:]
    assert before.endswith('p')
    before = before[:-1]
    prec = int(after)
    assert s.endswith('p+%d' % prec if foo == 1 else 'p-%d' % prec), f.hex()
    prec = 52 - prec if foo == 1 else 52 + prec

    numerator = int(before, 16)
    denominator = 2**prec
    lhs = float(numerator) / denominator
    assert lhs == f, (f, numerator, denominator, lhs)
    return '%d/2**%d' % (numerator, prec)
```

## See also

* <https://shreevatsa.wordpress.com/2015/04/01/printing-floating-point-numbers/>
* <https://cs.stackexchange.com/a/81039/891>

----
