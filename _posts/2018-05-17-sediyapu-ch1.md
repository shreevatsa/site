---
layout: post
title: Sediyapu Chandogati Chapter 1
excerpt: Trying...
date: 2018-05-17

---

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
    imgPlaceholder.textContent = ('Click here to load image from archive.org (page ' + pageNum +
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
    for (var cite of document.getElementsByTagName('cite')) {
        console.log('Going over cite: ' + cite);
        const p = cite.parentNode;
        const found = cite.textContent.match(/(.*) (.*) (.*)/);
        const pageNum = found[1];
        const startHeightFraction = found[2];
        const stopHeightFraction = found[3];
        console.log('Pagenum is #' + pageNum + '# and startHeightFraction is #' + startHeightFraction + '# and stopHeightFraction is #' + stopHeightFraction + '#');
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
