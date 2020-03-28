"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._typecode import Typecode
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
        super().__init__(value, strict_level, **kwargs)

    def _create_type_checker(self):
        from ..checker import BinaryTypeChecker

        return BinaryTypeChecker(self._data, self._strict_level)

    def _create_type_converter(self):
        from ..converter import BinaryConverter

        return BinaryConverter(self._data, self._params)
