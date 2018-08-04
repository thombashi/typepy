# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

from .._typecode import Typecode
from ..checker import BinaryTypeChecker
from ..converter import BinaryConverter
from ._base import AbstractType


class Binary(AbstractType):
    """
    |result_matrix_desc|

    :py:attr:`.strict_level`
        |strict_level|
    """

    @property
    def typecode(self):
        return Typecode.STRING

    def __init__(self, value, strict_level=1, **kwargs):
        super(Binary, self).__init__(value, strict_level, kwargs)

    def _create_type_checker(self):
        return BinaryTypeChecker(self._data, self._strict_level)

    def _create_type_converter(self):
        return BinaryConverter(self._data)
