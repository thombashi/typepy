# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import ipaddress

from ._checker import (
    TypeChecker,
    TypeCheckerStrictLevel,
)
from ._common import isstring


class IpAddressTypeCheckerStrictLevel0(TypeCheckerStrictLevel):

    def is_instance(self):
        return self._is_ipaddress(self._value)

    def is_valid_after_convert(self, converted_value):
        return self._is_ipaddress(converted_value)

    @staticmethod
    def _is_ipaddress(value):
        return isinstance(
            value, (ipaddress.IPv4Address, ipaddress.IPv6Address))


class IpAddressTypeChecker(TypeChecker):

    def __init__(self, value, strict_level):
        super(IpAddressTypeChecker, self).__init__(
            value=value,
            checker_mapping={
                0: IpAddressTypeCheckerStrictLevel0,
            },
            strict_level=strict_level)
