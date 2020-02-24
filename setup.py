#!/usr/bin/env python3

import setuptools
from pathlib import Path

project_dir = Path(__file__).parent

setuptools.setup(
    name='twittervideo',
    version='1.0.0',

    description='Summarize twitter feeds in a wordcloud video',

    # Allow UTF-8 characters in README with encoding argument.
    # long_description=project_dir.joinpath('README.rst').read_text(encoding="utf-8"),
    keywords=['python'],

    author='jpsullivan',
    url='https://www.github.com/ec500C1/video-sullyj42',

    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},

    # pip 9.0+ will inspect this field when installing to help users install a
    # compatible version of the library for their Python version.
    python_requires='>=3.5',
    package_data={'': ['fonts/*.ttf']},
    # data_files=[('textfiles', ['textfiles/commonwords.txt', 'textfiles/commonwords2.txt'])]
    include_package_data=True,
)
