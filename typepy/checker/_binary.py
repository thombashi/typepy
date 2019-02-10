# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import six

from ._checker import CheckerFactory, TypeCheckerBase, TypeCheckerDelegator


class BinaryTypeCheckerStrictLevel0(TypeCheckerBase):
    def is_instance(self):
        return isinstance(self._value, six.binary_type)

    def is_valid_after_convert(self, converted_value):
        return isinstance(converted_value, six.binary_type)


_factory = CheckerFactory(checker_mapping={0: BinaryTypeCheckerStrictLevel0})


class BinaryTypeChecker(TypeCheckerDelegator):
    def __init__(self, value, strict_level):
        super(BinaryTypeChecker, self).__init__(
            value=value, checker_factory=_factory, strict_level=strict_level
        )
