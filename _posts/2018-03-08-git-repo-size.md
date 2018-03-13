---
layout: post
title: "Why is my Git repo so large?"
tags: [git, done]
excerpt: A script for seeing what exactly takes up space inside a Git repository itself.
date: 2018-03-08
---

Why does my Git repository take up so much space?

A while ago, I became curious about a particularly large Git repository I was working with. From my first encounter with that repo, I was surprised and frustrated to find how long many operations took (e.g. the initial `git clone`), some because of the size. I suspected that the large size was because of (1) some binary files being checked in to the repo (which seems like something that one should never do, but happens), and (2) the accumulated history of certain files that were frequently checked-in, e.g. a large one that was auto-generated and committed every few hours, with lots of changes. So I started trying to look into it.

If you look inside your `.git` directory, the bulk of the space is probably taken by the `.objects` directory.[^LFS] What is inside it?

Here is a script that may help you discover which files, aggregated over their entire history, contribute the most to the size of your repository. I'm also trying out, if not exactly “literate programming”, then at least “Explaining code for publication”, so that I'll be able to understand this script again.

[^LFS]: Maybe not if you're using Git Large File Storage (LFS), but then the space used inside the `.git/lfs` is easier to explain: everything there simply is some (version of some) file stored using LFS. You can use `file` to see the type of the file, then open with corresponding application.

