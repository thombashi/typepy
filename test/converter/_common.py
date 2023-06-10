"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import typepy


EXCEPTION_RESULT = "E"


def convert_wrapper(typeobj, method):
    try:
        return getattr(typeobj, method)()
    except typepy.TypeConversionError:
        return EXCEPTION_RESULT
