# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class BinaryConverter(AbstractValueConverter):
    def force_convert(self):
        raise TypeConversionError("not inmplemented")
