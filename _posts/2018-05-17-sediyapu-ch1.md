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
    return ('https://archive.org/download/ChandassamputaSediyapu/page/n' + (pageNum + 9)
	    + '_y' + startHeightFraction + '_h' + (stopHeightFraction - startHeightFraction) + '_s2.jpg');
}
function annotatedPageRegion(pageNum, startHeightFraction, stopHeightFraction, text) {
    let outerDiv = document.createElement('div');
    outerDiv.style.border = '2px solid black';
    // outerDiv.style.overflow = 'hidden';
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
	let img = document.createElement('img');
	img.style.width = '600px';
	img.style.display = 'block';
	img.src = pageURL(pageNum, startHeightFraction, stopHeightFraction);
	imgDiv.replaceChild(img, imgPlaceholder);
    });

    outerDiv.appendChild(imgDiv);
    let textDiv = document.createElement('div');
    textDiv.style.display = 'inline';
    textDiv.style.width = (740 - 600) + 'px';
    textDiv.textContent = text;
    outerDiv.appendChild(textDiv);
    document.getElementById('mainBookPages').appendChild(outerDiv);
    // textDiv.style.height = img.offsetHeight;

}

annotatedPageRegion(53, 0.1, 0.25, 'Chapter 1: The meaning of "laya" (in various sources)');

annotatedPageRegion(53, 0.24, 0.575, 'The term "laya" is used in many senses.');
</script>

And here end the pages.
