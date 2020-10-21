#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import argparse
import logging
from html import escape # Python 3 only

import markdown
import markdown.extensions.codehilite
import markdown.extensions.extra
import markdown.extensions.toc
import markdown.extensions.nl2br
import markdown.extensions.admonition

import markdown_link_attr_modifier
import gfm

from css_html_js_minify import css_minify, html_minify

__version__ = '0.1.1'

logging_stream = sys.stderr
logging_format = '\033[1m%(asctime)s [%(levelname)s]:\033[0m%(message)s'

if 'DEBUG' in os.environ:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

if logging_stream.isatty():
    logging_date_format = '%H:%M:%S'
else:
    print('', file=logging_stream)
    logging_date_format = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    level=logging_level,
    format=logging_format,
    datefmt=logging_date_format,
    stream=logging_stream,
)

logging.addLevelName(logging.CRITICAL, '\033[31m{}\033[39m'.format(logging.getLevelName(logging.CRITICAL)))
logging.addLevelName(logging.ERROR, '\033[31m{}\033[39m'.format(logging.getLevelName(logging.ERROR)))
logging.addLevelName(logging.WARNING, '\033[33m{}\033[39m'.format(logging.getLevelName(logging.WARNING)))
logging.addLevelName(logging.INFO, '\033[36m{}\033[39m'.format(logging.getLevelName(logging.INFO)))
logging.addLevelName(logging.DEBUG, '\033[36m{}\033[39m'.format(logging.getLevelName(logging.DEBUG)))


if sys.flags.optimize > 0:
    logging.critical('Do not run with "-O", assert require no optimize')
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Yet another markdown to html converter, generate an offline all-in-one single HTML file.',
        add_help=True
    )
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbose output')
    parser.add_argument('-V', '--version', action='store_true', help='Output version info and exit')

    parser.add_argument('-t', '--title', help='If omitted, generate from input filename')
    parser.add_argument('-f', '--force', action='store_true', help='Force overwrite if output file exists')
    parser.add_argument('input_file', nargs='?', help='If omitted or "-", use stdin.')
    parser.add_argument('-o', '--output-file', dest='output_file', help='If omitted, auto decide. If "-", stdout.')

    parser.add_argument('--no-min-css', dest='min_css', action='store_false', help='Disable minify CSS')
    parser.add_argument('--min-html', dest='min_html', action='store_true', help='Enable minify HTML')
    parser.add_argument('--head-insert', metavar='HTML', help='HTML to insert to the start of <head>')
    parser.add_argument('--head-append', metavar='HTML', help='HTML to append to the end of <head>')
    parser.add_argument('--body-insert', metavar='HTML', help='HTML to insert to the start of <body>')
    parser.add_argument('--body-append', metavar='HTML', help='HTML to append to the end of <body>')

    args = parser.parse_args()
    
    # set args.input_file_obj
    if args.input_file is None:
        args.input_file_obj = sys.stdin
    elif args.input_file == '-':
        args.input_file_obj = sys.stdin
    else:
        args.input_file_obj = args.input_file # str
    
    # set args.output_file_obj
    if args.output_file == '-':
        args.output_file_obj = sys.stdout
    elif args.output_file is None:
        if args.input_file is None or args.input_file == '-':
            args.output_file_obj = sys.stdout
        else:
            args.output_file_obj = os.path.splitext(args.input_file)[0] + '.html' # str
    else:
        args.output_file_obj = args.output_file # str

    # set args.title
    if args.title is None:
        if args.input_file is None or args.input_file == '-':
            args.title = 'Untitled'
        else:
            args.title = os.path.splitext(args.input_file)[0]

    # set args.script_dir
    args.script_dir = os.path.abspath(os.path.dirname(__file__))

    return args


