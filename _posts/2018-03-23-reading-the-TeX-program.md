---
layout: post
title: Reading the TeX program
tags: [draft, tex]
excerpt: Lessons learned, thoughts, advice
date: 2018-03-23
---

For a while now, I have been trying to read the source code of TeX. It has been an interesting experience. I have had some glimmers of understanding, and have a long way to go. Here are some thoughts that may be helpful for anyone else attempting the same thing.

## Challenges

The TeX program is exceptionally well-documented, for a program of its size and age. It is written in accordance with the idea of *Literate Programming*, which Knuth devised while writing TeX (and considers one of the best things that resulted from the writing of TeX). The whole program is available as a published book (*TeX: The Program*, Volume B of *Computers & Typesetting*), and [in PDF form](http://texdoc.net/texmf-dist/doc/generic/knuth/tex/tex.pdf). So reading it seems like it ought to be easy.

One of the primary challenges for a modern programmer reading it, though, is that it's not written anything like the way we would expect it to be. To read the TeX program, one has to overcome:

* idiosyncracies of 1950s/60s/70s programming style,
* idiosyncracies of Pascal programming style,
* idiosyncracies of WEB programming style,
* idiosyncracies of Knuth's own programming style.

### 19[567]0s style

The TeX program was written during 1980–1982, as a rewrite of an earlier version (now retrospectively called TeX78) that was written in the SAIL programming language available at the Stanford Artificial Intelligence Laboratory where Knuth had computer access. Like anything else, it is influenced by the environment of its time and of its author.

Don Knuth entered Case Institute of Technology in 1956, encountered a computer (the IBM 650) and started programming. That's where he (co-)wrote RUNCIBLE, and by 1960 he was performing heroic feats like [writing an ALGOL 65 compiler for Burroughs](http://ed-thelen.org/comp-hist/B5000-AlgolRWaychoff.html#7) over summer break. So that was the era of his programming education. One of Knuth's classic papers on programming, which gives an insight into the world of the time and the way Knuth thinks, is *Structured Programming with go to Statements*, published 1974.

The first version of TeX was written in 1977–78, and the second (current) version was primarily a rewrite, but (I suspect) strongly influenced by the design of the first version. So forget about post-1980 programming practices. (For example, the C programming language didn't become popular outside Bell Labs circles until the 1980s.)

In fact, if we look at *Exercises in Programming Style* ([review](https://henrikwarne.com/2018/03/13/exercises-in-programming-style/)), and look at its first entry (“Good Old Times”), I'm reminded of my experience reading the TeX program: most of the memory the program uses is just laid out as an array, etc.

### Pascal style and WEB style

Knuth chose Pascal because he wanted the new TeX program to be portable—after his Gibbs lecture to the AMS, a lot of people at other universities (etc.) were interested in the program he had written primarily for himself—and Pascal, then very popular in education, was the language most widely available at the time, at least in the kind of places where people were interested in using TeX. (C had not yet ventured far from its Bell Labs home.)

Pascal, at least the version of Pascal in which Knuth wrote TeX (the [“Pascal-H”](http://texdoc.net/texmf-dist/doc/generic/knuth/tex/tex.pdf#page=3) available at SAIL), did not have `break`, `continue`, or even `return` statements. To return a value from a function, you assign the value to a “variable” with the name that of the function, and the value is returned when control reaches the end of the function. (I wonder how many of the modern programmers who parrot “goto considered harmful” would be willing to program in a C-like language without them.) To overcome these problems, he has evolved a certain “`goto` discipline”, a consistent way of using `goto`s with labels like `continue` and `return`, and a few unusual ones of his own, like `reswitch`. 

In fact, for most of the criticisms in Kernighan's “*Why Pascal is Not My Favorite Programming Language*”, there are workarounds in the way Knuth uses it. (That article/paper was written in 1981, at around the same time TeX was being written.)

Some more:

* The semicolon is a statement separator, not a statement terminator: the last statement shouldn't (or at least needn't) have a semicolon
* Function invocations don't have `()`, so when you see something of the form `x := y`, it may be variable assignment *or* `y` may be a function call.

### WEB style and Knuth's style

I like to think of it this way: in the beginning, there was machine-oriented (assembly-language, etc.) programming, which was hard to read and maintain. Starting from there, 

... come up with some techniques: encapsulation, abstract data types....

... DEK has different solutions...

Other aspects of his style: bottom-up, machine sympathy, does everything himself (e.g. hash tables), ...

The organization of the program is really interesting: it's neither top-down (most important ideas first), nor bottom-up. It's mostly *bottom-up*, but it's more like a book (especially a mathematics textbook). The most important bits (or highest-level / crux of the thing) aren't necessarily either at the beginning or the end, but are more likely in the middle.

Other minor things:

* Indentation around `begin` etc. is really weird.
* The typesetting will put multiple statements on a line simply if they fit; for no good reason (saving paper?)

## Tips

1. Read the typeset version, not the `.web` file
2. The book is better than the result of `weave`. So is the typeset version online (with hyperlinks)

### Sidle up to TeX

1. Read other WEB programs, preferably those by DEK.
   Namely:

   ```
   tex/tex.web
   tex/glue.web
   mf/mf.web
   web/weave.web
   web/tangle.web
   etc/vftovp.web
   etc/vptovf.web
   texware/pooltype.web
   texware/pltotf.web
   texware/tftopl.web
   texware/dvitype.web
   mfware/mft.web
   mfware/gftype.web
   mfware/gftopk.web
   mfware/gftodvi.web
   ```


2. Good ones to start with may be `glue.web` (just a toy example), `dvitype.web` (good standalone program), and `tangle.web` and `weave.web`.
3. Read WEB programs by others. One I know of is `bibtex.web`. A few others in the TeX Live repo seem to be `cftest.web` (a toy program for testing `tangle`), `dvicopy.web` (by PB, the author of eTeX), `patgen.web`, `pktogf.web`, `pktype.web`, `pdftex.web`, `xetex.web`, and Omega versions:
   * `odvicopy.web`, `odvitype.web`, `ofm2opl.web`, `opl2ofm.web`, `otangle.web`, `ovf2ovp.web`, `ovp2ovf.web`
4. Read other programs by DEK. (See <https://cs.stanford.edu/~knuth/programs.html> and <https://github.com/shreevatsa/knuth-literate-programs/tree/master/programs>)
5. Read other implementations of TeX. (See <https://github.com/tex-other/> for a few, still being collected.)

### Other tips

* Watch the DEK videos (“The Internal Details of TeX82”)
* Read similar programs of that era (Pascal compiler (P4?), Crenshaw “Let's Build a Compiler”, etc.)

## Structure of the program

At a broad level 

----
