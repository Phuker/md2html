# md2html

Yet another markdown to html converter, generate an offline all-in-one single HTML file.

Program based on:

- [Python-Markdown](https://python-markdown.github.io/)
- My [markdown_link_attr_modifier](https://github.com/Phuker/markdown_link_attr_modifier)
- [Zopieux/py-gfm](https://github.com/Zopieux/py-gfm)
- [juancarlospaco/css-html-js-minify](https://github.com/juancarlospaco/css-html-js-minify)

CSS based on:

- Main theme: [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)
- Code highlight: [Pygments](https://pygments.org/)
- Others copy & modify from [my blog](https://phuker.github.io/)

## Features

The principle is: keep it simple.

- All-in-one single HTML file
- Completely offline, no CDN, no web fonts
- No JavaScript

Default enabled Markdown features: CodeHilite, Table of Contents, New Line to Break, Admonition, `<a target="_blank"`, part of GitHub-Flavored Markdown. For details, see `md2html/__init__.py`, `convert()` function, and [Python-Markdown Extensions docs](https://python-markdown.github.io/extensions/).

## Demo

Click [Download ZIP](https://github.com/Phuker/md2html/archive/main.zip) to download all files, extract it, open `demo/demo.html` in your browser.

## Requirements

- Python >= `3.6`, with `pip` installed

## Install

```bash
python3 -m pip install md2html-phuker
```

## Usage

```console
$ md2html --help
usage: md2html [-h] [-v] [-V] [-t TITLE] [-f] [-o OUTPUT_FILE] [--no-min-css] [--min-html] [--head-insert HTML] [--head-append HTML] [--body-insert HTML] [--body-append HTML] [input_file]

Convert .md to a single .html web page

positional arguments:
  input_file            If omitted or "-", use stdin.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output
  -V, --version         Output version info and exit
  -t TITLE, --title TITLE
                        If omitted, generate from input filename
  -f, --force           Force overwrite if output file exists
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        If omitted, auto decide. If "-", stdout.
  --no-min-css          Disable minify CSS
  --min-html            Enable minify HTML
  --head-insert HTML    HTML to insert to the start of <head>
  --head-append HTML    HTML to append to the end of <head>
  --body-insert HTML    HTML to insert to the start of <body>
  --body-append HTML    HTML to append to the end of <body>
```

## Tests

- Arguments: input x oupput x force x title, etc.

## FAQ

## License

This repo is licensed under the **GNU General Public License v3.0**
