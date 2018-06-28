---
layout: post
title: Modifying PDFs in Python with pdfrw
excerpt: Merging and deleting pages, etc. When "pdfnup" or the LaTeX package "pdfpages" aren't enough.
date: 2018-06-27
tags: [done, tools]

---

**Problem**: I have a PDF of 100 pages, which for best results needs to be viewed 2-up (that is, two pages, side by side) in one's PDF viewer.[^twopages] I'd like to instead change the PDF itself, into being a 51 page PDF (of different and uneven dimensions obviously) that contains Page 1, then Page 2–3 side-by-side, then Page 4–5, ..., then Page 98–99, and finally Page 100.

## Non-working(?) solutions

Along with a TeX distribution like TeX Live or MiKTeX, there is installed a binary called `pdfnup` which is supposed to be able to do this sort of thing. It is a wrapper around the LaTeX package `pdfpages`, which is also supposed to help with this sort of thing.

But after being unsuccessful getting the `pdfpages` package's `nup` and `fitpaper` to work together properly (and `openright` in this case, but I couldn't get them to work together regardless) — by which I mean that each combined side-by-side page should have dimensions exactly those of putting two of the original PDF's pages next to each other — I looked for other options.

## A working solution

There are (at least) two packages that help with manipulating PDFs in Python. One is `PyPDF2`, which didn't work for me for some reason I don't remember now. (I think I had trouble even installing it.) The other is `pdfrw` (see [GitHub repository](https://github.com/pmaupin/pdfrw)) which even comes with an example ([`booklet.py`](https://github.com/pmaupin/pdfrw/blob/master/examples/booklet.py)) that does almost exactly what I want. Lightly modified and simplified, here it is (put it in `booklet2.py` say):

```python
import os
import sys
from pdfrw import PdfReader, PdfWriter, PageMerge

def side_by_side_page(page_left, page_right):
    result = PageMerge() + [page_left, page_right]
    result[1].x += result[0].w  # Start second page after width of first page.
    return result.render()

def make_booklet(filename):
    """First page, pairs of pages, last page."""
    ipages = PdfReader(filename).pages
    assert len(ipages) % 2 == 0, 'Change code below if number of pages is odd.'
    opages = []
    opages.append(ipages.pop(0))
    while len(ipages) >= 2:
        opages.append(side_by_side_page(ipages.pop(0), ipages.pop(0)))
    opages.append(ipages.pop(0))
    return opages

if __name__ == '__main__':
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    opages = make_booklet(infilename)
    PdfWriter(outfilename).addpages(opages).write()
```

Run as

```
python3 booklet2.py in.pdf out.pdf
```

It worked!



[^twopages]: Viewing pages side by side, in different PDF viewers: In Preview.app, go to View → Two Pages, or hit ⌘3. In Adobe Acrobat Reader DC (yes that's its name: from Adobe Acrobat Reader to Adobe Reader back to Adobe Acrobat Reader DC), go to View → Page Display → Two Page View, and also check View → Page Display → Show Cover Page in Two Page View. In Google Chrome: give up; it doesn't have that feature.



----
