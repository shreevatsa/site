---
layout: post
title: Sediyapu Chandogati Chapter 1
excerpt: A “map” of Chapter 1 of this work.
date: 2018-05-17

---

Inspired/encouraged by Shatavadhani Ganesh (and more recently by Sridatta A), I’ve finally started reading Sediyapu Krishna Bhat’s work. They are right that this is a kind of work on prosody rather different from the usual texts like Vṛtta-ratnākara and others. Although I'm only on the second chapter so far, I find it quite methodical and clarifying. More on the book as a whole (and some of its interesting points) later. Anyway, I agree that this work ought to be available to more people, hopefully translated into English or Sanskrit or Hindi or whatever.

It is not my place or intention to translate this work. (In a work like this, the author is very careful and precise with his language, including resorting to vague words exactly when appropriate, and translation could easily add to the confusion and distort the intention.) But at least I can make a “map” of the work, for myself to read this work again and quickly jump to relevant sections, and maybe it can be useful to other interested Kannada readers too. The start of such a thing is below.

Below are the pages from <a href="https://archive.org/details/ChandassamputaSediyapu"><i>Chandas-sampuṭa</i> by Sediyapu Krishna Bhatta</a>.

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
    outerDiv.style.border = '2px solid black';
    outerDiv.style.display = 'flex';
    outerDiv.style.alignItems = 'center';

    let imgDiv = document.createElement('div');
    imgDiv.style.width = '600px';
    const ht = (stopHeightFraction - startHeightFraction) * (499 / 352) * 600;
    imgDiv.style.height = ht + 'px';
    imgDiv.style.display = 'flex';
    imgDiv.style.alignItems = 'center'; // center vertically
    imgDiv.style.justifyContent = 'center'; // center horizontally

    let imgPlaceholder = document.createElement('span');
    imgPlaceholder.textContent = ('Click here to load image (page ' + pageNum +
                  ' from ' + startHeightFraction +
                  ' to ' + stopHeightFraction + ')');
    imgDiv.appendChild(imgPlaceholder);
    imgDiv.addEventListener('click', () => {
        let aNode = document.createElement('a');
        aNode.href = streamURL(pageNum);
        let img = document.createElement('img');
        img.style.width = '600px';
        img.style.display = 'block';
        img.src = pageURL(pageNum, startHeightFraction, stopHeightFraction);
        aNode.appendChild(img);
        imgDiv.replaceChild(aNode, imgPlaceholder);
    });

    outerDiv.appendChild(imgDiv);
    let textDiv = document.createElement('div');
    textDiv.style.display = 'inline';
    textDiv.style.width = (740 - 600) + 'px';
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

The term "laya" is used in many senses.<cite>53 0.24 0.575</cite>

<script>
updateCites();
</script>

And here end the pages.

--------

Aside: On the "technology" used in this page—I'm basically new to CSS etc.—see <https://jsfiddle.net/op9srymy/> and the following about archive.org:

- OK to hotlink: <https://archive.org/post/261115/hotlinking-allowed>
- Even documented: <https://archive.readme.io/docs/retrieving-book-pages>
- But only works if pages have been labelled (i.e. IA knows what page “page1” is). Instead, see: <https://openlibrary.org/dev/docs/bookurls>
- <https://archive.org/download/ChandassamputaSediyapu/page/n25_s2.jpg> this works! (2x downscaling)
- <https://archive.org/download/ChandassamputaSediyapu/page/n25_x280_y292_w668_h1080_s2.jpg> -- part of some page!
