#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup

with open('Readme.PyPI.md', 'r') as f:
    long_description = f.read()

setup(
    name='md2html-phuker',
    description='Yet another markdown to html converter, generate an offline all-in-one single HTML file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Phuker',
    author_email='Phuker@users.noreply.github.com',
    url='https://github.com/Phuker/md2html',
    license='GNU General Public License v3.0',
    keywords='markdown html convert',
    packages=['md2html'],
    py_modules = [],
    package_data={
        "md2html": ["*.css"],
    },
    entry_points={
        'console_scripts': [
            'md2html=md2html:main'
        ]
    },
    install_requires=[
        'markdown>=3',
        'pygments',
        'css-html-js-minify',
        'markdown-link-attr-modifier',
        'py-gfm',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: Markdown',
    ],
    python_requires = '>=3.6'
)
