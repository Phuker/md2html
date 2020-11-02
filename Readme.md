# md2html

Yet another markdown to html converter, generate an offline all-in-one single HTML file.

This is a *feng-he-guai* program. Python code based on:

- [Python-Markdown](https://python-markdown.github.io/) and its officially supported extensions
- [Phuker/markdown_link_attr_modifier](https://github.com/Phuker/markdown_link_attr_modifier), my `Python-Markdown` extension to add attributes like `target="_blank"` to `<a>` tags
- [Zopieux/py-gfm](https://github.com/Zopieux/py-gfm), a `Python-Markdown` extension to support some [GFM](https://github.github.com/gfm/) features
- [juancarlospaco/css-html-js-minify](https://github.com/juancarlospaco/css-html-js-minify), a library to minify CSS and HTML code

CSS based on:

- [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css), the GitHub Markdown style, main theme
- [Pygments](https://pygments.org/), style for Code highlight code blocks
- Others copy & modify from [my blog](https://phuker.github.io/)

## Features

### Generated HTML

The principle is: keep it simple.

- All-in-one single HTML file
- Completely offline, no CDN, no web fonts
- No JavaScript

### Markdown syntax

This is a Markdown dialect, similar but different from [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/).

Default enabled Markdown features:

- [Extra](https://python-markdown.github.io/extensions/extra/) extensions
- [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/)
- [Table of Contents](https://python-markdown.github.io/extensions/toc/)
- [New Line to Break](https://python-markdown.github.io/extensions/nl2br/)
- [Admonition](https://python-markdown.github.io/extensions/admonition/)
- `<a target="_blank"`
- Part of GitHub Flavored Markdown

For details, see `convert()` function of `md2html/__init__.py`, and the demo below.

#### Demo

Download [.zip source code files](https://github.com/Phuker/md2html/archive/main.zip), extract it. In the directory `demo/`, there is a `demo.html` which is generated from `demo.md`. You can see `demo.md` to see supported syntax, and open `demo.html` in your browser to see its result.

## Requirements

- Python >= `3.6`, with `pip` installed

## Install

```bash
python3 -m pip install -U md2html-phuker
```

There are too many similar projects with similar names in PyPI, `md2html`, `md-to-html`, `markdown2html`, `markdown-to-html`, `mrkdwn2html` ... I have to add a suffix to keep away from this war of naming.

## Usage

### Show help

```console
$ md2html --help
usage: md2html [-h] [-v] [-V] [-t TITLE] [-f] [-o FILE] [--append-css FILE] [--no-min-css] [--min-html] [--head-insert HTML] [--head-append HTML] [--body-insert HTML] [--body-append HTML] [input_file]

Yet another markdown to html converter, generate an offline all-in-one single HTML file.

positional arguments:
  input_file            If omitted or "-", use stdin.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output
  -V, --version         Output version info and exit
  -t TITLE, --title TITLE
                        If omitted, generate from input filename
  -f, --force           Force overwrite if output file exists
  -o FILE, --output-file FILE
                        If omitted, auto decide. If "-", stdout.
  --append-css FILE     Append embedded CSS files, may specify multiple times.
  --no-min-css          Disable minify CSS, default enabled.
  --min-html            Enable minify HTML, default disabled.
  --head-insert HTML    HTML to insert to the start of <head>, may specify multiple times.
  --head-append HTML    HTML to append to the end of <head>, may specify multiple times.
  --body-insert HTML    HTML to insert to the start of <body>, may specify multiple times.
  --body-append HTML    HTML to append to the end of <body>, may specify multiple times.
```

If you are not sure about what will happen if you combine `[-o OUTPUT_FILE]`, `[input_file]` and `[-t TITLE]`, see `test.py`, which contains tens of input cases and their intended behaviors.

### Convert a file

```bash
md2html foo.md
```

This program will generate `foo.html` in the same dir, with HTML title `foo`.

### Read from `stdin`, output to `stdout`, specify HTML title

```bash
md2html --title 'baz' <foo.md >bar.html
```

```bash
cat foo.md | md2html -t 'baz' >bar.html
```

## Tests

```bash
make test
```

## FAQ

## License

This repo is licensed under the **GNU General Public License v3.0**
