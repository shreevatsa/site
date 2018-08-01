---
layout: post
title: Taking a look at Sanscript
excerpt: An examination of the Sanscript library for Sanskrit transliteration
date: 2018-07-17
tags: [draft]

---

As I'd like to resume working on the [Sanskrit metres](https://sanskritmetres.appspot.com/) site, one of the things I'd like to improve is the input interface. Specifically, I'd like to make it so that as you type, you will see what your input will be read as, with errors and potential pitfalls highlighted. So far I've used my own transliteration code in the (Python) backend, but should probably move to something in the frontend (JavaScript). So I started looking at Sanscript, to understand how it works and whether it can be adapted/extended to serve my purposes.

## Where to look at Sanscript?

Doing a Google Search for `sanscript`, and looking at other places, gives a few options:

* The web page <http://www.learnsanskrit.org/tools/sanscript> — This is the online interface. From the perspective of the transliteration library, a demo page. It uses a [minified file](http://www.learnsanskrit.org/scripts/sanscript.js), and [the link to the unminified version](http://www.learnsanskrit.org/scripts/sanscript_full.js) does not work.
* The GitHub repo `sanskrit/sanscript` <https://github.com/sanskrit/sanscript> — this links to [sanscript.js at an older version](https://github.com/sanskrit/sanscript.js/tree/3e109b09d0e69de1afb166ebd4d1ffb4e340a0c3) ([raw sanscript.js file](https://raw.githubusercontent.com/sanskrit/sanscript.js/3e109b09d0e69de1afb166ebd4d1ffb4e340a0c3/sanscript/sanscript.js))
* The GitHub repo `sanskrit/sanscript.js` <https://github.com/sanskrit/sanscript.js> ([raw](https://raw.githubusercontent.com/sanskrit/sanscript.js/master/sanscript/sanscript.js))
* [sanscript on npm](https://www.npmjs.com/package/sanscript) (use `npm v sanscript dist.tarball ` to get the link, namely https://registry.npmjs.org/sanscript/-/sanscript-0.0.2.tgz, then download and look.)
* Forks of the GitHub repo, e.g. [Shreeshrii/sanscript.js](https://github.com/Shreeshrii/sanscript.js/).
* Sites that are using it, e.g. [Ollett's web text of *Mālatīmādhava*](http://prakrit.info/mama/) uses [this older (I think) version](http://prakrit.info/mama/js/sanscript.js)

Anyway, whichever one you look at, the differences are not too large, so might as well pick one: say [the one from the GitHub repo](https://github.com/sanskrit/sanscript.js/blob/master/sanscript/sanscript.js).

(Later we can look at other libraries like [Salita](https://github.com/mbykov/salita): see [this thread](https://groups.google.com/d/topic/sanskrit-programmers/iDHAtIZPA2k). Also these: [1](https://github.com/sanskrit-coders/indic_transliteration), [2](https://github.com/sanskrit-coders/indic-transliteration), [3](https://github.com/sanskrit-coders/indic-transliteration#libraries-in-other-languages).)

## First impressions

There's something I must say about Sanscript, even before looking at it: the name is genius! Unbeatably catchy, and like “*amantrayam akṣaro nāsti*”, has given a useful meaning to a confused misspelling. The name itself guarantees that this should be the most used Sanskrit transliteration tool.

On looking at Sanscript, the first thing one is struck by is that the documentation (the GitHub repo's readme, also reproduced on the npm page) is excellent. It is crisp and concise, and gives the main things one may want to know in order to use it. Similarly, the interface that it provides to the user (programmer) is also great: the main thing it provides is a `Sanscript.t(data, from, to, options)` function, e.g. `Sanscript.t("satyam brUyAt", "hk", "devanagari")`.

The code is well-documented (the comments are exactly as long as they should be), with well-chosen terminology (e.g. "scheme" for either an Indic script or a transliteration method), and is organized well: all the “data” first, then the transliteration utils. The actual code for transliteration is quite short.

## Details

Some things that are notable, or could be different:

### Data and code

The `sanscript.js` file contains both “data” (the details of the different schemes) and “code”. These could probably be separate, e.g. in the history I see attempts to move the representation from something more code-heavy (`vowels: "a A i I".split(" ")`) to something representable in JSON (`"vowels": ["a", "A", "i", "I"]`) but still present in the `.js` file.

In principle, the data we care about is fundamentally tabular, i.e. correspondence between different schemes is by characters having the same positions in the lists for different schemes. I wonder if some sort of TSV or "spreadsheet" organization may help. For example, we could have a row for each scheme, and the columns could be things like "vowel A", "consonant k" etc.

Maybe the data is in fact two-fold: grapheme → phoneme, and phoneme → grapheme. This is a good way to think about cases like ITRANS (different graphemes can map to same phoneme), and Tamil (the phoneme → sgrapheme is lossy, and grapheme → phoneme is context-sensitive).

In fact, abstractly what is transliteration? What does it mean to say that, for instance, “kazcit yakSaH” (HK) and “कश्चित् यक्षः” (Devanagari) are the same, or should be transliterated to each other? The interpretation it seems to me is that both are surface realizations of the same underlying/deeper “something”.

This "something" is, to a first approximation, phonemes: both “kazcit yakSaH” and “कश्चित् यक्षः” encode the sequence of phonemes:

* consonant sound [velar (*kaṇṭhya*) unaspirated (*alpaprāṇa*) voiced], or simply consonant sound “k”.
* vowel sound “a”
* consonant sound “ś”
* consonant sound “c”
* vowel sound “i”
* consonant sound “t”
* consonant sound “y”
* vowel sound “a”
* consonant sound “k”
* consonant sound “ṣ”
* vowel sound “a”
* visarga

(Note that there are special rules for mapping phonemes ↔︎ graphemes for Brahmic scripts (implicit vowel and vowel marks, virāma, etc), while the mapping is a bit more transparent for most Roman schemes. There too, we may have things like a generic rule for *mahāprāṇa* consonants containing a “h”.)

But although this is an approximation, this is not quite it: from purely the phonemes, what we would get is “kazcityakSaH” or “कश्चित्यक्षः” — but we want to have the whitespace as well. So the “deeper” or “underlying” thing we have should actually be a combination of phonemes and graphemes (spaces, punctuation, and unrecognized characters). That is, our list above should contain, between “consonant sound t” and “consonant sound y”, something like “the character ‘ ’ (space)”. Thus the “type” of the elements in the list is a mixed one: neither purely phonemic, nor purely graphemic.

At this point, we have custom script-specific rules for how to map the graphemes (or actually, Unicode codepoints) of a particular script, to phonemes (and vice-versa). But we can go further: as the rules for going from grapheme to phoneme (or vice-versa) are common across various Indic scripts, we could abstract that out. So for example we could turn Devanagari “कश्चित् यक्षः” into the list:

* Brahmic consonant letter “ka”
* Brahmic consonant letter “śa”
* Brahmic virama
* Brahmic consonant letter “ca”
* Brahmic vowel mark “i”
* Brahmic consonant letter “ta”
* Brahmic virama
* the character ‘ ’ (space)
* Brahmic consonant letter “ya”
* Brahmic consonant letter “ka”
* Brahmic virama
* Brahmic consonant letter “ṣa”
* Brahmic visarga

And it’s obvious both how to go from  “कश्चित् यक्षः” to the above list, and from the above list to the list of grapho-phonemes. And vice-versa. And if we wanted to transliterate into another Brahmic script, we could proceed directly (transliterating vowel sign to vowel sign, etc), without going through the grapho-phonetic layer. Only when transliterating to a Roman scheme would we need to go all the way there.

This seems to make sense to me right now, but we need to examine the data (of all the various scripts/schemes) to see if this really makes sense. (It might be that each has some differences... e.g. the Tamil model needs quite a bit of special treatment, perhaps enough to treat it as an altogether separate model from Brahmic schemes.)

**TODO**: Compile all the data on the different scripts, in a clear (tabular?) format. Sets of columns can have common headers (“vowel signs”, “numerals” etc). Relevant reading:

* Scharf and Hyman, Linguistic Issues in Encoding Sanskrit (I should probably read and summarize this book anyway),
* The Unicode Standard

Incidentally, the latter says (Section 6.1, “writing systems”):

> Because of legacy practice, three distinct approaches have been taken in the Unicode Standard for the encoding of abugidas: the Devanagari model, the Tibetan model, and the Thai model. The Devanagari model, used for most abugidas, encodes an explicit virama character and represents text in its logical order. The Thai model departs from the Devanagari model in that it represents text in its visual display order, based on the typewriter legacy, rather than in logical order. The Tibetan model avoids an explicit virama, instead encoding a sequence of subjoined consonants to represent consonants occurring in clusters in a syllable.

There does not seem to be a list of all the scripts whose Unicode encoding follows the “Devanagari model”.

Anyway, this has been a long digression inspired by looking at just one part of the Sanscript source code: its script data. Let’s continue looking at the source code, for a few more things: the `skip_sgml` option (what should the API be, and also consider what should happen inside `<script>...</script>`), the `syncope` option (where should this be handled), and of course the actual transliteration code.

(Before that I should probably compile the actual data into a table first...)




----
