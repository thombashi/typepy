"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from decimal import Decimal, InvalidOperation

from .._common import strip_ansi_escape
from .._const import DefaultValue, ParamKey
from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class IntegerConverter(AbstractValueConverter):
    def force_convert(self):
        try:
            return int(Decimal(self._value))
        except (TypeError, OverflowError, ValueError, InvalidOperation):
            pass

        if self._params.get(ParamKey.STRIP_ANSI_ESCAPE, DefaultValue.STRIP_ANSI_ESCAPE):
            try:
                return int(Decimal(strip_ansi_escape(self._value)))
            except (TypeError, OverflowError, ValueError, InvalidOperation):
                pass

        raise TypeConversionError(
            "failed to force_convert to int: type={}".format(type(self._value))
        )
