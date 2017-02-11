# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from decimal import Decimal

import six

from ..type._realnumber import RealNumber
from ._checker import (
    TypeChecker,
    TypeCheckerStrictLevel,
)
from ._common import (
    isnan,
    isinf,
)


class IntegerTypeCheckerStrictLevel0(TypeCheckerStrictLevel):

    def is_instance(self):
        if isinstance(self._value, six.integer_types):
            return not isinstance(self._value, bool)

        if isinstance(self._value, float) or isinstance(self._value, Decimal):
            return True

        return False

    def is_exclude_instance(self):
        return isinf(self._value) or isnan(self._value)


class IntegerTypeCheckerStrictLevel1(IntegerTypeCheckerStrictLevel0):

    def is_instance(self):
        if not super(IntegerTypeCheckerStrictLevel1, self).is_instance():
            return False

        if isinstance(self._value, float) or isinstance(self._value, Decimal):
            if float(self._value).is_integer():
                return True

        try:
            return self._value.is_integer()
        except AttributeError:
            pass

        return False

    def is_exclude_instance(self):
        return any([
            super(IntegerTypeCheckerStrictLevel1, self).is_exclude_instance(),
            isinstance(self._value, bool),
            #isinstance(self._value, float) and not self._value.is_integer(),
            # isinstance(self._value, Decimal) and not float(
            #    self._value).is_integer(),
            RealNumber(self._value, strict_level=1).is_type(),
        ])

    # def is_valid_after_convert(self, converted_value):


class IntegerTypeCheckerStrictLevel2(IntegerTypeCheckerStrictLevel1):

    def is_exclude_instance(self):
        return any([
            isinstance(self._value, six.string_types),
            isinstance(self._value, bool),
            isinstance(self._value, float),
            isinstance(self._value, Decimal),
        ])


class IntegerTypeChecker(TypeChecker):

    def __init__(self, value, strict_level):
        super(IntegerTypeChecker, self).__init__(
            value=value,
            checker_mapping={
                0: IntegerTypeCheckerStrictLevel0,
                1: IntegerTypeCheckerStrictLevel1,
                2: IntegerTypeCheckerStrictLevel2,
            },
            strict_level=strict_level)
