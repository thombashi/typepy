# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import six

from .._common import strip_ansi_escape
from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class IpAddressConverter(AbstractValueConverter):
    def force_convert(self):
        import ipaddress

        value = six.text_type(self._value)

        try:
            return ipaddress.ip_address(value)
        except ValueError:
            pass

        try:
            return ipaddress.ip_address(strip_ansi_escape(value))
        except ValueError:
            raise TypeConversionError(
                "failed to force_convert to dictionary: type={}".format(type(self._value))
            )
