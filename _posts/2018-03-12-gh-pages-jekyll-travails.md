---
layout: post
title: Getting started with Jekyll for GitHub Pages
tags: [done, blog, continue]
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

## More understanding of Jekyll

(After a few days / months...) Here's yet another attempt to understand the scope of Jekyll. In a new empty directory (like `/tmp/test`), run the command that we've been using so far:

    bundle exec jekyll serve

You will get:

    Could not locate Gemfile or .bundle/ directory

So create a `Gemfile` file, with the contents being what we've seen so far:

    source "https://rubygems.org"
    gem "github-pages", group: :jekyll_plugins

And run `bundle exec jekyll serve` again. Observed behaviour: A file `Gemfile.lock` and a directory `_site` are created, and a web server comes up at http://127.0.0.1:4000/ serving the contents of `_site` directory (`assets/css/` and `assets/javascript/`, probably coming from the `github-pages` gem).

Next, add some files to the current directory -- `.pdf`, `.png`, or whatever, even `.html` (anything except `.md` files).  Also, some directories. Now, when you run `bundle exec jekyll serve`, note that all these are copied into the `_site` directory. So what `bundle exec jekyll serve` does is like `python2 -m SimpleHTTPServer` or `python3 -m http.server`: serves the current directory as a http server, with the added wrinkle of copying everytihng over to a separate `_site` directory.

Finally, add a `.md` file and try again. Then you get:

    fatal: not a git repository (or any of the parent directories): .git
       GitHub Metadata: Error processing value 'title':
      Liquid Exception: No repo name found. Specify using PAGES_REPO_NWO environment variables, 'repository' in your configuration, or set up an 'origin' git remote pointing to your github.com repository. in /_layouts/default.html
                 ERROR: YOUR SITE COULD NOT BE BUILT:
                        ------------------------------------
                        No repo name found. Specify using PAGES_REPO_NWO environment variables, 'repository' in your configuration, or set up an 'origin' git remote pointing to your github.com repository.

This shows another (main) job of jekyll: to generate `.html` files for going into `_site`, from `.md` files. And with `github-pages` in the `Gemfile`, it seems to talk to GitHub. If we carry out these same steps from a clone of a repository hosted on GitHub (in an empty directory within the repo, create a `Gemfile` as above, and add some files including a`.md` file), we get the `_site` generated successfully with `.html` file corresponding to the `.md` file, and even a copy of the `.md` file itself. There's a warning though:

       GitHub Metadata: No GitHub API authentication could be found. Some fields may be missing or have incorrect data.

For this, [the internet](https://github.com/github/pages-gem/issues/399) suggests one should create a `_config.yml` and add:

    github: [metadata]

to it. (E.g. run `echo "github: [metadata]" >> _config.yml` in the directory.) But this didn't work for me; I had to follow [this](https://github.com/github/pages-gem/issues/399#issuecomment-361091215): generate a token at https://github.com/settings/tokens and `export JEKYLL_GITHUB_TOKEN=...`.


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

* Having the actual categories and tags (from the metadata in "YAML frontmatter") show up on the page: something like
  {%raw%}
  ```
  Categories: {{ page.categories | join: ', ' }}

  Tags: {{ page.tags | join: ', ' }}
  ```
  {%endraw%}

## Yet to figure out:

* Images? Links to other posts?

----

Some other blogs I've seen recently, interesting for either their content or look/theme/features, that maybe I can use as examples (not all are hosted on GitHub Pages though): [danluu](http://danluu.com/), [wesleyac](http://blog.wesleyac.com/) ([code](https://github.com/WesleyAC/blog)), [hillelwayne](https://www.hillelwayne.com/), [mzucker](https://mzucker.github.io/) ([code](https://github.com/mzucker/mzucker.github.io)), [haixing-hu](http://haixing-hu.github.io/), [leemendelowitz](https://leemendelowitz.github.io/blog/how-does-python-find-packages.html) (Disqus), [DeBroglie](https://boristhebrave.github.io/DeBroglie/) (is this even Jekyll? Probably not), [jakevdp](http://jakevdp.github.io/blog/2018/09/13/waiting-time-paradox/), [Diogocastro](https://diogocastro.com/blog/2018/06/17/typeclasses-in-perspective/) (GitHub for comments! And all 3 posts are great too).

----
