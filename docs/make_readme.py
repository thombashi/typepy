#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import os
import sys

from path import Path
import readmemaker


PROJECT_NAME = "typepy"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)
    maker.write_chapter("Usage")

    intro_root = Path(os.path.join("pages", "introduction"))

    maker.write_file(intro_root.joinpath("usage.txt"))


def main():
    maker = readmemaker.ReadmeMaker(PROJECT_NAME, OUTPUT_DIR)
    intro_root = Path(os.path.join("pages", "introduction"))

    maker.write_file(intro_root.joinpath("badges.txt"))
    maker.set_indent_level(0)

    maker.write_chapter("Summary")
    maker.write_file(intro_root.joinpath("summary.txt"))

    maker.write_chapter("Features")
    maker.write_file(intro_root.joinpath("features.txt"))

    write_examples(maker)

    maker.write_file(
        maker.doc_page_root_dir_path.joinpath("installation.rst"))

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_line_list([
        "http://{:s}.rtfd.io/".format(PROJECT_NAME),
    ])

    return 0


if __name__ == '__main__':
    sys.exit(main())
