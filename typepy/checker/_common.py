# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import decimal
import math

import six


def isstring(value):
    return isinstance(value, six.string_types + (six.text_type, six.binary_type))


def isinf(value):
    try:
        return decimal.Decimal(value).is_infinite()
    except OverflowError:
        return True
    except TypeError:
        return False
    except (ValueError, decimal.InvalidOperation):
        return False


def isnan(value):
    try:
        return math.isnan(value)
    except (TypeError, OverflowError):
        return False
