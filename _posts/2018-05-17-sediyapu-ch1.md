---
layout: post
title: Sediyapu Chandogati Chapter 1
tags: [done, sanskrit]
excerpt: A “map” of Chapter 1 of this work.
date: 2018-05-17

---

Inspired/encouraged by Shatavadhani Ganesh (and more recently by Sridatta A), I’ve finally started reading Sediyapu Krishna Bhat’s work. They are right that this is a kind of work on prosody rather different from the usual texts like Vṛtta-ratnākara and others. Although I'm only on the second chapter so far, I find it quite methodical and clarifying. More on the book as a whole (and some of its interesting points) later. Anyway, I echo the statement that this work ought to be available to more people, hopefully translated into English or Sanskrit or Hindi or whatever.

It is not my place or intention to translate this work. (In a work like this, the author is very careful and precise with his language, including resorting to vague words exactly when appropriate, and translation could easily add to the confusion and distort the intention.) But at least I can make a “map” of the work, for myself to read this work again and quickly jump to relevant sections, and maybe it can be useful to other interested Kannada readers too. The start of such a thing is below.

Below are the pages from Chapter 1 of <a href="https://archive.org/details/ChandassamputaSediyapu"><i>Chandas-sampuṭa</i> by Sediyapu Krishna Bhatta</a>.

<style>
.outer-image-and-notes-container {
  display: flex;
  border: 2px solid black;
  align-items: center;
  margin-top: 2em;
  margin-bottom: 2em;
}
.inner-images {
  flex: 80;
  width: 80%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid grey;
  margin-right: 2px;
}
.inner-image {
  display: block;
}
.inner-notes {
  flex: 20;
  display: inline;
}
</style>

<div id="mainBookPages"></div>

<script>
function pageURL(pageNum, startHeightFraction, stopHeightFraction) {
    startHeightFraction = startHeightFraction || 0.0;
    stopHeightFraction = stopHeightFraction || 1.0;
    return ('https://archive.org/download/ChandassamputaSediyapu/page/n' + (Number(pageNum) + 9)
        + '_y' + startHeightFraction + '_h' + (stopHeightFraction - startHeightFraction) + '_s2.jpg');
}

function streamURL(pageNum) {
    return 'https://archive.org/stream/ChandassamputaSediyapu#page/n' + (Number(pageNum) + 9) + '/mode/1up';
}

function annotatedPageRegion(pageNum, startHeightFraction, stopHeightFraction, textNode) {
    let outerDiv = document.createElement('div');
    outerDiv.classList.add('outer-image-and-notes-container');

    let imgDiv = document.createElement('div');
    const ht = (stopHeightFraction - startHeightFraction) * (499 / 352) * 600;
    imgDiv.style.height = ht + 'px';
    imgDiv.classList.add('inner-images');

    let imgPlaceholder = document.createElement('span');
    imgPlaceholder.textContent = ('Click to load image (page ' + pageNum +
                  ' from ' + startHeightFraction +
                  ' to ' + stopHeightFraction + ')');
    imgDiv.appendChild(imgPlaceholder);
    imgDiv.addEventListener('click', () => {
        let aNode = document.createElement('a');
        aNode.href = streamURL(pageNum);
        let img = document.createElement('img');
        img.classList.add('inner-image');
        img.src = pageURL(pageNum, startHeightFraction, stopHeightFraction);
        aNode.appendChild(img);
        imgDiv.replaceChild(aNode, imgPlaceholder);
    });

    outerDiv.appendChild(imgDiv);
    let textDiv = document.createElement('div');
    textDiv.classList.add('inner-notes');
    textDiv.appendChild(textNode.cloneNode(true));
    outerDiv.appendChild(textDiv);
    document.getElementById('mainBookPages').appendChild(outerDiv);
    return outerDiv;
}

function updateCites() {
    /*
    const pToCites = new Map();
    for (var cite of document.getElementsByTagName('cite')) {
        const p = cite.parentNode;
        citesForP = pToCites.get(p) || [];
        citesForP.push(cite);
        pToCites.set(p, citesForP);
    }
    */

    for (var cite of document.getElementsByTagName('cite')) {
        const p = cite.parentNode;
        const found = cite.textContent.match(/(.*) (.*) (.*)/);
        const pageNum = found[1];
        const startHeightFraction = found[2];
        const stopHeightFraction = found[3];
        cite.style.display = 'none';
        p.parentNode.replaceChild(annotatedPageRegion(pageNum, startHeightFraction, stopHeightFraction, p), p);
    }
}
</script>

Chapter 1: The meaning of "laya" (in *various* sources).<cite>53 0.1 0.25</cite>

The term "laya" is used in many senses.<cite>53 0.24 0.505</cite>

Never defined clearly.<cite>53 0.5 0.575</cite>

Chandas and saṃgīta are inextricably linked.<cite>53 0.572 1.000</cite>

"Laya" is worth defining clearly.<cite>54 0.109 0.193</cite>

(Footnote 1 continued, footnote 2.)<cite>54 0.690 0.854</cite>

It's an old term; what do dictionaries say?<cite>54 0.190 0.403</cite>

Amarakośa<cite>54 0.403 0.688</cite>

Footnote 3: what are Āvāpa and niṣkrama?<cite>54 0.848 0.898</cite>

