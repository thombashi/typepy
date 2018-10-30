# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from decimal import Decimal


class DefaultValue(object):
    FLOAT_TYPE = Decimal
    STRIP_ANSI_ESCAPE = True


class StrictLevel(object):
    MIN = 0
    MAX = 100


class ParamKey(object):
    STRIP_ANSI_ESCAPE = "strip_ansi_escape"
    TIMEZONE = "timezone"
