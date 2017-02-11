# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .._error import TypeConversionError
from ._interface import AbstractValueConverter


class IntegerConverter(AbstractValueConverter):

    def force_convert(self):
        try:
            return int(float(self._value))
        except (TypeError, ValueError, OverflowError):
            raise TypeConversionError(
                "failed to force_convert to int: type={}".format(
                    type(self._value)))