Amarakośa continued: "tāla" = actions taken to measure time; "laya" = the equality of these measured time intervals<cite>55 0.051 0.425</cite>

[Measured by gīta / vādya / nṛtya]<cite>55 0.425 0.754</cite>

Footnotes 4, 5, 6, 7<cite>55 0.771 0.933</cite>

layānvita (samanvita-layaḥ) (tālabaddha) = something that uniformly fits some tāla<cite>56 0.112 0.403</cite>

tāla = originally, clapping of hands (ಕೈತಟ್ಟುವಿಕೆ)<cite>56 0.377 0.833</cite>

Footnote 8: More on tāla = ಕೈತಟ್ಟುವಿಕೆ<cite>56 0.836 0.905</cite>

Footnote 8 continued<cite>57 0.591 0.838</cite>

tāla = the act of measuring out time (such as by clapping); layānvita / samanvitalaya = being able to be measured by (i.e. fitting) uniformly-spaced claps<cite>57 0.113 0.386</cite>

Footnote 9<cite>57 0.836 0.910</cite>

<- Summary<cite>57 0.383 0.587</cite>

With this, end of Kośa. Next, Nāṭyaśāstra.<cite>58 0.112 0.195</cite>

laya = equality of mātra-s (duration of utterance) of different parts of a verse. ("parts" = akṣara-puñja, chandaḥ-khaṇḍa)<cite>58 0.192 0.486</cite>

Footnotes 10 and 11<cite>58 0.484 0.647</cite>

Footnote 12<cite>58 0.645 0.909</cite>

Footnote 12 continued<cite>59 0.481 0.790</cite>

No contradiction with Amara<cite>59 0.108 0.355</cite>

The mātrākāla here is not an absolute unit of time like "1 second"; it's a relative (and arbitrary) unit and up to the speaker.<cite>59 0.354 0.480</cite>

Footnote 13: elaboration.<cite>59 0.785 0.915</cite>

Footnote 13 continued<cite>60 0.609 0.834</cite>

Same in music: can lengthen/shorten the equal units<cite>60 0.109 0.598</cite>

Footnote 14: some informal/other meanings of "laya"<cite>60 0.830 0.908</cite>

Footnote 14 continued: we become conscious of equality of events only when they end. This relates to other two meanings of “laya” (līna, and end).<cite>61 0.269 0.854</cite>

Music has laya of druta-madhya-vilambita; these don't apply to chandas.<cite>61 0.107 0.254</cite>

Footnote 15: A different "druta" and "vilambita" exist in chandas and will be discussed later.<cite>61 0.848 0.940</cite>

With words (chando-bandha) can say fast or slow; only relative time matters. Music is different.<cite>62 0.115 0.641</cite>

(Continued, see below.)<cite>62 0.638 0.878</cite>

"laya" was earlier used for equality; now used for the times themselves?<cite>63 0.107 0.331</cite>

Footnote 16: generic and particular.<cite>63 0.735 0.896</cite>

Examples of metonymy in language.<cite>63 0.325 0.721</cite>

Reconciliation of meanings.<cite>64 0.110 0.613</cite>

From above. I've repeated it here, as I yet lack a way to highlight. :-)<cite>64 0.194 0.242</cite>

More in music: pause<cite>64 0.609 0.935</cite>

Pause after tāla<cite>65 0.106 0.235</cite>

Longer duration of repeating equal pattern $\iff$ faster repetition / speech / action, so “laya” is also used for speed/tempo, too.<cite>65 0.232 0.537</cite>

Footnote 17 (example of above).<cite>65 0.835 0.906</cite>

But ideally, only when there's actually equality!<cite>65 0.511 0.832</cite>

More on the laya = tempo/speed sense, as found in śikṣā<cite>66 0.107 0.787</cite>

Start of (long) Footnote 18, on "laya" in words like "svaralaya", "śrutilaya", "tantrīlaya"<cite>66 0.761 0.949</cite>

Footnote 18 continued :-) "tantrīlaya" in Ramayana, the meaning given by commentators<cite>67 0.122 0.696</cite>

[Footnote 18 continued] But that meaning doesn't fit here; Anuṣṭup has no laya<cite>67 0.675 0.898</cite>

[Footnote 18 continued] Given the singing context in Sarga 4, "fits with music" (veena) makes more sense.<cite>68 0.135 0.397</cite>

[Footnote 18 continued] The "special" meaning given by someone does not make sense.<cite>68 0.372 0.912</cite>

[Footnote 18 concluded] No special other meaning.<cite>69 0.475 0.854</cite>

Footnote 19. Just a regular footnote :-)<cite>69 0.847 0.917</cite>

None of these "speed" meanings apply to chandas.<cite>69 0.114 0.280</cite>

Summary / reiteration<cite>69 0.263 0.471</cite>

<script>
updateCites();
</script>

And here end the pages.

--------

To summarize, what this chapter has done is define the term "laya". If I had to say it in my own words, my summary would be something like the following. *Laya* is equality of extent — *laya* is when different "units" (in the context of prosody, different "chunks" of a verse) have the same duration (as measured by various means: *tāla*). (By extension, "laya" is also the subjective experience one has of this equality; it is also the "end" or "pause" after such equal units; it is also the actual extent (duration) of those equal units; and by further extension as in music it's also the "speed" — but the fundamental meaning remains: something has "laya" when different parts of it are equal in extent.)
