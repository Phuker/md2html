#!/usr/bin/env python3
# encoding: utf-8

"""
Yet another markdown to html converter, generate an offline all-in-one single HTML file.

License:
GNU General Public License v3.0

Home page:
https://github.com/Phuker/md2html
"""

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

__version__ = '0.3.0'

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


def parse_args(arg_list=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='Yet another markdown to html converter, generate an offline all-in-one single HTML file.',
        add_help=True
    )
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbose output')
    parser.add_argument('-V', '--version', action='store_true', help='Output version info and exit')

    parser.add_argument('-t', '--title', help='If omitted, generate from input filename')
    parser.add_argument('-f', '--force', action='store_true', help='Force overwrite if output file exists')
    parser.add_argument('input_file', nargs='?', help='If omitted or "-", use stdin.')
    parser.add_argument('-o', '--output-file', metavar='FILE', dest='output_file', help='If omitted, auto decide. If "-", stdout.')

    style_choices = ['sidebar-toc', ]
    parser.add_argument('--style', metavar='PRESET', action='append', default=[], choices=style_choices, help=f'Additional preset style, choices: {", ".join(style_choices)}')

    parser.add_argument('--append-css', metavar='FILE', action='append', default=[], help='Append embedded CSS files, may specify multiple times.')

    parser.add_argument('--no-min-css', dest='min_css', action='store_false', help='Disable minify CSS, default enabled.')
    parser.add_argument('--min-html', dest='min_html', action='store_true', help='Enable minify HTML, default disabled.')

    parser.add_argument('--head-insert', metavar='HTML', action='append', default=[], help='HTML to insert to the start of <head>, may specify multiple times.')
    parser.add_argument('--head-append', metavar='HTML', action='append', default=[], help='HTML to append to the end of <head>, may specify multiple times.')
    parser.add_argument('--body-insert', metavar='HTML', action='append', default=[], help='HTML to insert to the start of <body>, may specify multiple times.')
    parser.add_argument('--body-append', metavar='HTML', action='append', default=[], help='HTML to append to the end of <body>, may specify multiple times.')

    args = parser.parse_args(arg_list)
    
    # set args.input_file_obj
    if not args.input_file: # None, ''
        args.input_file_obj = sys.stdin
    elif args.input_file == '-':
        args.input_file_obj = sys.stdin
    else:
        args.input_file = os.path.abspath(os.path.expanduser(args.input_file))
        args.input_file_obj = args.input_file # str
    
    # set args.output_file_obj
    if args.output_file == '-':
        args.output_file_obj = sys.stdout
    elif not args.output_file: # None, ''
        if not args.input_file or args.input_file == '-':
            args.output_file_obj = sys.stdout
        else:
            args.output_file_obj = os.path.splitext(args.input_file)[0] + '.html' # str
    else:
        args.output_file = os.path.abspath(os.path.expanduser(args.output_file))
        args.output_file_obj = args.output_file # str

    # set args.title if not specified
    if args.title is None:
        if not args.input_file or args.input_file == '-':
            args.title = 'Untitled'
        else:
            args.title = os.path.splitext(os.path.basename(args.input_file))[0]

    args.append_css = [os.path.abspath(os.path.expanduser(_)) for _ in args.append_css]

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
            title='Table of Contents',
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
    template = '''<!DOCTYPE html>
<!-- Generated with https://github.com/Phuker/md2html -->
<html>
<head>
{head_insert}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
<title>{title}</title>
{css_html_block}
{head_append}</head>
<body>
{body_insert}<div class="markdown-body">
{html_content}
</div>
{body_append}</body>
</html>
'''
    title = args.title

    head_insert = ''.join([_ + '\n' for _ in args.head_insert])
    head_append = ''.join([_ + '\n' for _ in args.head_append])
    body_insert = ''.join([_ + '\n' for _ in args.body_insert])
    body_append = ''.join([_ + '\n' for _ in args.body_append])

    css_file_list = [
        os.path.join(args.script_dir, 'github-markdown.css'),
        os.path.join(args.script_dir, 'pygments.css'),
        os.path.join(args.script_dir, 'main.css'),
    ]
    
    if 'sidebar-toc' in args.style:
        css_file_list.append(os.path.join(args.script_dir, 'style-sidebar-toc.css'))
    
    css_file_list += args.append_css
    css_content_list = [read_file(_) for _ in css_file_list]

    if args.min_css:
        logging.info('Minify CSS')
        size_old = sum(map(len, css_content_list))
        css_content_list = [css_minify(_, comments=False) for _ in css_content_list]
        size_new = sum(map(len, css_content_list))
        logging.info('Size shrunk %d B/%d B = %.2f %%', size_old - size_new, size_old, (size_old - size_new) / size_old * 100)
    
    css_html_block = '\n'.join(['<style type="text/css">\n' + _ + '\n</style>' for _ in css_content_list])

    logging.info('Converting Markdown')
    html_content = convert(md)

    if args.min_html:
        logging.info('Minify HTML')
        size_old = len(html_content)
        html_content = html_minify(html_content, comments=False)
        size_new = len(html_content)
        logging.info('Size shrunk %d B/%d B = %.2f %%', size_old - size_new, size_old, (size_old - size_new) / size_old * 100)

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


def print_version_exit():
    print(f'md2html version {__version__}')
    print(__doc__)
    sys.exit(1)


def main():
    args = parse_args()

    if args.verbose > 0:
        logging.root.setLevel(logging.DEBUG)
        logging.debug('Verbose output enabled')
    
    logging.debug('This file is: %r', __file__)
    logging.debug('sys.argv = %r', sys.argv)
    logging.debug('parse_args() result: %r', args)

    if args.version:
        print_version_exit()

    if type(args.output_file_obj) == str and os.path.exists(args.output_file_obj) and not args.force:
        logging.error('%r already exists. Use -f to overwrite.', args.output_file_obj)
        sys.exit(1)
    
    logging.info('Page title is: %r', args.title)
    if len(args.append_css) > 0:
        logging.info('Append embedded CSS files: %s', ', '.join([repr(_) for _ in args.append_css]))

    md = read_file(args.input_file_obj)
    result = render(args, md)
    write_file(args.output_file_obj, result)


if __name__ == "__main__":
    main()

