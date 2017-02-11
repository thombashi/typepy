# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from decimal import Decimal

import six

from ._checker import (
    TypeChecker,
    TypeCheckerStrictLevel,
)
from ._common import (
    isstring,
    isnan,
    isinf,
)


class RealNumberTypeCheckerStrictLevel0(TypeCheckerStrictLevel):

    def is_instance(self):
        return any([
            isinstance(self._value, float),
            isinstance(self._value, Decimal),
        ])

    def is_exclude_instance(self):
        return any([
            isinstance(self._value, bool),
            isinf(self._value),
            isnan(self._value)
        ])

    def is_valid_after_convert(self, converted_value):
        return all([
            not isinf(converted_value),
            not isnan(converted_value),
        ])


class RealNumberTypeCheckerStrictLevel1(RealNumberTypeCheckerStrictLevel0):

    def is_instance(self):
        return (
            super(RealNumberTypeCheckerStrictLevel1, self).is_instance() and
            not float(self._value).is_integer()
        )

    def is_exclude_instance(self):
        return any([
            super(RealNumberTypeCheckerStrictLevel1,
                  self).is_exclude_instance(),
            isinstance(self._value, six.integer_types),
        ])

    def is_valid_after_convert(self, converted_value):
        return not float(converted_value).is_integer()


class RealNumberTypeCheckerStrictLevel2(RealNumberTypeCheckerStrictLevel1):

    def is_exclude_instance(self):
        return any([
            super(RealNumberTypeCheckerStrictLevel2,
                  self).is_exclude_instance(),
            isstring(self._value),
        ])


class RealNumberTypeChecker(TypeChecker):

    def __init__(self, value, strict_level):
        super(RealNumberTypeChecker, self).__init__(
            value=value,
            checker_mapping={
                0: RealNumberTypeCheckerStrictLevel0,
                1: RealNumberTypeCheckerStrictLevel1,
                2: RealNumberTypeCheckerStrictLevel2,
            },
            strict_level=strict_level)
