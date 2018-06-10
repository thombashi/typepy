# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import warnings

from ._const import StrictLevel
from .type import NullString, String


def is_hex(value):
    try:
        int(value, 16)
    except (TypeError, ValueError):
        return False

    return True


def is_null_string(value):
    return NullString(value, strict_level=StrictLevel.MIN).is_type()


def is_not_null_string(value):
    return String(value, strict_level=StrictLevel.MAX).is_type()


def is_empty_string(value):
    warnings.warn(
        "is_empty_string() will be deleted in the future, "
        "use is_null_string instead.",
        DeprecationWarning)

    return is_null_string(value)


def is_not_empty_string(value):
    warnings.warn(
        "is_not_empty_string() will be deleted in the future, "
        "use is_not_null_string instead.",
        DeprecationWarning)

    return is_not_null_string(value)


def is_empty_sequence(value):
    try:
        return value is None or len(value) == 0
    except TypeError:
        return False


def is_not_empty_sequence(value):
    try:
        return len(value) > 0
    except TypeError:
        return False
