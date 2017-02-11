# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from decimal import Decimal


class DefaultValue(object):
    FLOAT_TYPE = Decimal


class StrictLevel(object):
    MIN = 0
    MAX = 100
