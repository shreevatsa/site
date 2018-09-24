---
layout: post
title: The structure of old PDF files with bitmap fonts
excerpt: How were PDFs made by Ghostscript in the 1990s?
date: 2018-09-04
tags: [draft]

---

(This is something I started writing and abandoned... you may want to read this only after I've returned to this and tidied it up properly.)

In the previous post, we looked at a simple PDF file, generated with modern methods -- what objects it contains, how they are related, etc.

Now let's switch gears and look at a very atypical (these days) PDF file, and a large one at that, namely this file: <http://www.vldb.org/conf/1999/P29.pdf>. With `mutool clean -d P29.pdf P29-mutool.pdf` (not bothering with `qpdf --qdf --object-streams=disable P29.pdf P29-qpdf.pdf` right now) one can see that, for example, the second page[^secondpage] refers to two fonts:

[^secondpage]: Why the second page? I wanted to look at the second page rather than the first page because it has a layout more typical of the rest of the pages, but coincidentally it's also the case that the first object in this PDF file happens to be for the second page.

    /Font <<
      /B 173 0 R
      /A 166 0 R
    >>

Pursuing Object 173, one sees that the font `/B` does not quite look like the examples we saw in the last post. This PDF file is clearly using some other sort of font technology. For one thing, the object has a bunch of `/CharProcs`, like:

      /CharProcs <<
        /a0 271 0 R
        /a1 267 0 R
        /a10 202 0 R
        /a100 217 0 R
        /a101 221 0 R

What are these? According to the PDF spec, `CharProcs` is:

> A dictionary in which each key is a character name and the value associated with that key is a content stream that constructs and paints the glyphs for that character.

So let's go deeper and look at object 271, which was associated with character name `a0` above:

    271 0 obj
    <<
      /Length 177
    >>
    stream
    0 0 0 0 23 67 d1
    23 0 0 67 0 0 cm
    BI
    /IM true/W 23/H 67/BPC 1/F/CCF/DP<</K -1
    /Columns 23
    /BlackIs1 true
    >>
    ID 【...about 60 bytes of binary data...】
    EI
    endstream
    endobj

This is supposed to be the "content stream that constructs and paints the glyphs for that character". It may be helpful to actually look at this iamge data visually, so let's pursue this further.

Here, `BI`, `EI`, `ID` are PDF operators for the begin/end of image data, and the actual image data, for inline images (see section 4.8.6 Inline Images in the PDF reference). The keys above stand for: ImageMask, Width, Height, BitsPerComponent, Filter (CCITTFaxDecode), and DecodeParms [sic]. The value for `/DP` is itself a dictionary, the parameters to the CCITTFaxDecode filter being used here, whose keys represent (see Table 3.9):

- `/K`: according to the PDF reference, it only matters whether K is negative (*"pure two-dimensional encoding (Group 4)"*), zero (*"pure one-dimensional encoding (Group 3, 1-D)"*) or positive (*"mixed... (Group 3,2-D)"*).

- `/Columns`: "The width of the image in pixels." (The PDF reference also says "If the value is not a multiple of 8, the filter adjusts the width of the unencoded image to the next multiple of 8, so that each line starts on a byte boundary" but I think this may not be actually true, and may depend on the `EncodedByteAlign` described just above.)

- `BlackIs1`: self-explanatory.

Decoding the "CCITT Group 4" image data inside `ID` became a task of its own, so I've separated it into another post.


Going back to the font object 173, it also has an encoding, like:

      /Encoding 167 0 R

Finally, if you look at the actual place text is set (drawn? laid out?), it looks something like this (using `【ab】` to stand for the hex byte `0xAB`, etc):

      /A 1 Tf
      0.1 0 0 -0.1 65.2 734.6 Tm(g'【8b】*aU【97】&【8b】【1b】mRgKpfk*aUj5gKsUaUc【98】t0【83】|【91】Tn<mIn<j0cQp【7f】nIo【7f】nRgip【7f】m【8c】【8b】w【8b】5gio?adj0【9d】Pn<o【7f】cfad【97】0gKcfn<k)Tj

where the non-ASCII bytes (i.e. bytes < 32 or > 126, which in ASCII don't correspond to printable characters) occur interspersed with the smaller bytes: they are just bytes; ASCII or not doesn't mean anything. (Remember: it is not text!)

Now, what if we wanted to insert text into this document, in our own font? Could we just add that font as a resource, insert it into this document, and set text in it? It's worth a try,
but there appear to be a bunch of problems here:

* The font `/A` is chosen at size 1, not something like 9.9626, i.e. the scaling is probably different.

* There is a text matrix or something going on, with Tm -- again, the scaling may be different.

Let's try it anyway. We can generate a PDF containing all characters, say something like this `ascii.tex`:

    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    abcdefghijklmnopqrstuvwxyz
     0123456789
    !`` '' ` '  ( ) * + , - . / : ; = ? @ [ ] ` { | }
    
    \bye
    
Then we can extract the relevant objects out of the PDF (after uncompressing), namely, 
copy from `qpdf --qdf --object-streams=disable ascii.pdf ascii-qpdf.pdf`,
and add them to `P29-qpdf.pdf` after re-numbering. (E.g. 7, 8, 9, 10 or whatever, to 1094, 1095, 1096, 1097 or whatever.) Then run

    fix-qdf < P29-qpdf.pdf > P29-qpdf-fixed.pdf

This works, though it's not clear whether it's done anything. The next step is to remove something from the file. From Page 2, if I remove the first line, I can see in the output that the line disappears. Great!

Next step is to add this font as a resource, to say Page 2. That seems to work too.

Finally, we've come to the real problem: getting text onto the page. If just before the `/A 1 Tf`, I add something like `/F1 100 Tf (hello world) Tj`,
then I'm able to get *something* onto the page, though at the wrong location and in the wrong size.

Fixing this will require understanding the sizes, and the text matrix `Tm`, and everything.

Some reading:
the [basics are here](https://blog.idrsolutions.com/2010/04/understanding-the-pdf-file-format-text-streams/).
Some [warnings about text extraction](https://blog.idrsolutions.com/2009/04/pdf-text/).
If you are a nice person, you can generate PDFs containing [/ActualText](https://blog.idrsolutions.com/2012/04/understanding-the-pdf-file-format-actualtext/), so that others can extract text.
But that's not relevant to us here right now.
There's [useful info on what GhostScript does](https://blog.idrsolutions.com/2010/10/why-can-i-not-extract-text-from-this-ghostscript-generated-pdf-file/) (which is probably what is going on in P29.pdf).
A [note on space and Tw](https://blog.idrsolutions.com/2011/09/understanding-the-pdf-file-format-%E2%80%93-space-is-a-special-character/).
A [trick to infer spaces](https://blog.idrsolutions.com/2010/12/text-spaces-in-pdf-files/).
Another [note on spaces](https://blog.idrsolutions.com/2011/11/space-the-final-frontier-in-pdf/).

All that did not help, so let's read [the actual spec](http://benno.id.au/refs/PDFReference15_v5.pdf).
Chapter 5 is on text, from pages 349 to 436. That's a lot of pages to be reading when it's already past the time I'm supposed to sleep.
Some things though:

    /F13 12 Tf
    288 720 Td
    (ABC) Tj

> Note: What these steps produce on the page is not a 12-point glyph, but rather a 12-unit glyph, where the unit size is that of the text space at the time the glyphs are rendered on the page. The actual size of the glyph is determined by the text matrix (Tm) in the text object, several text state parameters, and the current transformation matrix (CTM) in the graphics state; see Section 5.3.3, “Text Space Details.” If the text space is later scaled to make the unit size 1 centimeter, painting glyphs from the same 12-unit font will generate results that are 12 centimeters high.

Section 5.1.3 "Glyph Positioning and Metrics" has some useful stuff. One thing it mentions is a FontMatrix -- this seems to be `/FontMatrix [1 0 0 1 0 0]` for the bitmap fonts in `P29.pdf`, but is `/FontMatrix [0.001 0 0 0.001 0 0 ]` for the Type 1 font (meaning that each text unit is 1000 glyph units, if I understand correctly).

> In all cases, the text-showing operators transform the displacement vector into text space and then translate text space by that amount. 


The "Td" instructions move in the user coordinate space. Note that in `simple.pdf` we had numbers like

    /F1 9.9626 Tf 91.925 710.037 Td [(one)]TJ 211.584 -654.747 Td [(1)]TJ

I think this means: from the bottom left corner i.e., (0,0), move right by 91.925 and up by 710.037, draw "one", then move right by a **further** 211.584 and down by 654.747, and draw "1".
This fits with the dimensions of the page being 612 x 792 points: moving up by about 710 (out of 792) is most of the page, similarly moving down by about 654. And 91.9 + 211.6 is about 303.5, which is about half the page.
So at least in `simple.pdf`, the movements were (1) relative, and (2) in units of points. (Also, on the size: note that 10 times 72 / 72.27 is 9.9626, so that's probably where that number comes from.)

Trying a similar `/F1 10 Tf 91.925 710.037 Td (hello world) Tj` *does* seem to work “out of the box” in P29.pdf as well, so we may not have to worry.
We just have to understand how `P29.pdf` is itself doing its positioning. That seems to be like:

    0.1 0 0 -0.1 65.2 734.6 Tm

What is this? Section 5.3 of the spec ("Text Objects") seems worth reading.

The text matrix Tm is initialized to the identity matrix during `BT`. I think it's a 3x3 matrix?

> Text space is the coordinate system in which text is shown. It is defined by the text matrix, Tm, and the text state parameters Tfs, Th, and Trise , which together determine the transformation from text space to user space.

(Here I think "user space" means "points". So the "text matrix" Tm determines (along with Tfs, Th, and Trise) what text space means in terms of points.)

The six numbers passed to `Tm` command set the Tm matrix: `a b c d e f Tm` sets the matrix to

    a b 0
	c d 0
	e f 1

More details in section 5.3.3 Text Space Details. The actual transformation from text space to device space (not user space?) is given by

            Tfs x Th     0      0
    Trm =       0       Tfs     0    x       Tm         x    CTM
                0      Trise    1

Ooh, see section 4.2.2 Common Transformations -- it's very relevant.

So anyway, `0.1 0 0 -0.1 65.2 734.6 Tm` represents a scaling by `sx = 0.1` and `sy = 0.1`, and a translation by `(65.2, 734.6)`.

So let me try:

    /F1 9.9626 Tf 65.2 734.6 Td (hello world) Tj

ooh it almost works: just a line too high. (Why?) Let me look into Trise. Nope, no luck. Let me try setting the same text matrix?

    /F1 9.9626 Tf 0.1 0 0 -0.1 65.2 734.6 Tm (hello world) Tj

is too tiny (0.1 the size?) and vertically flipped (the -0.1)? Trying

    /F1 9.9626 Tf 1 0 0 1 65.2 734.6 Tm (hello world) Tj

and now it's again 1 line too high. Well we'll live with that. If we can replace the old text and add the new, then everything being shifted up by 1 line is probably not a bad deal.

----
