---
layout: post
title: Notes on the structure of PDF files
excerpt: What is inside a PDF file?
date: 2018-09-01
tags: [done]

---

PDF files are in the [Portable Document Format](https://en.wikipedia.org/wiki/PDF). It is an interesting format: a PDF file typically contains binary data, but still one can open it up in a text editor and make *some* sense of it, and there are ways of making it even more readable. There are parts that are inevitably binary blobs (images, most kinds of fonts), but the rest can be somewhat understandable.

Here we make a first attempt at understanding what PDF files (at least the ones typically produced in the ways we care about) contain.

<style>
/* Make this whole post really wide, as it uses side-by-side comments inside code blocks. */
div.wrapper {
  max-width: 90vw;
}
</style>

So: Suppose you pass the following simple file through `pdftex`:

    one
    \vfil \eject
    two
    \vfil \eject
    three
    \bye

(Here, `\vfil \eject` is a plain TeX way to force a page break.)

The resulting PDF file looks like the following. (Using `【` and `】` to denote placeholders, because `[ ... ]` and `<< ... >>` and even `{ ... }` already have special meanings inside a PDF file.) (Note I've added newlines for clarity, also deleted trailing spaces.)


    %PDF-1.5

    %【bytes: D0 D4 C5 D8】

    3 0 obj
    <<
    /Length 76
    /Filter /FlateDecode
    >>
    stream
    【 ...binary data...】
    endstream
    endobj

    9 0 obj
    <<
    /Length 82
    /Filter /FlateDecode
    >>
    stream
	【 ...binary data...】
    endstream
    endobj

    12 0 obj
    <<
    /Length 78
    /Filter /FlateDecode
    >>
    stream
	【 ...binary data...】
    endstream
    endobj

    14 0 obj
    <<
    /Length1 1504
    /Length2 9743
    /Length3 0
    /Length 10753
    /Filter /FlateDecode
    >>
    stream
    【 ...lots of binary data...】
    endstream
    endobj

    17 0 obj
    <<
    /Producer (pdfTeX-1.40.18)
    /Creator (TeX)
    /CreationDate (D:20180902152332-07'00')
    /ModDate (D:20180902152332-07'00')
    /Trapped /False
    /PTEX.Fullbanner (This is pdfTeX, Version 3.14159265-2.6-1.40.18 (TeX Live 2017) kpathsea version 6.2.3)
    >>
    endobj

    5 0 obj
    <<
    /Type /ObjStm
    /N 11
    /First 71
    /Length 561
    /Filter /FlateDecode
    >>
    stream
	【 ...binary data...】
    endstream
    endobj

    18 0 obj
    <<
    /Type /XRef
    /Index [0 19]
    /Size 19
    /W [1 2 1]
    /Root 16 0 R
    /Info 17 0 R
    /ID [<D904304F945BE94DADD3C8D38DDDC285> <D904304F945BE94DADD3C8D38DDDC285>]
    /Length 65
    /Filter /FlateDecode
    >>
    stream
	【 ...binary data...】
    endstream
    endobj

    startxref
    12291
    %%EOF

This consists of ([see the quick overview here](https://blog.didierstevens.com/2008/04/09/quickpost-about-the-physical-and-logical-structure-of-pdf-files/)) the following, modulo some inaccuracies: 

* First, the header `%PDF-1.5` which identifies the file format ("magic bytes") and version number
* Then (inside a comment) the bytes `D0 D4 C5 C8` which I'm not sure what they are. (Added later: I think they are just arbitrary binary bytes?)
* Then a few objects are defined, each of them a dictionary (`<< ... >>`):
  * object 3, object 9, object 12, object 14, which contain only binary data
  * object 17 which has some metadata (the file was produced by pdfTeX, etc)
  * object 5, which is said to have "type ObjStm" (object stream)
  * object 18, which is said to have type XRef (cross-reference stream)
* then `startxref` and something like "12291", which is probably the size of (the main area of) the file
* finally, `%%EOF` to indicate end of file.

This is quite hard to understand directly (where's the text?), even though a tool like [iText RUPS](https://github.com/itext/rups) (see [what it can do](https://developers.itextpdf.com/tutorial/itext-rups-use-rups-change-your-pdf-syntax-and-dictionaries)) can still make *some* sense of it: after [installing](https://github.com/itext/rups/releases) (last release seems to be 5.5.9 from 2016), and running with `java -jar itext-rups-5.5.9-jar-with-dependencies.jar` one gets:

![]({{ "/assets/pdf-format/RUPS-on-simple.pdf.png" | absolute_url }})

But we'd like to see it for ourselves, so let's look again. (There are some additional learning resources, [here](https://brendanzagaeski.appspot.com/0005.html), [here](https://amccormack.net/2012-01-22-anatomy-of-a-pdf-document.html), [here](http://www.planetpdf.com/developer/article.asp?ContentID=navigating_the_internal_struct), [here](https://github.com/mozilla/pdf.js/wiki/Additional-Learning-Resources), and lots of great bite-sized posts [here](https://blog.idrsolutions.com/2013/01/understanding-the-pdf-file-format-overview/) -- but I confess I haven't read any of those properly.)

The file can become easier to understand if we transform it into a more text-friendly format, by using something like `mutool clean -d simple.pdf simple-mutool.pdf` (see [this question](https://stackoverflow.com/questions/3549541/best-tool-for-inspecting-pdf-files)) and view the resulting file. I've included comments below in the right margin of the text itself, because I couldn't quickly figure out how to do it externally here in HTML:

    %PDF-1.5                                                                                                                                          % A comment, just identifies as PDF version 1.5
    %【bytes: C2 B5 C2 B6】                                                                                                                           % Another comment, not sure what these bytes are or why they changed.


    
    1 0 obj                                                                                                                                           % Object 1, referred to by Object 2
    <<                                                                                                                                                % This is a dictionary, containing two keys.
      /Font <<                                                                                                                                        % The first key, /Font, has value itself a dictionary,
        /F1 4 0 R                                                                                                                                     % which maps the name "/F1" to (a reference to) Object 4.
      >>                                                                                                                                              % End of the /Font dictionary (not Object 1 dictionary)
      /ProcSet [ /PDF /Text ]                                                                                                                         % The second key, /Procset, is an array, containing the
    >>                                                                                                                                                % ... "procedure sets"(?) used by that page.
    endobj                                                                                                                                            % Overall, this object is (we'll see) the set of "resources" used by Object 2.
    


    2 0 obj                                                                                                                                           % Object 2: another dictionary, containing 5 keys.
    <<                                                                                                                                                % Is a dictionary
      /Type /Page                                                                                                                                     % It appears that this object is of type "page"
      /Contents 3 0 R                                                                                                                                 % And the contents of the page are in Object 3.
      /Resources 1 0 R                                                                                                                                % And it uses the resources defined in Object 1 above.
      /MediaBox [ 0 0 612 792 ]                                                                                                                       % Dimensions: 612 x 792 points is 8.5 x 11 inches.
      /Parent 6 0 R                                                                                                                                   % Note that its parent is Object 6: list of all pages.
    >>                                                                                                                                                % End of dictionary.
    endobj                                                                                                                                            % End of object.


    
    3 0 obj                                                                                                                                           % Object 3, referred to by Object 2: contents of the page.
    <<                                                                                                                                                % See inside "BT" to "ET" below for the contents --
      /Length 76                                                                                                                                      % First, font /F1 at size 9.9626 is chosen (Tf)
    >>                                                                                                                                                % Then, by (91.926, 710.037) we move (Td)
    stream                                                                                                                                            % Then the text "one" is laid out (TJ)
    BT                                                                                                                                                % Then by (211.584, -654.747) we move (Td again)
    /F1 9.9626 Tf 91.925 710.037 Td [(one)]TJ 211.584 -654.747 Td [(1)]TJ                                                                             % Finally, the text "1" is laid out (TJ again)
    ET                                                                                                                                                % That concludes the text object.
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 


    
    4 0 obj                                                                                                                                           % This was referred to in Object 1's /Font (as value for /F1)
    <<                                                                                                                                                % Is a dictionary
      /Type /Font                                                                                                                                     % Type is "font"
      /Subtype /Type1                                                                                                                                 % A T1 font: https://en.wikipedia.org/w/index.php?title=PostScript_fonts&oldid=851305532#Type_1
      /BaseFont /KYJUYM+CMR10                                                                                                                         % Name of the font, basically.
      /FontDescriptor 15 0 R                                                                                                                          % The bulk of the font is defined in Object 15
      /FirstChar 49                                                                                                                                   % The font's "widths" array starts with character 49
      /LastChar 119                                                                                                                                   % And ends with character 119.
      /Widths 13 0 R                                                                                                                                  % The actual widths are in object 13.
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 
    


    6 0 obj                                                                                                                                           % Object 6, the list of all pages.
    <<                                                                                                                                                % 
      /Type /Pages                                                                                                                                    % 
      /Count 3                                                                                                                                        % There are 3 pages,
      /Kids [ 2 0 R 8 0 R 11 0 R ]                                                                                                                    % namely: Object 2, Object 8, Object 11.
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 
    


    7 0 obj                                                                                                                                           % Object 7, similar to Object 1
    <<                                                                                                                                                % ...looks like resources used by page (Object 8).
      /Font <<                                                                                                                                        % 
        /F1 4 0 R                                                                                                                                     % Note that this also uses the same font from 4 above.
      >>                                                                                                                                              % 
      /ProcSet [ /PDF /Text ]                                                                                                                         % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % This is basically identical to Object 1.


    
    8 0 obj                                                                                                                                           % Object 8, the second page
    <<                                                                                                                                                % 
      /Type /Page                                                                                                                                     % 
      /Contents 9 0 R                                                                                                                                 % The contents are in Object 9.
      /Resources 7 0 R                                                                                                                                % The resources used are in Object 7.
      /MediaBox [ 0 0 612 792 ]                                                                                                                       % Similar MediaBox
      /Parent 6 0 R                                                                                                                                   % Parent is again the list of pages.
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


    
    9 0 obj                                                                                                                                           % Object 9, the contents of second page (Object 8).
    <<                                                                                                                                                % (See below). First Font /F1 at size 9.9 is chosen (Tf)
      /Length 84                                                                                                                                      % then to (by) (91.x, 710.x) we move (Td)
    >>                                                                                                                                                % The numbers passed to the text-showing operator TJ
    stream                                                                                                                                            % are text position adjustments (move left by that much)
    BT                                                                                                                                                % (kerning basically). See page 370 Figure 5.11 in PDF 1.5 spec
    /F1 9.9626 Tf 91.925 710.037 Td [(t)28(w)28(o)]TJ 211.584 -654.747 Td [(2)]TJ                                                                     % Then we move again (Td) and show "2".
    ET                                                                                                                                                % 
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 
    


    10 0 obj                                                                                                                                          % Object 10, resources used by third page (Object 11)
    <<                                                                                                                                                % Identical to Object 1 and Object 7
      /Font <<                                                                                                                                        % 
        /F1 4 0 R                                                                                                                                     % 
      >>                                                                                                                                              % 
      /ProcSet [ /PDF /Text ]                                                                                                                         % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


    
    11 0 obj                                                                                                                                          % Object 11, the third page
    <<                                                                                                                                                % 
      /Type /Page                                                                                                                                     % 
      /Contents 12 0 R                                                                                                                                % 
      /Resources 10 0 R                                                                                                                               % 
      /MediaBox [ 0 0 612 792 ]                                                                                                                       % 
      /Parent 6 0 R                                                                                                                                   % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 
    


    12 0 obj                                                                                                                                          % Object 12, contents of third page
    <<                                                                                                                                                % Show the text "three"
      /Length 78                                                                                                                                      % 
    >>                                                                                                                                                % 
    stream                                                                                                                                            % 
    BT                                                                                                                                                % 
    /F1 9.9626 Tf 91.925 710.037 Td [(three)]TJ 211.584 -654.747 Td [(3)]TJ                                                                           % 
    ET                                                                                                                                                % 
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 


    
    13 0 obj                                                                                                                                          % Object 13 -- referred to earlier (in Object 4) as
    [ 500 500 500 500 500 500 500 500 500 277.8 277.8 277.8 777.8                                                                                     % ... the widths of the font.
      472.2 472.2 777.8 750 708.3 722.2 763.9 680.6 652.8 784.7 750                                                                                   % Array of widths (recall FirstChar 49 and LastChar 119)
      361.1 513.9 777.8 625 916.7 750 777.8 680.6 777.8 736.1 555.6                                                                                   % 
      722.2 750 750 1027.8 750 750 611.1 277.8 500 277.8 500 277.8                                                                                    % 
      277.8 500 555.6 444.4 555.6 444.4 305.6 500 555.6 277.8 305.6                                                                                   % 
      527.8 277.8 833.3 555.6 500 555.6 527.8 391.7 394.4 388.9 555.6                                                                                 % 
      527.8 722.2 ]                                                                                                                                   % 
    endobj                                                                                                                                            % 


    
    14 0 obj                                                                                                                                          % Object 14, will be referred to in Object 15 below
    <<                                                                                                                                                % Has a dictionary (this one to the left) and then a stream.
      /Length1 1504                                                                                                                                   % 
      /Length2 9743                                                                                                                                   % 
      /Length3 0                                                                                                                                      % 
      /Length 11247                                                                                                                                   % 
    >>                                                                                                                                                % 
    stream                                                                                                                                            % 
    %!PS-AdobeFont-1.0: CMR10 003.002                                                                                                                 % The stream contains the PostScript font CMR10.
    %%Title: CMR10                                                                                                                                    % 
    %Version: 003.002                                                                                                                                 % 
    %%CreationDate: Mon Jul 13 16:17:00 2009                                                                                                          % 
    %%Creator: David M. Jones                                                                                                                         % 
    %Copyright: Copyright (c) 1997, 2009 American Mathematical Society                                                                                % 
    %Copyright: (<http://www.ams.org>), with Reserved Font Name CMR10.                                                                                % 
    % This Font Software is licensed under the SIL Open Font License, Version 1.1.                                                                    % 
    % This license is in the accompanying file OFL.txt, and is also                                                                                   % 
    % available with a FAQ at: http://scripts.sil.org/OFL.                                                                                            % 
    %%EndComments                                                                                                                                     % 
    FontDirectory/CMR10 known{/CMR10 findfont dup/UniqueID known{dup                                                                                  % These look like PostScript commands...
    /UniqueID get 5000793 eq exch/FontType get 1 eq and}{pop false}ifelse                                                                             % ... define the font I guess?
    {save true}{false}ifelse}{false}ifelse                                                                                                            % 
    11 dict begin                                                                                                                                     % 
    /FontType 1 def                                                                                                                                   % 
    /FontMatrix [0.001 0 0 0.001 0 0 ]readonly def                                                                                                    % 
    /FontName /KYJUYM+CMR10 def                                                                                                                       % 
    /FontBBox {-40 -250 1009 750 }readonly def                                                                                                        % 
    /PaintType 0 def                                                                                                                                  % 
    /FontInfo 9 dict dup begin                                                                                                                        % 
    /version (003.002) readonly def                                                                                                                   % 
    /Notice (Copyright \050c\051 1997, 2009 American Mathematical Society \050<http://www.ams.org>\051, with Reserved Font Name CMR10.) readonly def  % 
    /FullName (CMR10) readonly def                                                                                                                    % 
    /FamilyName (Computer Modern) readonly def                                                                                                        % 
    /Weight (Medium) readonly def                                                                                                                     % 
    /ItalicAngle 0 def                                                                                                                                % 
    /isFixedPitch false def                                                                                                                           % 
    /UnderlinePosition -100 def                                                                                                                       % 
    /UnderlineThickness 50 def                                                                                                                        % 
    end readonly def                                                                                                                                  % 
    /Encoding 256 array                                                                                                                               % The Encoding of this font
    0 1 255 {1 index exch /.notdef put} for                                                                                                           % Note that only a few characters
    dup 101 /e put                                                                                                                                    % e, h, n, o, one (i.e. 1), r, t, 3, 2, w
    dup 104 /h put                                                                                                                                    % are encoded, at those particular positions.
    dup 110 /n put                                                                                                                                    % 
    dup 111 /o put                                                                                                                                    % 
    dup 49 /one put                                                                                                                                   % 
    dup 114 /r put                                                                                                                                    % 
    dup 116 /t put                                                                                                                                    % 
    dup 51 /three put                                                                                                                                 % 
    dup 50 /two put                                                                                                                                   % 
    dup 119 /w put                                                                                                                                    % 
    readonly def                                                                                                                                      % 
    currentdict end                                                                                                                                   % 
    currentfile eexec                                                                                                                                 % 
    【 ... lots of binary data ...】                                                                                                                    % The binary data probably contains the glyph shapes
    endstream                                                                                                                                         % Or possibly the hinting program?
    endobj                                                                                                                                            % Whatever.


    
    15 0 obj                                                                                                                                          % Object 15, was referred to in Object 4 (the font /F1)
    <<                                                                                                                                                % Defines the major things about the font etc.
      /Type /FontDescriptor                                                                                                                           % 
      /FontName /KYJUYM+CMR10                                                                                                                         % 
      /Flags 4                                                                                                                                        % 
      /FontBBox [ -40 -250 1009 750 ]                                                                                                                 % 
      /Ascent 694                                                                                                                                     % 
      /CapHeight 683                                                                                                                                  % 
      /Descent -194                                                                                                                                   % 
      /ItalicAngle 0                                                                                                                                  % 
      /StemV 69                                                                                                                                       % 
      /XHeight 431                                                                                                                                    % 
      /CharSet (/e/h/n/o/one/r/t/three/two/w)                                                                                                         % 
      /FontFile 14 0 R                                                                                                                                % And refers to the above large Object 14 as /FontFile
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


    
    16 0 obj                                                                                                                                          % Object 16, the main catalog of the PDF (root of the tree)
    <<                                                                                                                                                % Note that it has as child (refers to) Object 6 (the list of pages)
      /Type /Catalog                                                                                                                                  % 
      /Pages 6 0 R                                                                                                                                    % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 



    17 0 obj                                                                                                                                          % Object 17, looks like some metadata.
    <<                                                                                                                                                % Referred to in the trailer below...
      /Producer (pdfTeX-1.40.18)                                                                                                                      % ...as "Info" (parallel to / separate from "Root")
      /Creator (TeX)                                                                                                                                  % 
      /CreationDate (D:20180902152332-07'00')                                                                                                         % 
      /ModDate (D:20180902152332-07'00')                                                                                                              % 
      /Trapped /False                                                                                                                                 % 
      /PTEX.Fullbanner (This is pdfTeX, Version 3.14159265-2.6-1.40.18 \(TeX Live 2017\) kpathsea version 6.2.3)                                      % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


    
    xref                                                                                                                                              % Cross-reference table
    0 19                                                                                                                                              % I think it contains the byte offsets of each object
    0000000005 00256 f                                                                                                                                % 
    0000000016 00000 n                                                                                                                                % 
    0000000094 00000 n                                                                                                                                % 
    0000000211 00000 n                                                                                                                                % 
    0000000340 00000 n                                                                                                                                % 
    0000000018 00001 f                                                                                                                                % 
    0000000494 00000 n                                                                                                                                % 
    0000000573 00000 n                                                                                                                                % 
    0000000651 00000 n                                                                                                                                % 
    0000000768 00000 n                                                                                                                                % 
    0000000905 00000 n                                                                                                                                % 
    0000000984 00000 n                                                                                                                                % 
    0000001104 00000 n                                                                                                                                % 
    0000001236 00000 n                                                                                                                                % 
    0000001652 00000 n                                                                                                                                % 
    0000013001 00000 n                                                                                                                                % 
    0000013271 00000 n                                                                                                                                % 
    0000013326 00000 n                                                                                                                                % 
    0000013601 00001 f                                                                                                                                % 


    
    trailer                                                                                                                                           % Trailer, PDF reader is supposed to start here (maybe)
    <<                                                                                                                                                % 
      /Size 19                                                                                                                                        % 
      /Info 17 0 R                                                                                                                                    % 
      /Root 16 0 R                                                                                                                                    % 
      /ID [ <D904304F945BE94DADD3C8D38DDDC285> (\371&B2\2240\231\3506I\357\215\277\311\211O) ]                                                        % The backslashes you see here are literal backslashes
    >>                                                                                                                                                % 
    startxref                                                                                                                                         % 
    13601                                                                                                                                             % 
    %%EOF                                                                                                                                             % End Of File
    
Whew! Most of the file makes sense. 

It's a bit of a pain to follow around the object references, and that's what a tool like RUPS provides:

![]({{ "/assets/pdf-format/RUPS-on-simple-mutool.pdf.png" | absolute_url }})


Another option, instead of the earlier `mutool clean -d simple.pdf simple-mutool.pdf` is to use `qpdf --qdf --object-streams=disable simple.pdf simple-qpdf.pdf` — this rearranges the PDF into a standard and easy-to-edit canonical order called "QDF" ([read documentation of QDF mode here](http://qpdf.sourceforge.net/files/qpdf-manual.html#ref.qdf)), specifically designed for making the file editable in a text editor. It's mostly the same as before, except that the objects are reordered (into basically a breadth-first traversal order of the tree) and arrays are laid out on separate lines.
	
    %PDF-1.5                                                                                                                                          %
    %【bytes: BF F7 A2 AE】                                                                                                                             % I'm beginning to think these are just random bytes...
    %QDF-1.0                                                                                                                                          % Another comment, for QPDF to identify that this is in the "good" format



    %% Original object ID: 16 0                                                                                                                       % The catalog, which was 16 (towards the end), has been moved up
    1 0 obj                                                                                                                                           % ...to Object 1.
    <<                                                                                                                                                % The trailer now mentions
      /Pages 3 0 R                                                                                                                                    %       /Info 2 0 R
      /Type /Catalog                                                                                                                                  % and
    >>                                                                                                                                                %       /Root 1 0 R
    endobj                                                                                                                                            % so the root have moved up top.


    
    %% Original object ID: 17 0                                                                                                                       % The info object is now here as
    2 0 obj                                                                                                                                           % Object 2.
    <<                                                                                                                                                % 
      /CreationDate (D:20180902152332-07'00')                                                                                                         % 
      /Creator (TeX)                                                                                                                                  % 
      /ModDate (D:20180902152332-07'00')                                                                                                              % 
      /PTEX.Fullbanner (This is pdfTeX, Version 3.14159265-2.6-1.40.18 \(TeX Live 2017\) kpathsea version 6.2.3)                                      % 
      /Producer (pdfTeX-1.40.18)                                                                                                                      % 
      /Trapped /False                                                                                                                                 % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 



    %% Original object ID: 6 0                                                                                                                        % 
    3 0 obj                                                                                                                                           % Object 3 is the "Pages" object, referred
    <<                                                                                                                                                % to from Object 1 (the Catalog) above.
      /Count 3                                                                                                                                        % 
      /Kids [                                                                                                                                         % 
        4 0 R                                                                                                                                         % The three pages are Objects 4, 5, 6.
        5 0 R                                                                                                                                         % 
        6 0 R                                                                                                                                         % 
      ]                                                                                                                                               % 
      /Type /Pages                                                                                                                                    % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


        
    %% Page 1                                                                                                                                         % 
    %% Original object ID: 2 0                                                                                                                        % 
    4 0 obj                                                                                                                                           % Object 4 -- the first page.
    <<                                                                                                                                                % 
      /Contents 7 0 R                                                                                                                                 % Its contents are in Object 7.
      /MediaBox [                                                                                                                                     % 
        0                                                                                                                                             % 
        0                                                                                                                                             % 
        612                                                                                                                                           % 
        792                                                                                                                                           % 
      ]                                                                                                                                               % 
      /Parent 3 0 R                                                                                                                                   % 
      /Resources 9 0 R                                                                                                                                % Its resources are in Object 9.
      /Type /Page                                                                                                                                     % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 



    %% Page 2                                                                                                                                         % 
    %% Original object ID: 8 0                                                                                                                        %
    5 0 obj                                                                                                                                           % Object 5 -- the second page.
    <<                                                                                                                                                % 
      /Contents 10 0 R                                                                                                                                % Its contents are in Object 10.
      /MediaBox [                                                                                                                                     % 
        0                                                                                                                                             % 
        0                                                                                                                                             % 
        612                                                                                                                                           % 
        792                                                                                                                                           % 
      ]                                                                                                                                               % 
      /Parent 3 0 R                                                                                                                                   % Obviously its parent is Object 3, the list of pages.
      /Resources 12 0 R                                                                                                                               % And its resources are in Object 12.
      /Type /Page                                                                                                                                     % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 



    %% Page 3                                                                                                                                         % 
    %% Original object ID: 11 0                                                                                                                       % 
    6 0 obj                                                                                                                                           % Object 6 -- the third page.
    <<                                                                                                                                                % 
      /Contents 13 0 R                                                                                                                                % Its contents are in Object 13.
      /MediaBox [                                                                                                                                     % 
        0                                                                                                                                             % 
        0                                                                                                                                             % 
        612                                                                                                                                           % 
        792                                                                                                                                           % 
      ]                                                                                                                                               % 
      /Parent 3 0 R                                                                                                                                   % 
      /Type /Page                                                                                                                                     % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % Interestingly, it doesn't refer to resources!



    %% Contents for page 1                                                                                                                            % 
    %% Original object ID: 3 0                                                                                                                        % 
    7 0 obj                                                                                                                                           % Object 7 -- the contents of the first page.
    <<                                                                                                                                                % 
      /Length 8 0 R                                                                                                                                   % The length is Object 8??
    >>                                                                                                                                                % 
    stream                                                                                                                                            % 
    BT                                                                                                                                                % Begin Text object.
    /F1 9.9626 Tf 91.925 710.037 Td [(one)]TJ 211.584 -654.747 Td [(1)]TJ                                                                             % Choose font /F1 (Tf), move (Td), set "one" (TJ), etc.
    ET                                                                                                                                                % 
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 


    
    8 0 obj                                                                                                                                           % Object 8 -- just the number 76.
    76                                                                                                                                                % So weird!
    endobj                                                                                                                                            % 



    %% Original object ID: 1 0                                                                                                                        % 
    9 0 obj                                                                                                                                           % Object 9 -- the resources for the first page.
    <<                                                                                                                                                % 
      /Font <<                                                                                                                                        % 
        /F1 16 0 R                                                                                                                                    % The font /F1, mapped to object 16.
      >>                                                                                                                                              % 
      /ProcSet [                                                                                                                                      % And a /ProcSet containing /PDF and /Text
        /PDF                                                                                                                                          % 
        /Text                                                                                                                                         % 
      ]                                                                                                                                               % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 



    %% Contents for page 2                                                                                                                            % 
    %% Original object ID: 9 0                                                                                                                        % 
    10 0 obj                                                                                                                                          % Object 10 -- contents of the second page.
    <<                                                                                                                                                % 
      /Length 11 0 R                                                                                                                                  % 
    >>                                                                                                                                                % 
    stream                                                                                                                                            % 
    BT                                                                                                                                                % 
    /F1 9.9626 Tf 91.925 710.037 Td [(t)28(w)28(o)]TJ 211.584 -654.747 Td [(2)]TJ                                                                     % Chooses font, sets "two" with kerning.
    ET                                                                                                                                                % 
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 


        
    11 0 obj                                                                                                                                          % Object 11 -- just the number 84.
    84                                                                                                                                                % 
    endobj                                                                                                                                            % 



    %% Original object ID: 7 0                                                                                                                        % 
    12 0 obj                                                                                                                                          % Object 12: resources for the second page.
    <<                                                                                                                                                % 
      /Font <<                                                                                                                                        % 
        /F1 16 0 R                                                                                                                                    % The font /F1, again mapped to object 16.
      >>                                                                                                                                              % 
      /ProcSet [                                                                                                                                      % 
        /PDF                                                                                                                                          % 
        /Text                                                                                                                                         % 
      ]                                                                                                                                               % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


        
    %% Contents for page 3                                                                                                                            % 
    %% Original object ID: 12 0                                                                                                                       % 
    13 0 obj                                                                                                                                          % Object 13 -- recall this is contents for Page 3.
    <<                                                                                                                                                % 
      /Length 14 0 R                                                                                                                                  % 
    >>                                                                                                                                                % 
    stream                                                                                                                                            % 
    BT                                                                                                                                                % 
    /F1 9.9626 Tf 91.925 710.037 Td [(three)]TJ 211.584 -654.747 Td [(3)]TJ                                                                           % Sets the text "three"
    ET                                                                                                                                                % 
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 
    


    14 0 obj                                                                                                                                          % 
    78                                                                                                                                                % 
    endobj                                                                                                                                            % 
    


    %% Original object ID: 10 0                                                                                                                       % 
    15 0 obj                                                                                                                                          % Object 15 -- resources for Page 3 I guess...
    <<                                                                                                                                                % ... not sure why Page 3 doesn't mention it.
      /Font <<                                                                                                                                        % 
        /F1 16 0 R                                                                                                                                    % 
      >>                                                                                                                                              % 
      /ProcSet [                                                                                                                                      % 
        /PDF                                                                                                                                          % 
        /Text                                                                                                                                         % 
      ]                                                                                                                                               % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


        
    %% Original object ID: 4 0                                                                                                                        % 
    16 0 obj                                                                                                                                          % Object 16 -- recall that resources dicts mapped
    <<                                                                                                                                                % font /F1 to this Object 16
      /BaseFont /KYJUYM+CMR10                                                                                                                         % 
      /FirstChar 49                                                                                                                                   % 
      /FontDescriptor 17 0 R                                                                                                                          % FontDescriptor is in Object 17
      /LastChar 119                                                                                                                                   % 
      /Subtype /Type1                                                                                                                                 % 
      /Type /Font                                                                                                                                     % 
      /Widths 18 0 R                                                                                                                                  % and widths in Object 18
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 


        
    %% Original object ID: 15 0                                                                                                                       % 
    17 0 obj                                                                                                                                          % Object 17, the FontDescriptor
    <<                                                                                                                                                % 
      /Ascent 694                                                                                                                                     % 
      /CapHeight 683                                                                                                                                  % 
      /CharSet (/e/h/n/o/one/r/t/three/two/w)                                                                                                         % Small CharSet
      /Descent -194                                                                                                                                   % 
      /Flags 4                                                                                                                                        % 
      /FontBBox [                                                                                                                                     % 
        -40                                                                                                                                           % 
        -250                                                                                                                                          % 
        1009                                                                                                                                          % 
        750                                                                                                                                           % 
      ]                                                                                                                                               % 
      /FontFile 19 0 R                                                                                                                                % FontFile is in Object 19
      /FontName /KYJUYM+CMR10                                                                                                                         % 
      /ItalicAngle 0                                                                                                                                  % 
      /StemV 69                                                                                                                                       % 
      /Type /FontDescriptor                                                                                                                           % 
      /XHeight 431                                                                                                                                    % 
    >>                                                                                                                                                % 
    endobj                                                                                                                                            % 



    %% Original object ID: 13 0                                                                                                                       % 
    18 0 obj                                                                                                                                          % Object 18 -- the widths.
    [                                                                                                                                                 % Might these actually correspond to characters? Let's see..
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      500                                                                                                                                             % 
      277.8                                                                                                                                           % 
      277.8                                                                                                                                           % 
      277.8                                                                                                                                           % 
      777.8                                                                                                                                           % 
      472.2                                                                                                                                           % 
      472.2                                                                                                                                           % 
      777.8                                                                                                                                           % 
      750                                                                                                                                             % 
      708.3                                                                                                                                           % 
      722.2                                                                                                                                           % 
      763.9                                                                                                                                           % 
      680.6                                                                                                                                           % 
      652.8                                                                                                                                           % 
      784.7                                                                                                                                           % 
      750                                                                                                                                             % 
      361.1                                                                                                                                           % 
      513.9                                                                                                                                           % 
      777.8                                                                                                                                           % 
      625                                                                                                                                             % 
      916.7                                                                                                                                           % 
      750                                                                                                                                             % 
      777.8                                                                                                                                           % 
      680.6                                                                                                                                           % 
      777.8                                                                                                                                           % 
      736.1                                                                                                                                           % 
      555.6                                                                                                                                           % 
      722.2                                                                                                                                           % 
      750                                                                                                                                             % 
      750                                                                                                                                             % 
      1027.8                                                                                                                                          % 
      750                                                                                                                                             % 
      750                                                                                                                                             % 
      611.1                                                                                                                                           % 
      277.8                                                                                                                                           % 
      500                                                                                                                                             % 
      277.8                                                                                                                                           % 
      500                                                                                                                                             % 
      277.8                                                                                                                                           % 
      277.8                                                                                                                                           % 
      500                                                                                                                                             % 
      555.6                                                                                                                                           % 
      444.4                                                                                                                                           % 
      555.6                                                                                                                                           % 
      444.4                                                                                                                                           % 
      305.6                                                                                                                                           % 
      500                                                                                                                                             % 
      555.6                                                                                                                                           % 
      277.8                                                                                                                                           % 
      305.6                                                                                                                                           % 
      527.8                                                                                                                                           % 
      277.8                                                                                                                                           % 
      833.3                                                                                                                                           % 
      555.6                                                                                                                                           % 
      500                                                                                                                                             % 
      555.6                                                                                                                                           % 
      527.8                                                                                                                                           % 
      391.7                                                                                                                                           % 
      394.4                                                                                                                                           % 
      388.9                                                                                                                                           % 
      555.6                                                                                                                                           % 
      527.8                                                                                                                                           % 
      722.2                                                                                                                                           % 
    ]                                                                                                                                                 % 
    endobj                                                                                                                                            % 



    %% Original object ID: 14 0                                                                                                                       % 
    19 0 obj                                                                                                                                          % Object 19 -- referred to as /FontFile
    <<                                                                                                                                                % 
      /Length1 1504                                                                                                                                   % 
      /Length2 9743                                                                                                                                   % 
      /Length3 0                                                                                                                                      % 
      /Length 20 0 R                                                                                                                                  % 
    >>                                                                                                                                                % 
    stream                                                                                                                                            % 
    %!PS-AdobeFont-1.0: CMR10 003.002                                                                                                                 % 
    %%Title: CMR10                                                                                                                                    % 
    %Version: 003.002                                                                                                                                 % 
    %%CreationDate: Mon Jul 13 16:17:00 2009                                                                                                          % 
    %%Creator: David M. Jones                                                                                                                         % 
    %Copyright: Copyright (c) 1997, 2009 American Mathematical Society                                                                                % 
    %Copyright: (<http://www.ams.org>), with Reserved Font Name CMR10.                                                                                % 
    % This Font Software is licensed under the SIL Open Font License, Version 1.1.                                                                    % 
    % This license is in the accompanying file OFL.txt, and is also                                                                                   % 
    % available with a FAQ at: http://scripts.sil.org/OFL.                                                                                            % 
    %%EndComments                                                                                                                                     % 
    FontDirectory/CMR10 known{/CMR10 findfont dup/UniqueID known{dup                                                                                  % 
    /UniqueID get 5000793 eq exch/FontType get 1 eq and}{pop false}ifelse                                                                             % 
    {save true}{false}ifelse}{false}ifelse                                                                                                            % 
    11 dict begin                                                                                                                                     % 
    /FontType 1 def                                                                                                                                   % 
    /FontMatrix [0.001 0 0 0.001 0 0 ]readonly def                                                                                                    % 
    /FontName /KYJUYM+CMR10 def                                                                                                                       % 
    /FontBBox {-40 -250 1009 750 }readonly def                                                                                                        % 
    /PaintType 0 def                                                                                                                                  % 
    /FontInfo 9 dict dup begin                                                                                                                        % 
    /version (003.002) readonly def                                                                                                                   % 
    /Notice (Copyright \050c\051 1997, 2009 American Mathematical Society \050<http://www.ams.org>\051, with Reserved Font Name CMR10.) readonly def  % 
    /FullName (CMR10) readonly def                                                                                                                    % 
    /FamilyName (Computer Modern) readonly def                                                                                                        % 
    /Weight (Medium) readonly def                                                                                                                     % 
    /ItalicAngle 0 def                                                                                                                                % 
    /isFixedPitch false def                                                                                                                           % 
    /UnderlinePosition -100 def                                                                                                                       % 
    /UnderlineThickness 50 def                                                                                                                        % 
    end readonly def                                                                                                                                  % 
    /Encoding 256 array                                                                                                                               % 
    0 1 255 {1 index exch /.notdef put} for                                                                                                           % 
    dup 101 /e put                                                                                                                                    % 
    dup 104 /h put                                                                                                                                    % 
    dup 110 /n put                                                                                                                                    % 
    dup 111 /o put                                                                                                                                    % 
    dup 49 /one put                                                                                                                                   % 
    dup 114 /r put                                                                                                                                    % 
    dup 116 /t put                                                                                                                                    % 
    dup 51 /three put                                                                                                                                 % 
    dup 50 /two put                                                                                                                                   % 
    dup 119 /w put                                                                                                                                    % 
    readonly def                                                                                                                                      % 
    currentdict end                                                                                                                                   % 
    currentfile eexec                                                                                                                                 % 
	%                                                                                                                                                 % 
	【 ... lots of binary data ...】                                                                                                                  % The binary data probably contains the glyph shapes
    endstream                                                                                                                                         % 
    endobj                                                                                                                                            % 


    
    %QDF: ignore_newline                                                                                                                              % 
    20 0 obj                                                                                                                                          % Object 20 -- just a length, referred to in Object 19 above
    11247                                                                                                                                             % 
    endobj                                                                                                                                            % 


    
    xref                                                                                                                                              % The cross-reference table and trailer.
    0 21                                                                                                                                              % 
    0000000000 65535 f                                                                                                                                % 
    0000000053 00000 n                                                                                                                                % 
    0000000135 00000 n                                                                                                                                % 
    0000000436 00000 n                                                                                                                                % 
    0000000565 00000 n                                                                                                                                % 
    0000000737 00000 n                                                                                                                                % 
    0000000912 00000 n                                                                                                                                % 
    0000001099 00000 n                                                                                                                                % 
    0000001230 00000 n                                                                                                                                % 
    0000001276 00000 n                                                                                                                                % 
    0000001415 00000 n                                                                                                                                % 
    0000001556 00000 n                                                                                                                                % 
    0000001603 00000 n                                                                                                                                % 
    0000001744 00000 n                                                                                                                                % 
    0000001879 00000 n                                                                                                                                % 
    0000001927 00000 n                                                                                                                                % 
    0000002044 00000 n                                                                                                                                % 
    0000002227 00000 n                                                                                                                                % 
    0000002543 00000 n                                                                                                                                % 
    0000003117 00000 n                                                                                                                                % 
    0000014488 00000 n                                                                                                                                % 
    trailer <<                                                                                                                                        % 
      /Info 2 0 R                                                                                                                                     % 
      /Root 1 0 R                                                                                                                                     % 
      /Size 21                                                                                                                                        % 
      /ID [<d904304f945be94dadd3c8d38dddc285><1a22ae686e982716689f3f745c0e18d2>]                                                                      % 
    >>                                                                                                                                                % 
    startxref                                                                                                                                         % 
    14511                                                                                                                                             % 
    %%EOF                                                                                                                                             % 
    
The ordering of the objects here is slightly easier to follow (as objects are consistently referred to before being defined), but besides that it's the same.

What if we have multiple fonts? With the following `.tex` file:

    one {\it two}
    
    \bye

the resulting PDF file is as expected: it has

      /Font <<
        /F1 4 0 R
        /F37 5 0 R
      >>
    
and then

    /F1 9.9626 Tf 91.925 710.037 Td [(one)]TJ/F37 9.9626 Tf 18.265 0 Td [(two)]TJ/F1 9.9626 Tf 193.319 -654.747 Td [(1)]TJ

i.e. (rewritten for clarity)

    /F1 9.9626 Tf 
	91.925 710.037 Td 
	[(one)]TJ

	/F37 9.9626 Tf 
	18.265 0 Td 
	[(two)]TJ

	/F1 9.9626 Tf 
	193.319 -654.747 Td
	[(1)]TJ

etc.

In a future post, we'll look at some ancient PDFs using bitmap fonts, to understand how they work(ed).

----
