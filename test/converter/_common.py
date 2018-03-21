# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import typepy


EXCEPTION_RESULT = "E"


def convert_wrapper(typeobj, method):
    try:
        return getattr(typeobj, method)()
    except (typepy.TypeConversionError):
        return EXCEPTION_RESULT