(Skip straight to the [script](#program), or see [example usage](#example-usage).)

## Background: objects and packfiles

A Git repository contains objects. (For a great introduction to Git, see [*Git from the Bottom Up* by John Wiegley](https://jwiegley.github.io/git-from-the-bottom-up/).)

### What are objects?

An object is one of {blob, tree, commit, tag}.

- A blob contains the contents of a file.
- A tree contains references (sha1) to blobs and other trees.
- A commit contains an author, committer, message, a reference to a tree, and references to parent commit(s).

Git stores its objects in the `.git/objects` directory. This includes “loose” objects, and one or more “packfiles”. You can view an object (whether loose or packed) with: `git cat-file -p <object_sha1>`.

### Loose objects

For example, an individual object with sha1 hash `8c7834fa3b2e97e5c465feed6ecaf5b777b57852` would be stored inside the `.git/objects/8c` directory, as file `7834fa3b2e97e5c465feed6ecaf5b777b57852`. At the command-line, we can run:

* `git cat-file -t 8c7834fa3b2e97e5c465feed6ecaf5b777b57852` to see the type of this object (e.g. “blob”)
* `git cat-file -s 8c7834fa3b2e97e5c465feed6ecaf5b777b57852` to see its size
* `git cat-file -p 8c7834fa3b2e97e5c465feed6ecaf5b777b57852` to see its raw contents, pretty-printed

### Packfiles

Calling `git gc` or `git repack` packs up the (non-useless) loose objects, into a single (if possible) “packfile”. These are inside the `.git/objects/pack/` directory. 

Running `git verify-pack -v <packfile_name>` shows the objects packed in the packfile. For example,

```
git verify-pack -v .git/objects/pack/pack-ee18f0f6494322cbf390d884227a14a0098d9aad.idx
```

may output lines like:

```
42888d9783dfd44612c0030003356dbe3f584b15 commit 270 182 4811
ad1100abd43cb8042b728cdc16321483547ffca1 commit 279 186 4993
6a02d658f4a936fd7d5bb05fc30560df50bdd5b3 commit 275 185 5179
0619aec4698e9b1f8bee1589b82389f2b1213b7b commit 245 159 5364
2dafc3a23dc8c1955ed17a6cb225cf66457cc360 commit 194 127 5523
9ca4c4608a3b88ea039eaf66c72b4970d22cbe91 blob   24437 7769 5650
5de21866f834ef06a479d6d0ea0cf0c5eb83f240 blob   2283 1244 13419
e7123041ee0458f44072ab4c5f267fd370f831f0 blob   4 13 14663
d37622b08b16e88ce2bb9a3fe4c0b849f3a2125c blob   34360 12743 14676
52a9a85c0b48650af3d41be09c5075c286c6fdc3 blob   31 44 27419 1 d37622b08b16e88ce2bb9a3fe4c0b849f3a2125c
95d8eee0f70bde1d44e44316bc288f9316af478a blob   1448 683 27463
70a14a52108e4566967f9a2648344fca7d3da092 blob   32740 12461 28146
ebe43e66c00715818d530057e0d358ae16fe6c8c blob   70 76 40607
98205597c91cad85c1d932e8b387cf87bbaaa601 blob   982150 747223 40683
e23ff48a3e5edee55081030aa7030ef496ccb51f tree   105 110 135215856
43e10db14ec3124babaec2937956a5bc9ae22923 tree   77 79 135215966
e0f0c8b0606632fc31a31c6f2c40facbb569c31d blob   17 32 135216045 1 d37622b08b16e88ce2bb9a3fe4c0b849f3a2125c
7e28c6822920704254953649ff4cbcf574f69e64 tree   105 111 135216077
0847592a8e925d38d1dcade405d73bdb9d618482 blob   2652 1095 135216188 2 664459c55427c538ad077c9d6be2a8b7a852e08f
4ec864f230f76a89a61fb21af561a8b5260fd7f8 blob   219 156 135217283
```

followed by a few other kinds of lines.

In the main part of the output (as shown above), there are two kinds of lines:

* Those like `SHA-1 type size size-in-pack-file offset-in-packfile ` e.g.

  ```
  afe561a8a28d088c4259a4cbc3a5b6299eebf7a2 blob   134 113 20692342
  ```

  This one means that object `afe561a8a28d088c4259a4cbc3a5b6299eebf7a2` is of type `blob`, has size `134` bytes, but in the packfile it's packed to a size of `113` bytes, starting at offset `20692342`.

* Those like `SHA-1 type size size-in-pack-file offset-in-packfile depth base-SHA-1` e.g.

  ```
  8c0566d2992b4b8900cecb552e7ebe43a80e0a94 commit 114 117 20692225 1 1a278471eb3c6584a3e94e0d977775882ced0407

  afe561a8a28d088c4259a4cbc3a5b6299eebf7a2 blob   134 113 20692342

  600d9685d79d1f5da591889bd41747d41bb8e28f blob   19 30 20692455 1 afe561a8a28d088c4259a4cbc3a5b6299eebf7a2
  ```

### Code for parsing output of `git verify-pack -v`

Here is Python code for what we've discussed so far. (Jump to the [next section](#names-of-objects) if you're not interested in the code.)

Function `object_line_re` simply returns a regex matching the two kinds of lines mentioned.

```python
def object_line_re():
    """Regex matching the object lines from `git verify-pack -v`:
           SHA-1 type size size-in-pack-file offset-in-packfile
           SHA-1 type size size-in-pack-file offset-in-packfile depth base-SHA-1
    For example:
8c0566d2992b4b8900cecb552e7ebe43a80e0a94 commit 114 117 20692225 1 1a278471eb3c6584a3e94e0d977775882ced0407
afe561a8a28d088c4259a4cbc3a5b6299eebf7a2 blob   134 113 20692342
600d9685d79d1f5da591889bd41747d41bb8e28f blob   19 30 20692455 1 afe561a8a28d088c4259a4cbc3a5b6299eebf7a2
    """
    basic_regexes = {
        'sha1_re': r'[0-9a-f]{40}',
        'type_re': r'(commit|blob  |tree  |tag   )',
        'num_re':  r'[0-9]{1,}'
    }
    field_regexes = {
        'object':      r'(?P<object_sha1>{sha1_re})'.format(**basic_regexes),
        'type':        r'(?P<object_type>{type_re})'.format(**basic_regexes),
        'orig_size':   r'(?P<orig_size>{num_re})'.format(**basic_regexes),
        'packed_size': r'(?P<packed_size>{num_re})'.format(**basic_regexes),
        'offset':      r'(?P<offset>{num_re})'.format(**basic_regexes),
        'depth':       r'(?P<depth>{num_re})'.format(**basic_regexes),
        'base':        r'(?P<base_object>{sha1_re})'.format(**basic_regexes),
    }
    line_re = '^{object} {type} {orig_size} {packed_size} {offset}( {depth})?( {base})?$'.format(**field_regexes)
    return line_re
```

We want to match the regex and return an object (a Python dictionary) containing those fields:

```python
def re_match(pattern, string):
    return re.match('^' + pattern + '$', string)


def parse_object_line(s):
    assert isinstance(s, unicode), (type(s), s)
    assert len(s) > 0
    m = re_match(object_line_re(), s)
    assert m, 'No match for #%s#' % s
    return {
        'sha1': m.group('object_sha1'),
        'type': m.group('object_type'),
        'orig_size': int(m.group('orig_size')),
        'packed_size': int(m.group('packed_size')),
        'offset': int(m.group('offset')),
        'depth': None if m.group('depth') == None else int(m.group('depth')),
        'base': m.group('base_object')
    }
```

Finally, as we read the output of `git verify-pack -v`, we'd like to discard the uninteresting lines, do some sanity-checks that confirm our understanding, and return a list of all the parsed objects. The function `objects_from_verify_pack` brings all of this together:

```python
def non_object_line(s):
    num_re = r'[0-9]{1,}'
    sha1_re = r'[0-9a-f]{40}'
    return (re_match('non delta: {num} objects'.format(num=num_re), s) or
            re_match('chain length = {num}: {num} objects?'.format(num=num_re), s) or
            re_match('.git/objects/pack/pack-{sha}.pack: ok'.format(sha=sha1_re), s))


def objects_from_verify_pack(lines):
    ret = []
    for line in lines:
        if non_object_line(line):
            continue
        obj = parse_object_line(line)
        if ret:
            assert ret[-1]['offset'] + ret[-1]['packed_size'] == obj['offset'], (ret[-1], obj)
        assert obj['type'] in ['tag   ', 'commit', 'blob  ', 'tree  '], '#%s#' % obj['type']
        ret.append(obj)
    return ret
```

## Names of objects

We can associate objects with their names by using `git rev-list --objects --all`. This lists each object along with, in case it's a blob,[^onlyblobs] its filename. For example,

```
0431aa5d99bcb2e63f13377235f33f3eee4fc842 mine/notes.md
```

shows that the object `0431aa5d99bcb2e63f13377235f33f3eee4fc842` (of type “blob”) has filename `mine/notes.md`.

[^onlyblobs]: Trees, commits, and tags take up nonzero space too, but they're usually tiny.

### Code for names of objects

This just maps each blob (object) name from the kind of output above, to the file name.

```python
def index_blob_names(lines):
    """Takes output from rev-list, and maps blob names to file names."""
    ret = {}
    for line in lines:
        parts = line.split(' ', 1)
        # Some blobs are unreachable, so line has just a sha1.
        if len(parts) > 1:
            assert len(parts) == 2, parts
            # if len(parts[1].split()) > 1:
            #     print 'filename with spaces:', line,
            ret[parts[0]] = parts[1].strip()
    return ret
```

```
0431aa5d99bcb2e63f13377235f33f3eee4fc842 mine/notes.md
```



## Program

Putting together everything we've learned, here's the general plan of the program:

1. Run `git gc` or at least `git repack` first, to pack up loose objects (so that we don't have to bother counting them, and can focus on just the packfile).
2. Run `git verify-pack -v` on each packfile (usually there's only one) in `.git/objects/pack`, to get the sizes of blobs in the packfile.
3. Run `git rev-list --objects --all`, to associate each object (blob) with its filename.
4. Aggregate the sizes by filename.

### Code for main program

We've already seen the code for Steps 2 and 3; there's not much to the rest:

```python
def run_process(cmd_parts):
    logging.info('Running: %s', ' '.join(cmd_parts))
    return subprocess.check_output(cmd_parts).decode('ascii').splitlines()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')

    run_process(['git', 'gc'])

    # verify_pack_lines = codecs.open('git-verify-pack-unsorted', encoding='ascii').readlines()
    verify_pack_lines = run_process(['git', 'verify-pack', '-v'] +
                                    glob.glob('.git/objects/pack/pack-*.idx'))
    logging.info('Parsing the output')
    objects = objects_from_verify_pack(verify_pack_lines)
    # objects.sort(cmp=lambda x, y: cmp(x['packed_size'], y['packed_size']), reverse=True)

    (total_size, unnormalized, normalized) = aggregate_sizes_by_filename(objects)
    print '\nUnnormalized:'
    print_sizes(unnormalized, total_size)
    print '\nNormalized:'
    print_sizes(normalized, total_size)
```

Here, the normalization is a small feature added for aggregating files further.

```python
def normalize_filename(name):
    # Normalization 1: glob patterns
    glob_patterns = ['logs/.nfs*', '*node_modules*', '*.png', '*.jpg', '*.sql']
    for pattern in glob_patterns:
        if fnmatch.fnmatch(name, pattern):
            name = pattern
    # Normalization 2: files we don't care to distinguish
    same = [['*.sql', 'dump.csv'], ['*.png', '*.jpg']]
    for equivalence_class in same:
        if name in equivalence_class:
            name = ' or '.join(equivalence_class)
    # if orig_name != name:
    #   print 'Normalized %s to %s' % (orig_name, name)
    return name


def aggregate_sizes_by_filename(objects):
    # rev_list_lines = codecs.open('git-all-objects.txt', encoding='ascii').readlines()
    rev_list_lines = run_process(['git', 'rev-list', '--objects', '--all'])
    blob_names = index_blob_names(rev_list_lines)

    aggregated_size = {'unnormalized': collections.defaultdict(int),
                       'normalized': collections.defaultdict(int)}
    total_size = 0

    logging.info('Aggregating sizes of files')
    for obj in objects:
        size = obj['packed_size']
        sha1 = obj['sha1']
        if obj['type'] == 'blob  ' and sha1 in blob_names:
            key = blob_names[sha1]
        else:
            key = '{0} ({1})'.format(sha1, obj['type'].strip())
        aggregated_size['unnormalized'][key] += size
        aggregated_size['normalized'][normalize_filename(key)] += size
        total_size += size
    logging.info('Done.')
    return (total_size, aggregated_size['unnormalized'], aggregated_size['normalized'])
```

And `print_sizes` just prints the output somewhat prettily:

```python
def print_sizes(sizes, total_size, limit=20):
    cumulative = 0
    print 'Cumulat       Size Filename'
    for (i, (key, size)) in enumerate(sorted(sizes.iteritems(), key=lambda x: x[1], reverse=True)):
        if i >= limit:
            break
        cumulative += size
        cumulative_percent = '%6.2f%%' % (cumulative * 100.0 / total_size)
        padded_size = '%10d' % size
        print '%s %s %s' % (cumulative_percent, padded_size, key)
```

### Example usage

The whole file is available here. Here is are a couple of examples of using `pack_stats.py`, with slight changes to the `normalize_filename` function, taking two of the “most starred” repositories on GitHub:

```
% git clone https://github.com/facebook/react.git
% cd react
% python ~/tmp/pack-stats.py
21:40:51 Running: git gc
Counting objects: 133178, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (38205/38205), done.
Writing objects: 100% (133178/133178), done.
Total 133178 (delta 87690), reused 133178 (delta 87690)
21:40:54 Running: git verify-pack -v .git/objects/pack/pack-cbc8b897541007e3c238670bae05259b2a613c30.idx
21:40:59 Parsing the output
21:41:02 Running: git rev-list --objects --all
21:41:03 Aggregating sizes of files
21:41:05 Done.

Unnormalized:
Cumulat       Size Filename
  4.05%    5589674 docs/img/blog/steve_reverse.gif
  5.46%    1938492 feed.xml
  6.82%    1876445 fixtures/dom/public/test.mp4
  8.09%    1749212 docs/js/react.js
  9.10%    1392744 docs/img/blog/devtools-full.gif
 10.07%    1339403 docs/img/blog/react-50k-tshirt.jpg
 10.96%    1225044 docs/img/docs/react-devtools-state.gif
 11.81%    1178231 docs/img/blog/cra-dynamic-import.gif
 12.59%    1077569 blog/index.html
 13.34%    1031710 docs/img/blog/cra-runtime-error.gif
 14.06%     999664 docs/img/blog/modus-create.gif
 14.73%     922294 npm-shrinkwrap.json
 15.39%     911577 blog/page2/index.html
 16.04%     897576 docs/downloads/react-0.12.2.zip
 16.69%     887643 docs/downloads/react-0.12.0.zip
 17.33%     881556 blog/page3/index.html
 17.95%     855381 docs/img/blog/devtools-search.gif
 18.56%     844780 docs/downloads/react-0.13.3.zip
 19.17%     843658 docs/downloads/react-0.13.2.zip
 19.78%     843183 docs/downloads/react-0.13.1.zip

Normalized:
Cumulat       Size Filename
 22.40%   30894996 docs/downloads/*
 37.50%   20828172 blog/*
 48.22%   14783529 docs/img/*
 57.07%   12207367 *.png or *.jpg
 58.47%    1938492 feed.xml
 59.83%    1876445 fixtures/dom/public/test.mp4
 61.15%    1821756 downloads/*
 62.42%    1749212 docs/js/react.js
 63.09%     922294 npm-shrinkwrap.json
 63.60%     707621 yarn.lock
 64.01%     556257 scripts/fiber/tests-passing.txt
 64.40%     538927 js/babel-browser.min.js
 64.76%     506072 js/JSXTransformer.js
 65.09%     448350 CHANGELOG.md
 65.41%     437829 docs/js/react-dom.js
 65.71%     423967 src/renderers/dom/shared/__tests__/ReactDOMComponent-test.js
 66.01%     406261 js/react.js
 66.28%     372890 js/babel.min.js
 66.52%     326202 src/renderers/dom/shared/ReactDOMComponent.js
 66.73%     296028 docs/tutorial.html
```

And another:

```
% git clone https://github.com/golang/go.git
% cd go
% python ~/tmp/pack-stats.py
19:28:05 Running: git gc
Counting objects: 333421, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (65823/65823), done.
Writing objects: 100% (333421/333421), done.
Total 333421 (delta 265185), reused 333421 (delta 265185)
Checking connectivity: 333421, done.
19:28:15 Running: git verify-pack -v .git/objects/pack/pack-d2dbded1eb87bb4a79f9693d2d79944e19dbe3d8.idx
19:28:27 Parsing the output
19:28:35 Running: git rev-list --objects --all
19:28:37 Aggregating sizes of files
19:28:41 Done.

Unnormalized:
Cumulat       Size Filename
  1.68%    2656211 src/cmd/compile/internal/gc/ssa.go
  3.11%    2249070 src/pkg/exp/locale/collate/tables.go
  4.44%    2105208 src/crypto/internal/boring/goboringcrypto_linux_amd64.syso
  5.73%    2027063 src/cmd/compile/internal/ssa/rewriteAMD64.go
  6.82%    1722334 src/cmd/cover/cover
  7.77%    1508251 src/pkg/exp/regexp/re2.txt.gz
  8.69%    1454991 misc/trace/trace_viewer_lean.html
  9.48%    1239749 src/cmd/go/build.go
 10.26%    1223838 src/net/http/h2_bundle.go
 10.99%    1161578 src/cmd/compile/internal/ssa/opGen.go
 11.69%    1098279 doc/GoCourseDay1.pdf
 12.26%     896866 src/cmd/go/go_test.go
 12.82%     893453 src/net/http/serve_test.go
 13.38%     874823 src/pkg/exp/eval/eval
 13.91%     847985 src/cmd/vendor/github.com/google/pprof/internal/report/testdata/sample.bin
 14.43%     822732 src/cmd/compile/internal/ssa/rewritegeneric.go
 14.95%     808963 doc/talks/io2010/talk.pdf
 15.45%     797070 src/cmd/internal/obj/x86/asm6.go
 15.95%     781395 src/cmd/compile/internal/gc/walk.go
 16.44%     777351 lib/time/zoneinfo.zip

Normalized:
Cumulat       Size Filename
  2.63%    4144082 *.png or *.jpg
  4.31%    2656211 src/cmd/compile/internal/gc/ssa.go
  5.73%    2249070 src/pkg/exp/locale/collate/tables.go
  7.07%    2105208 src/crypto/internal/boring/goboringcrypto_linux_amd64.syso
  8.35%    2027063 src/cmd/compile/internal/ssa/rewriteAMD64.go
  9.44%    1722334 src/cmd/cover/cover
 10.40%    1508251 src/pkg/exp/regexp/re2.txt.gz
 11.32%    1454991 misc/trace/trace_viewer_lean.html
 12.11%    1239749 src/cmd/go/build.go
 12.88%    1223838 src/net/http/h2_bundle.go
 13.62%    1161578 src/cmd/compile/internal/ssa/opGen.go
 14.31%    1098279 doc/GoCourseDay1.pdf
 14.88%     896866 src/cmd/go/go_test.go
 15.45%     893453 src/net/http/serve_test.go
 16.00%     874823 src/pkg/exp/eval/eval
 16.54%     847985 src/cmd/vendor/github.com/google/pprof/internal/report/testdata/sample.bin
 17.06%     822732 src/cmd/compile/internal/ssa/rewritegeneric.go
 17.57%     808963 doc/talks/io2010/talk.pdf
 18.08%     797070 src/cmd/internal/obj/x86/asm6.go
 18.57%     781395 src/cmd/compile/internal/gc/walk.go

```



