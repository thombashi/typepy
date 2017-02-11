# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import abc

from .._error import TypeConversionError
from .._typecode import Typecode
from ..checker._interface import TypeCheckerInterface
from ..converter import ValueConverterInterface


class AbstractType(TypeCheckerInterface, ValueConverterInterface):
    """
    .. py:attribute:: hogehoge

        hogehogehogehogehogehoge
    """

    __slots__ = (
        "_data", "_strict_level", "_params",
        "__checker", "__converter",
    )

    @abc.abstractproperty
    def typecode(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _create_type_checker(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _create_type_converter(self):  # pragma: no cover
        pass

    @property
    def typename(self):
        return Typecode.get_typename(self.typecode)

    def __init__(self, value, strict_level, params=None):
        self._data = value
        self._strict_level = strict_level

        if params is None:
            self._params = {}
        else:
            self._params = params

        self.__checker = self._create_type_checker()
        self.__converter = self._create_type_converter()

    def __repr__(self):
        element_list = [
            "is_type={}".format(self.is_type()),
            "strict_level={}".format(self._strict_level),
            "try_convert={}".format(self.try_convert()),
        ]

        return ", ".join(element_list)

    def is_type(self):
        """
        :return:
        :rtype: bool
        """

        if self.__checker.is_type():
            return True

        if self.__checker.is_exclude_instance():
            return False

        try:
            self._converted_value = self.__converter.force_convert()
        except TypeConversionError:
            return False

        if not self.__checker.is_valid_after_convert(self._converted_value):
            return False

        return True

    def validate(self):
        """
        :raises TypeError:
            If the value is not matched the type that the class represented.
        """

        if self.is_type():
            return

        raise TypeError(
            "invalid value type: expected={}, actual={}".format(
                Typecode.get_typename(self.typecode), type(self._data)))

    def force_convert(self):
        """
        :return: Converted value.
        :raises pytypeutil.TypeConversionError:
            If the value cannot convert.
        """

        return self.__converter.force_convert()

    def convert(self):
        """
        :return: Converted value.
        :raises pytypeutil.TypeConversionError:
            If the value cannot convert.
        """

        if self.is_type():
            return self.force_convert()

        raise TypeConversionError(
            "failed to convert from {} to {}".format(
                type(self._data).__name__, self.typename))

    def try_convert(self):
        """
        :return: Converted value. |None| if failed to convert.
        """

        try:
            return self.convert()
        except TypeConversionError:
            return None
