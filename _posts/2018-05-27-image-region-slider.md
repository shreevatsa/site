---
layout: post
title: Archive.org book page image slider selector
excerpt: Show part of an archive.org page image
date: 2018-05-27
tags: [done, blog, software]

---

I'd like to choose a book available on the Internet Archive (archive.org), choose a page number, and show part of the page (from one vertical offset to another). To help with choose the offsets, the thing below might help.

URL of the book:
<input type="text" size="60" id="bookUrl" value="https://archive.org/details/ChandassamputaSediyapu">

Book's page number offsets (nXX = pageNumber + this):
<input type="text" size="4" id="pageNumberOffset" value="9">

Page number:
<input type="text" size="4" id="pageNumber" value="53">

<style>
.everything-wrapper {
    display: flex;
}
.slider-wrapper {
  flex-grow: 0;
  width: 12px;
  height: 800px;
}
.slider-wrapper input {
  -webkit-appearance: slider-vertical;
  width: 10px;
  height: 800px;
  margin: 4px;
}
.image-wrapper {
   flex: 4;
   background-color: lightblue;
 }
.results {
   flex: 1;
}
</style>

<div class="everything-wrapper">
<div class="slider-wrapper">
  <input type="range" step="0.1" value="100" id="slider-left">
</div>
<div class="image-wrapper">
<img id="pageImage" src="https://archive.org/download/aliceinwonderlan00carriala/page/n25_s2.jpg" height="800px">
</div>
<div class="slider-wrapper">
  <input type="range" step="0.1" value="0" id="slider-right">
</div>
<div class="results">
<p>On the left I have <span id="left-value">0.0</span> and on the right, I have <span id="right-value">100.0</span>.</p>
<p><tt>&lt;cite&gt;<span id="pageNum"></span> <span id="topFraction"></span> <span id="botFraction"></span>&lt;/cite&gt;</tt></p>
</div>
</div>
<textarea id="scratchspace" rows="3" style="width:100%"></textarea>

<script>
function realPageNumber() {
    return Number(document.getElementById('pageNumber').value) + Number(document.getElementById('pageNumberOffset').value);
    console.log("real page number: ", realPageNumber);
}
function bookId() {
    return document.getElementById('bookUrl').value.replace('https://archive.org/details/', '');
}
function updateInput() {
    let pageUrl = `https://archive.org/download/${bookId()}/page/n${realPageNumber()}_s2.jpg`;
    document.getElementById('pageImage').src = pageUrl;
    document.getElementById('slider-left').value = 100;
    document.getElementById('slider-right').value = 0;
    document.getElementById('left-value').textContent = 0.0;
    document.getElementById('right-value').textContent = 100.0;
    updateResult();
}
document.getElementById('pageNumber').addEventListener('input', updateInput);

function updateResult() {
    let top = document.getElementById('left-value').textContent;
    let bottom = document.getElementById('right-value').textContent;
    if (Number(top) > Number(bottom)) {
        [top, bottom] = [bottom, top];
    }
    const topFraction = (top / 100.0).toFixed(3);
    const botFraction = (bottom / 100.0).toFixed(3);
    const heightFraction = ((bottom - top)/100.0).toFixed(3);
    // console.assert(top <= bottom);
    let ret = `inset(${top}% 0% ${(100.0 - bottom).toFixed(2)}% 0%)`;
    // console.log('Top and bottom are ' + top + ' and ' + bottom + ' so setting clipPath to ' + ret);
    document.getElementById('pageImage').style.clipPath = ret;
    document.getElementById('pageNum').textContent = document.getElementById('pageNumber').value;
    document.getElementById('topFraction').textContent = topFraction;
    document.getElementById('botFraction').textContent = botFraction;

    document.getElementById('markdownequivalent').innerHTML = `
    [![p ${document.getElementById('pageNumber').value}](https://archive.org/download/${bookId()}/page/n${realPageNumber()}_y${topFraction}_h${heightFraction}_s2.jpg)](https://archive.org/stream/${bookId()}#page/n${realPageNumber()}/mode/1up)
    `.trim();
}
document.getElementById('slider-left').addEventListener('input', (e) => {
    document.getElementById('left-value').textContent = (100.0 - e.target.value).toFixed(2);
    updateResult();
});
document.getElementById('slider-right').addEventListener('input', (e) => {
    document.getElementById('right-value').textContent = (100.0 - e.target.value).toFixed(2);
    updateResult();
});

function stripTrailingBlankLines() {
  let s = document.getElementById('scratchspace').value;
  let last = s.length - 1;
  while (last >= 0 && s[last] == '\n') {
    --last;
  }
  s = s.substr(0, last + 1);
  document.getElementById('scratchspace').value = s;
}

document.getElementById('scratchspace').addEventListener('keyup', stripTrailingBlankLines);
document.getElementById('scratchspace').addEventListener('change', stripTrailingBlankLines);
</script>

Possible markdown:
<pre id="markdownequivalent"></pre>

Aside: On the "technology" used in this page—I'm basically new to CSS etc.—see <https://jsfiddle.net/12zhpedw/> and the following about archive.org:

- OK to hotlink: <https://archive.org/post/261115/hotlinking-allowed>
- Even documented: <https://archive.readme.io/docs/retrieving-book-pages>
- But only works if pages have been labelled (i.e. IA knows what page “page1” is). Instead, see: <https://openlibrary.org/dev/docs/bookurls>
- <https://archive.org/download/ChandassamputaSediyapu/page/n25_s2.jpg> this works! (2x downscaling)
- <https://archive.org/download/ChandassamputaSediyapu/page/n25_x280_y292_w668_h1080_s2.jpg> -- part of some page!



------
