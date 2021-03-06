// Returns a direct URL to an image region on archive.org
function pageURL(pageNum, startHeightFraction, stopHeightFraction) {
    startHeightFraction = startHeightFraction || 0.0;
    stopHeightFraction = stopHeightFraction || 1.0;
    return `https://archive.org/download/ChandassamputaSediyapu/page/n${Number(pageNum) + 9}_y${startHeightFraction}_h${stopHeightFraction - startHeightFraction}_s2.jpg`;
}

// Returns a URL for viewing page `pageNum` in the archive.org stream viewer
function streamURL(pageNum) {
    return `https://archive.org/stream/ChandassamputaSediyapu#page/n${Number(pageNum) + 9}/mode/1up`;
}

function strFrac(num) {
    // https://stackoverflow.com/a/38676273/4958
    return Number(Number(num * 100).toFixed(1)) + '%';
}

function makeImagePlaceholder(pageNum, startHeightFraction, stopHeightFraction) {
    // Don't remember where these magic numbers came from. Will have to rethink.
    const ht = (stopHeightFraction - startHeightFraction) * (499 / 352) * 600;
    const imgPlaceholder = document.createElement('div');
    imgPlaceholder.classList.add('inner-image');

    const a = document.createElement('a');
    const img = document.createElement('img');
    img.dataset.src = pageURL(pageNum, startHeightFraction, stopHeightFraction);
    img.style.height = ht + 'px';
    img.style.width = '600px';
    a.appendChild(img);
    imgPlaceholder.appendChild(a);
    const onclick = () => {
        img.src = img.dataset.src;
        clickHereDiv.style.visibility = 'hidden';
        img.addEventListener('load', () => {
            // img.style.height = 'auto';
            a.href = streamURL(pageNum);
            imgPlaceholder.removeEventListener('click', onclick);
        });
    };
    imgPlaceholder.addEventListener('click', onclick);
    const clickHereDiv = document.createElement('div');
    clickHereDiv.style.position = 'absolute';
    clickHereDiv.style.top = '50%';
    clickHereDiv.style.left = '50%';
    clickHereDiv.style.transform = 'translate(-50%, -50%)';
    clickHereDiv.style.width = '100%';
    clickHereDiv.textContent = ('Click to load image (page ' + pageNum +
        ' from ' + strFrac(startHeightFraction) +
        ' to ' + strFrac(stopHeightFraction) + ')');
    imgPlaceholder.appendChild(clickHereDiv);
    return imgPlaceholder;
}

// Creates a new div that looks like this:
// <div class="outer-image-and-notes-container">
//   <div class="inner-notes">
//      ... [textNode]
//   </div>
//   <div class="inner-images">
//     <img class="inner-image">[...]</div>
//   </div>
// </div>
function annotatedPageRegion(pageNum, startHeightFraction, stopHeightFraction, textNode) {
    let outerDiv = document.createElement('div');
    outerDiv.classList.add('outer-image-and-notes-container');

    let imgDiv = document.createElement('div');
    imgDiv.classList.add('inner-images');
    const imgPlaceholder = makeImagePlaceholder(pageNum, startHeightFraction, stopHeightFraction);
    imgDiv.appendChild(imgPlaceholder);
    outerDiv.appendChild(imgDiv);
    let textDiv = document.createElement('div');
    textDiv.classList.add('inner-notes');
    textDiv.appendChild(textNode.cloneNode(true));
    outerDiv.appendChild(textDiv);
    // document.getElementById('mainBookPages').appendChild(outerDiv);
    return outerDiv;
}

function updateCites() {
    for (var cite of document.getElementsByTagName('cite')) {
        const [, pageNum, startHeightFraction, stopHeightFraction] = cite.textContent.match(/(.*) (.*) (.*)/);
        cite.style.display = 'none';
        // If we have a <p>...<cite>...</cite></p>, then we need to turn the p into a div, etc: replace cite's parentNode with annotatedPageRegion...
        // After that, if the <p>...</p> is already inside something of class inner-notes, then we just have to append an image
        const p = cite.parentNode;
        if (p.parentNode.classList.contains('inner-notes')) {
            const images = p.parentNode.parentNode.getElementsByClassName('inner-images')[0];
            images.appendChild(makeImagePlaceholder(pageNum, startHeightFraction, stopHeightFraction));
        } else {
            p.parentNode.replaceChild(annotatedPageRegion(pageNum, startHeightFraction, stopHeightFraction, p), p);
        }
    }
}
