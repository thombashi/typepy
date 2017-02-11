# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import abc

from .._typecode import Typecode
from ._interface import TypeCheckerInterface


class CheckerCreator(object):

    @property
    def min_strict_level(self):
        return min(self.__checker_mapping)

    @property
    def max_strict_level(self):
        return max(self.__checker_mapping)

    def __init__(self, type_object, value, checker_mapping):
        self.__type_object = type_object
        self.__value = value
        self.__checker_mapping = checker_mapping

    def create(self, strict_level=None):
        if strict_level is None:
            strict_level = self.max_strict_level
        elif strict_level < self.min_strict_level:
            strict_level = self.min_strict_level
        elif strict_level > self.max_strict_level:
            strict_level = self.max_strict_level

        return self.__checker_mapping.get(strict_level)(
            self.__type_object, self.__value)


class TypeCheckerStrictLevel(TypeCheckerInterface):
    __slots__ = ("_value", )

    def __init__(self, type_object, value):
        self.__type_object = type_object
        self._value = value

    @abc.abstractmethod
    def is_instance(self):
        pass

    def is_type(self):
        return all([
            self.is_instance(),
            not self.is_exclude_instance()
        ])

    def validate(self):
        """
        :raises TypeError:
            If the value is not matched the type to be expected.
        """

        if self.is_type():
            return

        raise TypeError(
            "invalid value type: expected={}, actual={}".format(
                Typecode.get_typename(self.typecode), type(self._value)))

    def is_exclude_instance(self):
        return False

    def is_valid_after_convert(self, converted_value):
        return True


class TypeChecker(TypeCheckerInterface):

    def __init__(self, value, checker_mapping, strict_level):
        self.__checker = CheckerCreator(
            self,
            value=value,
            checker_mapping=checker_mapping).create(strict_level)

    def is_type(self):
        return self.__checker.is_type()

    def is_valid_after_convert(self, value):
        return self.__checker.is_valid_after_convert(value)

    def is_instance(self):
        return self.__checker.is_instance()

    def is_exclude_instance(self):
        return self.__checker.is_exclude_instance()

    def validate(self):
        self.__checker.validate()
