"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._common import strip_ansi_escape
from .._const import DefaultValue, ParamKey
from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class BoolConverter(AbstractValueConverter):
    def force_convert(self):
        if isinstance(self._value, int):
            return bool(self._value)

        try:
            return self.__strict_strtobool(self._value)
        except ValueError:
            pass

        if self._params.get(ParamKey.STRIP_ANSI_ESCAPE, DefaultValue.STRIP_ANSI_ESCAPE):
            try:
                return self.__strict_strtobool(strip_ansi_escape(self._value))
            except (TypeError, ValueError):
                pass

        raise TypeConversionError(
            "failed to force_convert to bool: type={}".format(type(self._value))
        )

    @staticmethod
    def __strict_strtobool(value):
        from distutils.util import strtobool

        if isinstance(value, bool):
            return value

        try:
            lower_text = value.lower()
        except AttributeError:
            raise ValueError("invalid value '{}'".format(str(value)))

        binary_value = strtobool(lower_text)
        if lower_text not in ["true", "false"]:
            raise ValueError("invalid value '{}'".format(str(value)))

        return bool(binary_value)
