"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._typecode import Typecode
from ._base import AbstractType


class Bool(AbstractType):
    """
    |result_matrix_desc|

    .. include:: matrix_bool_type.txt

    .. py:attribute:: strict_level

        |strict_level|
    """

    @property
    def typecode(self):
        return Typecode.BOOL

    def __init__(self, value, strict_level=2, **kwargs):
        super().__init__(value, strict_level, **kwargs)

    def _create_type_checker(self):
        from ..checker._bool import BoolTypeChecker

        return BoolTypeChecker(self._data, self._strict_level)

    def _create_type_converter(self):
        from ..converter._bool import BoolConverter

        return BoolConverter(self._data, self._params)
