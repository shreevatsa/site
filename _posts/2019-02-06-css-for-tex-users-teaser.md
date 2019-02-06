---
layout: post
title: CSS For TeX users -- a teaser
excerpt: A universal trick for layout with CSS 
date: 2019-02-06
tags: [draft]

---

After years of struggling with CSS -- by which I mean, about once a year wanting to lay out something, trying to learn CSS layout, and achieving some partial success in the layout I wanted, after hours of frustration -- I think I've finally figured out a trick that will reduce the time to minutes.

Later I'll write a proper tutorial with context and everything, but for now here's a teaser. In short the idea is to

1. set `inline-flex` on all `div`s (because a div having outer display type of `block` is obscene: it means that while the parent container is laying out its children, this one suddenly declares not its interior but how it should be laid out relative to the other children!)

2. use appropriate hfills and vfills (boxes and glue), just as in TeX.

Here's an example. With the following CSS:

```css
* {
    box-sizing: border-box;
}
.areaofsanity {
     display: inline-flex;
     width: 100%;
     height: 60vh; 
     border: 2px solid black;
}
.areaofsanity div {
   display: inline-flex;
}
.hss { /* like \hss but also for the vertical direction. */
    flex: 1000 1000 0;
}
.vbox {
   flex-direction: column;
}
.hbox { /* redundant, use for clarity if you like */ 
   flex-direction: row;
}
.hsize {
   width: 100%;
}

.something {
    width: 30vw;
    height: 20vh;
    border: 2px solid black;
}
```

<style>
* {
    box-sizing: border-box;
}
.areaofsanity {
     display: inline-flex;
     width: 100%;
     height: 60vh; 
     border: 2px solid black;
}
.areaofsanity div {
   display: inline-flex;
}
.hss { /* like \hss but also for the vertical direction. */
    flex: 1000 1000 0;
}
.vbox {
   flex-direction: column;
}
.hbox { /* redundant, use for clarity if you like */ 
   flex-direction: row;
}
.hsize {
   width: 100%;
}

.something {
    width: 30vw;
    height: 20vh;
    border: 2px solid black;
}
</style>

and the following tree:

```html
<div class="areaofsanity">
  <div class="vbox hsize">
    <div class="hss"></div>
    <div class="hss"></div>
    <div class="hbox">
        <div class="hss"></div>
	<div class="something">This is a normal paragraph inside a div that has specified size, and is laid out 2/3rds from the top and 1/3rd from the left.</div>
	<div class="hss"></div>
	<div class="hss"></div>
    </div>
    <div class="hss"></div>
  </div>
</div>
```

we get:

<div class="areaofsanity">
  <div class="vbox hsize">
    <div class="hss"></div>
    <div class="hss"></div>
    <div class="hbox">
        <div class="hss"></div>
	<div class="something">This is a normal paragraph inside a div that has specified size, and is laid out 2/3rds from the top and 1/3rd from the left.</div>
	<div class="hss"></div>
	<div class="hss"></div>
    </div>
    <div class="hss"></div>
  </div>
</div>

How's that? :-)

More later!

----
