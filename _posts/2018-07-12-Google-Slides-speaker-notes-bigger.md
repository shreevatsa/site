---
layout: post
title: Making “speaker notes” bigger in Google Slides
excerpt: When presenting from Google Slides, the speaker notes are too small. Here's a fix.
date: 2018-07-12
tags: [done]

---

When presenting from Google Slides, the speaker notes are too small.[^what] Here's one way to increase the font size.

Open speaker notes, right-click and click on "Inspect", then click on "Console", and enter the following:

```javascript
function makeBigger() {
  for (let e of document.getElementsByTagName('p')) {
    e.style.fontSize = "300%";
  }
  for (let e of document.getElementsByTagName('span')) {
    e.style.fontSize = "300%";
  }
}
setInterval(makeBigger, 200);
```

What this does: every 200 milliseconds (every one-fifth of a second), it finds all "p" elements on the page, and sets their font size to "300%". Change the value to whatever you want. Here's a picture (video?) of the code in action:

![]({{ "/assets/misc/speaker-notes-bigger.gif" | absolute_url }})

----

[^what]: Note: I mean the speaker notes, not the preview of the slide being shown (or next and previous slides). The preview of the slides is also too small, and there even exists [a Chrome extension](https://chrome.google.com/webstore/detail/google-slides-auto-resize/piciggpbidhfbpefjjbomcgomanjfbeb) to make it better—though I couldn't get it to work—but this post is not about making them bigger. In fact, I strongly feel that the speaker should *not* get into the (very tempting) habit of looking at the slide being shown, because then it becomes too tempting to make the slides work as a reminder for what to say (as a prompt for the speaker, rather as something meant for the audience). See [Chris Okasaki's post on why he doesn't use PowerPoint for teaching](http://okasaki.blogspot.com/2008/01/why-i-dont-use-powerpoint-for-teaching.html). If you really need some information that is on the slides, copy it to the speaker notes. Ideally, the speaker notes should contain everything you need for speaking, and the slides should contain everything that the audience should see while you're speaking. The two are different things, and it's best to plan them separately.
