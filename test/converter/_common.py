# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import pytypeutil


EXCEPTION_RESULT = "E"


def convert_wrapper(typeobj, method):
    try:
        return getattr(typeobj, method)()
    except (pytypeutil.TypeConversionError):
        return EXCEPTION_RESULT