def convert(md):
    import urllib.parse # Python 3 only

    def my_slugify(value, sep):
        return urllib.parse.quote_plus(value.replace(' ', sep))
    
    extensions = [
        markdown.extensions.codehilite.CodeHiliteExtension(
            css_class='highlight',
            linenums=False,
            guess_lang=False,
        ),
        markdown.extensions.extra.ExtraExtension(),
        markdown.extensions.toc.TocExtension(
            toc_depth='2-6', # h1 not included
            permalink=True,
            slugify=my_slugify,
        ),
        markdown.extensions.nl2br.Nl2BrExtension(),
        markdown.extensions.admonition.AdmonitionExtension(),

        markdown_link_attr_modifier.LinkAttrModifierExtension(),
        gfm.StrikethroughExtension(),
        gfm.TaskListExtension(),
    ]
    return markdown.markdown(md, extensions=extensions)


def render(args, md):
    logging.info('Start rendering')
    template = '''<!doctype html>
<html>
<head>
{head_insert}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
<title>{title}</title>
{css_html_block}
{head_append}
</head>
<body>
{body_insert}
<div class="markdown-body">
{html_content}
</div>
{body_append}
</body>
</html>
'''
    title = args.title

    with open(os.path.join(args.script_dir, 'main.css'), 'r') as f:
        css_main = f.read()
    with open(os.path.join(args.script_dir, 'github-markdown.css'), 'r') as f:
        css_github = f.read()
    with open(os.path.join(args.script_dir, 'pygments.css'), 'r') as f:
        css_pygments = f.read()
    
    head_insert = args.head_insert if args.head_insert else ''
    head_append = args.head_append if args.head_append else ''
    body_insert = args.body_insert if args.body_insert else ''
    body_append = args.body_append if args.body_append else ''

    css_content_list = [css_github, css_pygments, css_main]
    if args.min_css:
        logging.info('Minify CSS')
        css_content_list = [css_minify(_, comments=False) for _ in css_content_list]
    css_html_block = '\n'.join(['<style type="text/css">\n' + _ + '\n</style>' for _ in css_content_list])

    logging.info('Converting Markdown')
    html_content = convert(md)

    if args.min_html:
        logging.info('Minify HTML')
        html_content = html_minify(html_content, comments=False)

    template_args = {
        'title': escape(title),
        'css_html_block': css_html_block,
        'html_content': html_content,
        'head_insert': head_insert,
        'head_append': head_append,
        'body_insert': body_insert,
        'body_append': body_append,
    }
    return template.format(**template_args)


# obj: fd or str
def read_file(obj):
    try:
        if type(obj) == str:
            logging.info('Reading %r', obj)
            with open(obj, 'r') as f:
                return f.read()
        else:
            logging.info('Reading %s', obj.name)
            return obj.read()
    except Exception as e:
        logging.error('%r %r', type(e), e)
        sys.exit(1)


# obj: fd or str
def write_file(obj, content):
    try:
        if type(obj) == str:
            logging.info('Writing %d Bytes to %r', len(content), obj)
            with open(obj, 'w') as f:
                f.write(content)
        else:
            logging.info('Writing %d Bytes to %s', len(content), obj.name)
            obj.write(content)
    except Exception as e:
        logging.error('%r %r', type(e), e)
        sys.exit(1)


def print_version_exit():
    print(f'md2html version {__version__}')
    sys.exit(1)


def main():
    args = parse_args()

    if args.verbose > 0:
        logging.root.setLevel(logging.DEBUG)
    
    logging.debug('If you see this, verbose output is enabled.')
    logging.debug('argparse result: %r', args)

    if args.version:
        print_version_exit()

    if type(args.output_file_obj) == str and os.path.exists(args.output_file_obj) and not args.force:
        logging.error('%r already exists. Use -f to overwrite.', args.output_file_obj)
        sys.exit(1)
    
    logging.info('Page title is: %r', args.title)

    md = read_file(args.input_file_obj)
    result = render(args, md)
    write_file(args.output_file_obj, result)


if __name__ == "__main__":
    main()

