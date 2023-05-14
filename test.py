#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import unittest

from md2html import md2html


ROOT = os.path.dirname(os.path.abspath(__file__))
PWD = os.getcwd()

TITLE_UNTITLED = 'Untitled'

print(f'Testing md2html: {md2html!r}')


class TestParseArgs(unittest.TestCase):
    def test_parse_args_wrong_input(self):
        cases = (
            ('-t', ),
            ('a.md', 'b.md'),
            ('-o', ),
            ('--body-insert', ),
            ('a.md', '-o'),
        )
        for case in cases:
            self.assertRaises(SystemExit, md2html._parse_args, case)
    
    def test_multiple_specified_args(self):
        shell_args = md2html._parse_args(())
        self.assertEqual(shell_args.append_css, [])
        self.assertEqual(shell_args.head_insert, [])
        self.assertEqual(shell_args.head_append, [])
        self.assertEqual(shell_args.body_insert, [])
        self.assertEqual(shell_args.body_append, [])
        self.assertEqual(shell_args.style, [])

        shell_args = md2html._parse_args(('--body-insert', '<dict>', '--body-insert', '<cook>'))
        self.assertEqual(shell_args.body_insert, ['<dict>', '<cook>'])

        shell_args = md2html._parse_args(('--append-css', '~/q/w/e.css', '--append-css', '../qwerty.css'))
        self.assertEqual(shell_args.append_css, [
            os.path.abspath(os.path.expanduser('~/q/w/e.css')),
            os.path.abspath(os.path.join(PWD, '../qwerty.css')),
        ])

        shell_args = md2html._parse_args(('--style', 'sidebar-toc'))
        self.assertEqual(shell_args.style, ['sidebar-toc'])

        self.assertRaises(SystemExit, md2html._parse_args, ('--style', 'xxx-not-exist'))

    def test_parse_args_matrix(self):
        path_in_1 = '~/abc/defg.md'
        path_in_1_result = os.path.abspath(os.path.expanduser(path_in_1))
        path_out_1 = '~/abc/defg.html'
        path_out_1_result = os.path.abspath(os.path.expanduser(path_out_1))
        title_result_1 = 'defg'

        path_in_2 = '../abcdef/defgxx.md'
        path_in_2_result = os.path.abspath(os.path.join(PWD, path_in_2))
        path_out_2 = '../abcdef/defgxx.html'
        path_out_2_result = os.path.abspath(os.path.join(PWD, path_out_2))
        title_result_2 = 'defgxx'

        title_x = 'zxcvbnm'

        cases = {
            (): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('-o', ''): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('-o', '-'): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('-o', path_out_1): (sys.stdin, path_out_1_result, TITLE_UNTITLED),
            ('-o', path_out_2): (sys.stdin, path_out_2_result, TITLE_UNTITLED),

            ('', ): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('', '-o', ''): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('', '-o', '-'): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('', '-o', path_out_1): (sys.stdin, path_out_1_result, TITLE_UNTITLED),
            ('', '-o', path_out_2): (sys.stdin, path_out_2_result, TITLE_UNTITLED),

            ('-', ): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('-', '-o', ''): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('-', '-o', '-'): (sys.stdin, sys.stdout, TITLE_UNTITLED),
            ('-', '-o', path_out_1): (sys.stdin, path_out_1_result, TITLE_UNTITLED),
            ('-', '-o', path_out_2): (sys.stdin, path_out_2_result, TITLE_UNTITLED),

            (path_in_1, ): (path_in_1_result, path_out_1_result, title_result_1),
            (path_in_1, '-o', ''): (path_in_1_result, path_out_1_result, title_result_1),
            (path_in_1, '-o', '-'): (path_in_1_result, sys.stdout, title_result_1),
            (path_in_1, '-o', path_out_1): (path_in_1_result, path_out_1_result, title_result_1),
            (path_in_1, '-o', path_out_2): (path_in_1_result, path_out_2_result, title_result_1),

            (path_in_2, ): (path_in_2_result, path_out_2_result, title_result_2),
            (path_in_2, '-o', ''): (path_in_2_result, path_out_2_result, title_result_2),
            (path_in_2, '-o', '-'): (path_in_2_result, sys.stdout, title_result_2),
            (path_in_2, '-o', path_out_1): (path_in_2_result, path_out_1_result, title_result_2),
            (path_in_2, '-o', path_out_2): (path_in_2_result, path_out_2_result, title_result_2),

            ('-t', title_x, ): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '-o', ''): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '-o', '-'): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '-o', path_out_1): (sys.stdin, path_out_1_result, title_x),
            ('-t', title_x, '-o', path_out_2): (sys.stdin, path_out_2_result, title_x),

            ('-t', title_x, '', ): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '', '-o', ''): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '', '-o', '-'): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '', '-o', path_out_1): (sys.stdin, path_out_1_result, title_x),
            ('-t', title_x, '', '-o', path_out_2): (sys.stdin, path_out_2_result, title_x),

            ('-t', title_x, '-', ): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '-', '-o', ''): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '-', '-o', '-'): (sys.stdin, sys.stdout, title_x),
            ('-t', title_x, '-', '-o', path_out_1): (sys.stdin, path_out_1_result, title_x),
            ('-t', title_x, '-', '-o', path_out_2): (sys.stdin, path_out_2_result, title_x),

            ('-t', title_x, path_in_1, ): (path_in_1_result, path_out_1_result, title_x),
            ('-t', title_x, path_in_1, '-o', ''): (path_in_1_result, path_out_1_result, title_x),
            ('-t', title_x, path_in_1, '-o', '-'): (path_in_1_result, sys.stdout, title_x),
            ('-t', title_x, path_in_1, '-o', path_out_1): (path_in_1_result, path_out_1_result, title_x),
            ('-t', title_x, path_in_1, '-o', path_out_2): (path_in_1_result, path_out_2_result, title_x),

            ('-t', title_x, path_in_2, ): (path_in_2_result, path_out_2_result, title_x),
            ('-t', title_x, path_in_2, '-o', ''): (path_in_2_result, path_out_2_result, title_x),
            ('-t', title_x, path_in_2, '-o', '-'): (path_in_2_result, sys.stdout, title_x),
            ('-t', title_x, path_in_2, '-o', path_out_1): (path_in_2_result, path_out_1_result, title_x),
            ('-t', title_x, path_in_2, '-o', path_out_2): (path_in_2_result, path_out_2_result, title_x),
        }

        for case in cases:
            result_tuple = cases[case]
            shell_args = md2html._parse_args(case)
            
            self.assertEqual(shell_args.input_file_obj, result_tuple[0])
            self.assertEqual(shell_args.output_file_obj, result_tuple[1])
            self.assertEqual(shell_args.title, result_tuple[2])


if __name__ == '__main__':
    unittest.main()
