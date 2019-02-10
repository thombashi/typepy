# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from ._checker import CheckerFactory, TypeChecker, TypeCheckerStrictLevel
from ._common import isinf, isstring


class InfinityCheckerStrictLevel0(TypeCheckerStrictLevel):
    def is_instance(self):
        return isinf(self._value)

    def is_valid_after_convert(self, converted_value):
        try:
            return converted_value.is_infinite()
        except AttributeError:
            return False


class InfinityCheckerStrictLevel1(InfinityCheckerStrictLevel0):
    def is_exclude_instance(self):
        return isstring(self._value)


_factory = CheckerFactory(
    checker_mapping={0: InfinityCheckerStrictLevel0, 1: InfinityCheckerStrictLevel1}
)


class InfinityTypeChecker(TypeChecker):
    def __init__(self, value, strict_level):
        super(InfinityTypeChecker, self).__init__(
            value=value, checker_factory=_factory, strict_level=strict_level
        )
