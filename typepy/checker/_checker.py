# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc

from ._interface import TypeCheckerInterface


class CheckerCreator(object):
    __slots__ = ("__min_strict_level", "__max_strict_level", "__value", "__checker_mapping")

    @property
    def min_strict_level(self):
        return self.__min_strict_level

    @property
    def max_strict_level(self):
        return self.__max_strict_level

    def __init__(self, value, checker_mapping):
        self.__value = value
        self.__checker_mapping = checker_mapping

        self.__min_strict_level = min(checker_mapping)
        self.__max_strict_level = max(checker_mapping)
        self.__checker_mapping[None] = self.__max_strict_level

    def create(self, strict_level=None):
        checker_class = self.__checker_mapping.get(strict_level)
        if not checker_class:
            if strict_level < self.min_strict_level:
                checker_class = self.__checker_mapping[self.min_strict_level]
            if strict_level > self.max_strict_level:
                checker_class = self.__checker_mapping[self.max_strict_level]

        return checker_class(self.__value)


class CheckerFactory(object):
    __slots__ = ("__min_strict_level", "__max_strict_level", "__checker_mapping")

    @property
    def min_strict_level(self):
        return self.__min_strict_level

    @property
    def max_strict_level(self):
        return self.__max_strict_level

    def __init__(self, checker_mapping):
        self.__checker_mapping = checker_mapping

        self.__min_strict_level = min(checker_mapping)
        self.__max_strict_level = max(checker_mapping)
        self.__checker_mapping[None] = self.__max_strict_level

    def get_checker_class(self, strict_level=None):
        checker_class = self.__checker_mapping.get(strict_level)
        if checker_class:
            return checker_class
        if strict_level < self.min_strict_level:
            return self.__checker_mapping[self.min_strict_level]
        if strict_level > self.max_strict_level:
            return self.__checker_mapping[self.max_strict_level]

        raise ValueError("unexpected strict level: {}".format(strict_level))


class TypeCheckerStrictLevel(TypeCheckerInterface):
    __slots__ = ("_value",)

    def __init__(self, value):
        self._value = value

    @abc.abstractmethod
    def is_instance(self):
        pass

    def is_type(self):
        return self.is_instance() and not self.is_exclude_instance()

    def validate(self):
        """
        :raises TypeError:
            If the value is not matched the type to be expected.
        """

        if self.is_type():
            return

        raise TypeError("invalid value type: actual={}".format(type(self._value)))

    def is_exclude_instance(self):
        return False

    def is_valid_after_convert(self, converted_value):
        return True


class TypeChecker(TypeCheckerInterface):
    __slots__ = ("__checker",)

    def __init__(self, value, checker_factory, strict_level):
        self.__checker = checker_factory.get_checker_class(strict_level)(value)

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
