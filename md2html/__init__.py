#!/usr/bin/env python3
# encoding: utf-8

"""
Yet another markdown to html converter, generate an offline all-in-one single HTML file.
https://github.com/Phuker/md2html
"""

import os
import sys
import argparse
import logging
import atexit
import urllib.parse
from html import escape

import markdown
import markdown.extensions.codehilite
import markdown.extensions.extra
import markdown.extensions.toc
import markdown.extensions.nl2br
import markdown.extensions.admonition
import markdown_link_attr_modifier
import gfm


__version__ = '0.5.0'
logger = logging.getLogger(__name__)

VERSION_STR_SHORT = f'md2html version {__version__}'
VERSION_STR_LONG = f'md2html version {__version__}\n{__doc__.strip()}'


def _assert(expr, msg=''):
    if not expr:
        raise AssertionError(msg)


def _init_logging():
    logging_stream = sys.stderr
    logging_format = '\x1b[1m%(asctime)s [%(levelname)s]:\x1b[0m%(message)s'
    logging_level = logging.INFO

    if logging_stream.isatty():
        logging_date_format = '%H:%M:%S'
    else:
        logging_date_format = '%Y-%m-%d %H:%M:%S %z'

    logging.basicConfig(
        level=logging_level,
        format=logging_format,
        datefmt=logging_date_format,
        stream=logging_stream,
    )

    logging.addLevelName(logging.CRITICAL, '\x1b[31m{}\x1b[39m'.format(logging.getLevelName(logging.CRITICAL)))
    logging.addLevelName(logging.ERROR, '\x1b[31m{}\x1b[39m'.format(logging.getLevelName(logging.ERROR)))
    logging.addLevelName(logging.WARNING, '\x1b[33m{}\x1b[39m'.format(logging.getLevelName(logging.WARNING)))
    logging.addLevelName(logging.INFO, '\x1b[36m{}\x1b[39m'.format(logging.getLevelName(logging.INFO)))
    logging.addLevelName(logging.DEBUG, '\x1b[36m{}\x1b[39m'.format(logging.getLevelName(logging.DEBUG)))


def _parse_args(args=sys.argv[1:]):
    choices_style = [
        'sidebar-toc',
        'dark',
    ]

    parser = argparse.ArgumentParser(
        description=VERSION_STR_LONG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True
    )

    parser.add_argument('-t', '--title', help='If omitted, generate from input filename')
    parser.add_argument('-f', '--force', action='store_true', help='Force overwrite if output file exists')
    parser.add_argument('input_file', nargs='?', help='If omitted or "-", use stdin.')
    parser.add_argument('-o', '--output-file', metavar='FILE', dest='output_file', help='If omitted, auto decide. If "-", stdout.')

    parser.add_argument('--style', metavar='PRESET', action='append', default=[], choices=choices_style, help=f'Preset style addons, choices: {", ".join(choices_style)}')

    parser.add_argument('--append-css', metavar='FILE', action='append', default=[], help='Append embedded CSS files, may specify multiple times.')

    parser.add_argument('--head-insert', metavar='HTML', action='append', default=[], help='HTML to insert to the start of <head>, may specify multiple times.')
    parser.add_argument('--head-append', metavar='HTML', action='append', default=[], help='HTML to append to the end of <head>, may specify multiple times.')
    parser.add_argument('--body-insert', metavar='HTML', action='append', default=[], help='HTML to insert to the start of <body>, may specify multiple times.')
    parser.add_argument('--body-append', metavar='HTML', action='append', default=[], help='HTML to append to the end of <body>, may specify multiple times.')

    parser.add_argument('-V', '--version', action='store_true', help='Show version and exit')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity level (use -vv or more for greater effect)')

    result = parser.parse_args(args)

    if result.verbose >= 1:
        logging.root.setLevel(logging.DEBUG)

    # set result.input_file_obj
    if not result.input_file: # None, ''
        result.input_file_obj = sys.stdin
    elif result.input_file == '-':
        result.input_file_obj = sys.stdin
    else:
        result.input_file = os.path.abspath(os.path.expanduser(result.input_file))
        result.input_file_obj = result.input_file # str
    
    # set result.output_file_obj
    if result.output_file == '-':
        result.output_file_obj = sys.stdout
    elif not result.output_file: # None, ''
        if not result.input_file or result.input_file == '-':
            result.output_file_obj = sys.stdout
        else:
            result.output_file_obj = os.path.splitext(result.input_file)[0] + '.html' # str
    else:
        result.output_file = os.path.abspath(os.path.expanduser(result.output_file))
        result.output_file_obj = result.output_file # str

    # set result.title if not specified
    if result.title is None:
        if not result.input_file or result.input_file == '-':
            result.title = 'Untitled'
        else:
            result.title = os.path.splitext(os.path.basename(result.input_file))[0]

    result.append_css = [os.path.abspath(os.path.expanduser(_)) for _ in result.append_css]

    # set result.script_dir
    result.script_dir = os.path.abspath(os.path.dirname(__file__))

    logger.debug('Command line arguments: %r', result)

    if result.version:
        print(VERSION_STR_LONG)
        sys.exit(0)

    return result


