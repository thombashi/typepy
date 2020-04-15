"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import json

from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class DictionaryConverter(AbstractValueConverter):
    def force_convert(self):
        try:
            return dict(self._value)
        except (TypeError, ValueError):
            pass

        if isinstance(self._value, str):
            try:
                return json.loads(self._value)
            except json.JSONDecodeError:
                pass

        raise TypeConversionError(
            "failed to force_convert to dictionary: type={}".format(type(self._value))
        )
