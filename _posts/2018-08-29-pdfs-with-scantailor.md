---
layout: post
title: Processing PDFs with ScanTailor
excerpt: Working with book scans
---

[Scan Tailor](http://scantailor.org/) is a great program for working with scanned images (of books). It deals with the common problems one has with scans: they may be tilted, they may be warped (e.g. curve towards the middle of the book), etc.

Sometimes, a PDF is made up of scanned images. (As opposed to being made up of characters laid out on the page.) In such cases, it is an attractive idea to “disassemble” the PDF into images, process them with ScanTailor, and re-assemble into a better PDF (or some other format).

## Installing ScanTailor

The ScanTailor project has not seen updates in the last few years, so this was quite hard,[^update] at least on macOS. I later came to know (from some posts on diybookscanner.org) that there are forks of ScanTailor which have more features and/or may have better updates, but I didn't know it at the time. I used [these instructions](https://github.com/scantailor/scantailor/issues/273#issuecomment-357964331) to install (not a direct quote):

> First, run
>
> ```sh
> git clone https://github.com/Homebrew/homebrew-boneyard
> cd homebrew-boneyard
> git checkout f0f4e12197
> ```
> Then edit `homebrew-boneyard/scantailor.rb` to change the line `depends_on "qt"` to `depends_on "cartr/qt4/qt@4"`. Finally run:
>
> ```sh
> brew tap cartr/qt4
> brew tap-pin cartr/qt4
> brew install qt@4
> brew install scantailor.rb
> scantailor
> ```

(Actually those instructions didn't quite work for me directly, but I was able to figure out from there...)

## Extracting images from PDF

### From rendering

There are many ways to do it. For example (from [here](https://christianheilmann.com/2012/09/30/quick-one-converting-a-multi-page-pdf-to-a-jpg-for-each-page-on-osx/)) one can “render” each PDF page, and write out the pixels:

```sh
gs -dNOPAUSE -sDEVICE=jpeg -r144 -sOutputFile=p%03d.jpg file.pdf
```

or

```sh
gs -dNOPAUSE -sDEVICE=pngalpha -r1260 -sOutputFile=p%03d.jpg myPDFfile.pdf
```

This will work regardless of whether the PDF is made of scanned images or not. The problem is that this “resamples” — e.g. if the PDF contains images at a certain resolution, the output of this is the outcome of rendering the page at (probably) a different resolution.

### Directly

If the PDF really contains images, then we should be able to get the images directly out of the PDF stream. (I vaguely remember once doing it by just opening the PDF in Emacs and copy-pasting the relevant binary sections into new files...)

There are some relevant questions on Stack Overflow: See [Extract images from PDF without resampling, in python?](https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python) and linked questions.

(There are also questions about PDF structure in general: see [inspecting PDF files](https://stackoverflow.com/questions/3549541/best-tool-for-inspecting-pdf-files) and [Convert PDF to a tree](https://stackoverflow.com/questions/43323751/convert-pdf-to-a-tree).)

Anyway, I ended up using `pdfimages` from the Poppler library. For example:

```sh
pdfimages -f 1 -l 230 -png myPDFfile.pdf someFooPrefix
```

or

```sh
pdfimages -all -f 1 -l 84 myPDFfile.pdf someFooPrefix
```

## Using ScanTailor

Once you have the images extracted in whatever way, you can use either the ScanTailor GUI or `scantailor-cli` (I've had better results with the GUI, because there are things you don't realize until you see the output).

### Assembling images

I want pages laid out 2x2 on each page (to save paper), for which I can use, for example, [`montage` from ImageMagick](http://www.imagemagick.org/Usage/montage/):

```sh
montage extr-007.tif extr-008.tif extr-009.tif extr-010.tif -geometry +1+1 montage.png
```

For example (the multiple variable assignment in the `for` loop requires Zsh I think):

```sh
for a b c d in {005..088}; do echo "$a and $b and $c and $d"; montage extr-$a.tif extr-$b.tif extr-$c.tif extr-$d.tif -geometry +1+1 montage-$a.png; done
```

### Converting to PDF

ImageMagick can do that too:

```sh
convert montage-0* together.pdf
```

That's it!

[^update]: It is unfortunate that we live in a world where already-working software needs to keep getting updated, just to keep working. It's because most software has many dependencies (other libraries, at least the operating system), and those keep getting updated. That's one reason it's good to minimize dependencies.





----
