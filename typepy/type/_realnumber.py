# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from .._const import DefaultValue
from .._typecode import Typecode
from ._base import AbstractType


class RealNumber(AbstractType):
    """
    |result_matrix_desc|

    .. include:: matrix_realnumber_type.txt

    :py:attr:`.strict_level`
        |strict_level|
    """

    @property
    def typecode(self):
        return Typecode.REAL_NUMBER

    def __init__(self, value, strict_level=0, **kwargs):
        super(RealNumber, self).__init__(value, strict_level, **kwargs)

    def _create_type_checker(self):
        from ..checker._realnumber import RealNumberTypeChecker

        return RealNumberTypeChecker(self._data, self._strict_level)

    def _create_type_converter(self):
        from ..converter._realnumber import FloatConverter

        converter = FloatConverter(self._data, self._params)
        converter.float_class = self._params.get("float_type", DefaultValue.FLOAT_TYPE)

        return converter