# obj: fd or str
def read_file(obj):
    if isinstance(obj, str):
        logger.info('Reading %r', obj)
        with open(obj, 'r') as f:
            return f.read()
    else:
        logger.info('Reading %s', obj.name)
        return obj.read()


# obj: fd or str
def write_file(obj, content):
    if isinstance(obj, str):
        logger.info('Writing to %r', obj)
        with open(obj, 'w') as f:
            f.write(content)
    else:
        logger.info('Writing to %s', obj.name)
        obj.write(content)


def convert(md):
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

        markdown_link_attr_modifier.LinkAttrModifierExtension(
            new_tab = 'on',
            no_referrer = 'external_only',
            auto_title = 'on',
        ),
        gfm.StrikethroughExtension(),
        gfm.TaskListExtension(list_attrs={'class': 'task-list'}, item_attrs={'class': 'task-list-item'}),
    ]
    return markdown.markdown(md, extensions=extensions)


def render(shell_args, md):
    logger.info('Start rendering')
    template = '''<!DOCTYPE html>
<!--
Generated with md2html {version}
Homepage: https://github.com/Phuker/md2html
-->
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
    title = shell_args.title

    head_insert = ''.join([_ + '\n' for _ in shell_args.head_insert])
    head_append = ''.join([_ + '\n' for _ in shell_args.head_append])
    body_insert = ''.join([_ + '\n' for _ in shell_args.body_insert])
    body_append = ''.join([_ + '\n' for _ in shell_args.body_append])

    css_file_list = [
        os.path.join(shell_args.script_dir, 'github-markdown.css'),
        os.path.join(shell_args.script_dir, 'pygments.css'),
        os.path.join(shell_args.script_dir, 'main.css'),
    ]
    
    addon_styles = {
        'sidebar-toc': 'style-sidebar-toc.css',
        'dark': 'style-dark.css',
    }
    for style_name in shell_args.style:
        css_file_list.append(os.path.join(shell_args.script_dir, addon_styles[style_name]))
    
    css_file_list += shell_args.append_css
    css_content_list = [read_file(_) for _ in css_file_list]
    
    css_html_block = '\n'.join(['<style type="text/css">\n' + _ + '\n</style>' for _ in css_content_list])

    logger.info('Converting Markdown')
    html_content = convert(md)

    template_args = {
        'version': __version__,
        'title': escape(title),
        'css_html_block': css_html_block,
        'html_content': html_content,
        'head_insert': head_insert,
        'head_append': head_append,
        'body_insert': body_insert,
        'body_append': body_append,
    }
    return template.format(**template_args)


def main():
    _init_logging()
    shell_args = _parse_args()

    if sys.stderr.isatty():
        atexit.register(lambda: logger.info('Exiting'))
    else:
        atexit.register(lambda: logger.info('Exiting\n'))

    logger.info(VERSION_STR_SHORT)
    logger.debug('Script file self path: %r', __file__)

    if isinstance(shell_args.output_file_obj, str) and os.path.exists(shell_args.output_file_obj) and not shell_args.force:
        logger.error('%r already exists. Use -f to overwrite.', shell_args.output_file_obj)
        sys.exit(1)
    
    logger.info('Page title is: %r', shell_args.title)
    
    if len(shell_args.append_css) > 0:
        logger.info('Append embedded CSS files: %s', ', '.join([repr(_) for _ in shell_args.append_css]))

    md = read_file(shell_args.input_file_obj)
    result = render(shell_args, md)
    write_file(shell_args.output_file_obj, result)


if __name__ == '__main__':
    main()
