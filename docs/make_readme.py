#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
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

    maker.write_chapter("For more information")
    maker.write_line_list([
        "Type check/validate/convert results will be changed according to",
        "``strict_level`` value which can be passed to constructors as an argument.",
        "More information can be found in the ",
        "`API reference <http://{:s}.rtfd.io/en/latest/pages/reference/index.html>`__.".format(
            PROJECT_NAME),
    ])


def main():
    maker = readmemaker.ReadmeMaker(PROJECT_NAME, OUTPUT_DIR)
    intro_root = Path(os.path.join("pages", "introduction"))

    maker.write_file(intro_root.joinpath("badges.txt"))

    maker.inc_indent_level()
    maker.write_chapter("Summary")
    maker.write_file(intro_root.joinpath("summary.txt"))

    write_examples(maker)

    maker.set_indent_level(0)
    maker.write_chapter("Features")
    maker.write_file(intro_root.joinpath("features.txt"))

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
