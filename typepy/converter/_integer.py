# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from decimal import Decimal, InvalidOperation

from .._common import strip_ansi_escape
from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class IntegerConverter(AbstractValueConverter):
    def force_convert(self):
        try:
            return int(Decimal(self._value))
        except (TypeError, OverflowError, ValueError, InvalidOperation):
            pass

        try:
            return int(Decimal(strip_ansi_escape(self._value)))
        except (TypeError, OverflowError, ValueError, InvalidOperation):
            pass

        raise TypeConversionError(
            "failed to force_convert to int: type={}".format(type(self._value))
        )
