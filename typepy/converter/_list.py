"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class ListConverter(AbstractValueConverter):
    def force_convert(self):
        try:
            return list(self._value)
        except (TypeError, ValueError):
            raise TypeConversionError(
                "failed to force_convert to list: type={}".format(type(self._value))
            )
