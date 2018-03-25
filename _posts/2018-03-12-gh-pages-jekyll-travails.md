---
layout: post
title: Getting started with Jekyll for GitHub Pages
tags: [blog]
excerpt: My attempts trying to read and understand documentation, to set up this blog.
date: 2018-03-12
---

By the end of this post, I'll hopefully have set up a blog on GitHub Pages, using Jekyll.

## What is a static site generator / why use Jekyll?

Suppose you wanted to make a static website—a bunch of HTML pages. You could do this by writing each HTML page manually. I've tried that in fact, and it's not impossible. But soon you run into a few annoyances.

Firstly, writing valid HTML by hand (opening and closing tags, indicating paragraphs with `<p> … </p>` instead of just a blank line) is a bit cumbersome and annoying. This could be solved by writing your input in an easier-to-type markup like Markdown or [org-mode](https://orgmode.org/) or (if you prefer) LaTeX, and using a Markdown-to-HTML (or whatever) converter. For this approach, an excellent tool is [pandoc](https://pandoc.org/).

Secondly, you'd probably like to have a common header, footer, CSS styles, or something like that, common to all or many pages. We could implement this ourselves too, with some simple scripts (or the right options to the tools mentioned previously), but soon we'll want to add templating, some way of tagging individual pages, etc. This, along with the previous problem, is a big part of what a static site generator does for you:

> Jekyll makes it easy to create site-wide headers and footers without having to copy them across every page. It also offers advanced templating features, … (from [here](https://help.github.com/articles/about-github-pages-and-jekyll/))

IMO this second reason is still not a convincing one to use static site generators (or rather, to use an existing one rather than essentially writing your own), but it's useful.

Finally, if you're keeping the files in version control (on GitHub), it may be preferable to check in only the version in the markup you typed, rather than the generated HTML. As GitHub Pages supports only Jekyll natively, this suggests using Jekyll.

(Overall, I think the rationale for using this is still somewhat weak, but….)

## Where are the docs?

There are some on [help.github.com](https://help.github.com/), namely under [GitHub Pages Basics](https://help.github.com/categories/github-pages-basics/) and under [Customizing GitHub Pages](https://help.github.com/categories/customizing-github-pages/). (Linked-to from [pages.github.com](https://pages.github.com/).)

There's a bit of a switcheroo going on: on the one hand, the GitHub Pages documentation says that it supports Jekyll, etc; there's even an entire section on Jekyll. On the other hand, most of the documentation on GitHub is chiefly about how you can just put the individual html files (e.g. `index.html`) into your repo, and those files get served on GitHub Pages (which makes sense).

In the first set of docs (under “GitHub Pages Basics”), the main thing documented is that if you have a GitHub repository named `username.github.io`, then it will be served at `https://username.github.io`, and if you have a GitHub repository named anything else (say `projectname`) then it will be served at `https://username.github.io/projectname`. Which raises the natural question: what if you have both? (The answer [here](https://github.com/isaacs/github/issues/547#issuecomment-220288687) suggests that it may work… should give it a try.)

So how do you actually get started with Jekyll? Seems to be [here](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/#step-3-optional-generate-jekyll-site-files): the

```
bundle exec jekyll _3.3.0_ new NEW-JEKYLL-SITE-REPOSITORY-NAME
```

command. This will create the files needed (the `_config.yml`, the `Gemfile`, the `index.md` file and the `_posts` directory, etc).

## What I understand so far

If I understand correctly, this is how you use Jekyll:

* Pick a “theme”
* Initialize a new Jekyll site (for that theme?), to auto-generate certain files
* Follow the theme's instructions to know what files you need to edit where

Something slightly different is indicated in the Jekyll documentation, e.g. starting at [the Jekyll quickstart](https://jekyllrb.com/docs/quickstart/). We need to do either:

* `jekyll new myblog --blank` to start absolutely blankly (which seems to be equivalent to `touch index.html; mkdir _drafts _layouts _posts`)
* `jekyll new myblog` which does a lot more (creates a rather long `Gemfile` and `_config.yml` for instance) — for the theme “Minima”, with some further options.

The funny thing is that the [documentation on GitHub](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/#step-3-optional-generate-jekyll-site-files) suggests that the *real* way to use Jekyll, and what most people do, is copy-paste from an existing Jekyll site:

> You may already have Jekyll site files on your local computer if you cloned a Jekyll site repository. If you don't have a Jekyll site downloaded, you can generate Jekyll site files for a basic Jekyll template site in your local repository.
>
> If you want to use an existing Jekyll site repository on GitHub as the starting template for your Jekyll site, fork and clone the Jekyll site repository on GitHub to your local computer. For more information, see "[Fork a repo](https://help.github.com/articles/fork-a-repo/)."

Anyway, if instead we want to do the equivalent of the `jekyll new myblog` mentioned earlier, the GitHub-documented command is to, from within the repo, do:

```sh
bundle exec jekyll _3.3.0_ new . --force
```

At this point, I must say the whole thing is bonkers. For example, I had to add

```
github: [metadata]
```

to my `_config.yml` at some point. For another example, the default theme (Minima) references a “post” and a “home” layout. But guess what, *none* of the other supported themes have these layouts, so you cannot really switch to any other, or at least it's not documented how. (See also the end of [this comment](https://github.com/github/pages-gem/issues/416#issuecomment-337052107): there's no consistency between themes.)

## Really, what is Jekyll?

Ok, let's make another attempt to understand. Of the magic that Jekyll does with a default(Minima)-themed site, some of it must be coming from the theme (e.g. the styling probably comes from the theme), and some from Jekyll itself. What exactly does Jekyll do?

From within the site(?) directory created as mentioned above, running `bundle show minima` shows where the theme is, and looking at those files gives some insight:

```sh
find $(bundle show minima) -type f | xargs less
```

(See especially `README.md`)

What an examination of these files shows is that there is really not much in the theme. It's Jekyll itself that takes care of all stuff like converting `.md` to `.html` files according to the specified `layout`, and it has some pretty powerful templating system. So we don't need to worry too much right now about picking the right theme; it should be possible to get the “features” of other themes by seeing how they are implemented (and these implementations are reasonably small), and copying them over.

Having finally understood this, we can start with the default Minima theme, and extend it as necessary.

## How to get started (really)

Now that we know (roughly) what Jekyll does, what the theme does, etc., here's a fresh guide to getting started. (Based on [GitHub documentation](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/).)

1. Create a new repo on GitHub and `cd` into it, or `cd` into an existing repo

2. Make sure everything is saved / backed up. Delete `Gemfile` and `Gemfile.lock`, unless you understand what they are and are sure you need them.

3. In the root directory of the repo, add these two lines to a file called Gemfile:

   ```
   source 'https://rubygems.org'
   gem 'github-pages', group: :jekyll_plugins
   ```

4. Type `bundle install`, to install Jekyll and everything else that GitHub pages assumes.

5. Run `bundle exec jekyll new . --force` to generate the default files for the default Jekyll theme.

6. Once again delete `Gemfile` and `Gemfile.lock`, and restore `Gemfile` as in Step 3.

7. Start writing posts in `_posts`

8. Run `bundle exec jekyll serve` to check that everything works.

9. Commit all these files.

10. To customize stuff, the recommended way (in the Jekyll / Minima documentation) is to copy the theme's files into the repo, and edit them. For example, copy the file `$(bundle show minima)/_layouts/home.html` to edit the “home” layout.


## Some improvements

Here are a few I made:

* Change permalink format to not include the annoying date: put the following in `_config.yml`:

  ```yaml
  permalink: ":slug:output_ext"
  ```

* Change the date format to look like "2018 Mar 8": put the following in `_config.yml ` (see [here](https://github.com/jekyll/minima/issues/69) and [here](http://shopify.github.io/liquid/filters/date/)):

  ```yaml
  minima:
      date_format: "%Y %b %e"
  ```

* Something needed to just get it to work: need to set `baseurl` in `config.yml` (see e.g. [point 4 here](https://ilovesymposia.com/2015/01/04/some-things-i-learned-while-building-a-site-on-github-pages/))

* MathJax: added JavaScript to `default.html`

* “n-minute read”: use something like {%raw%}`{{ post.content | number_of_words | divided_by: 250 | plus: 2}}`{%endraw%} to get a number.

* Yet to figure out: Images? Links to other posts?



* Other good blogs I've seen recently, that I can use as examples: [danluu](http://danluu.com/), [wesleyac](http://blog.wesleyac.com/) ([code](https://github.com/WesleyAC/blog)), [hillelwayne](https://www.hillelwayne.com/), [mzucker](https://mzucker.github.io/) ([code](https://github.com/mzucker/mzucker.github.io)), [haixing-hu](http://haixing-hu.github.io/),

----
