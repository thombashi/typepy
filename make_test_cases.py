#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os
import sys

import typepy
from typepy import Infinity, Integer, Nan, NullString, RealNumber, StrictLevel, String


nan = float("nan")
inf = float("inf")


class Params:
    def __init__(self, stream):
        self.__stream = stream
        self.strict_level = None
        self.typeclass = None

    def __del__(self):
        if self.__stream:
            self.__stream.close()
            self.__stream = None

    def write_test_params(self, method, value):
        if isinstance(value, str):
            write_value = f'"{value:s}"'
        else:
            write_value = value

        self.__stream.write(
            '["{:s}", {:d}, {}, {}],\n'.format(
                method, self.strict_level, write_value, self.__exeute_method(method, value)
            )
        )

    def __exeute_method(self, method, value):
        try:
            result = getattr(self.typeclass(value, self.strict_level), method)()
            if method == "validate":
                result = "-"
        except (TypeError, typepy.TypeConversionError):
            return '"E"'

        # for string tests
        if NullString(result, StrictLevel.MAX).is_type():
            return '""'

        strict_level = StrictLevel.MAX

        typeobj = Integer(result, strict_level)
        if typeobj.is_type():
            return typeobj.convert()

        typeobj = RealNumber(result, strict_level)
        if typeobj.is_type():
            return typeobj.convert()

        if String(result, strict_level).is_type():
            return f'"{result}"'

        if Infinity(result, strict_level).is_type():
            return '"inf"'

        if Nan(result, strict_level).is_type():
            return '"nan"'

        return result


class TestParamWriter:
    METHOD_LIST = (
        # "is_type",
        # "validate",
        "convert",
        "try_convert",
        "force_convert",
    )

    class Bool:
        VALUE_LIST = [True, "true", 1, 1.1, None]

    class String:
        VALUE_LIST = ["abc", "", 1, "-1", None, True, inf, nan]

    class Number:
        VALUE_LIST = [
            1,
            1.0,
            1.1,
            "0",
            "1.0",
            "1.1",
            sys.maxsize,
            "1,000,000,000,000",
            True,
            None,
            inf,
            nan,
            "test",
            "",
        ]

    def __init__(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.__writer = Params(open(file_path, "w"))

    def write_bool_tests(self):
        self.__writer.typeclass = typepy.Bool

        for method in self.METHOD_LIST:
            for strict_level in (0, 1, 2):
                self.__writer.strict_level = strict_level
                for value in self.Bool.VALUE_LIST:
                    self.__writer.write_test_params(method, value)

    def write_string_tests(self):
        self.__writer.typeclass = typepy.String

        for method in self.METHOD_LIST:
            for strict_level in (0, 1, 2):
                self.__writer.strict_level = strict_level
                for value in self.String.VALUE_LIST:
                    self.__writer.write_test_params(method, value)

    def write_integer_tests(self):
        self.__writer.typeclass = typepy.Integer

        for method in self.METHOD_LIST:
            for strict_level in (0, 1, 2):
                self.__writer.strict_level = strict_level
                for value in self.Number.VALUE_LIST:
                    self.__writer.write_test_params(method, value)

    def write_realnumber_tests(self):
        self.__writer.typeclass = typepy.RealNumber

        for method in self.METHOD_LIST:
            for strict_level in (0, 1, 2):
                self.__writer.strict_level = strict_level
                for value in self.Number.VALUE_LIST:
                    self.__writer.write_test_params(method, value)


if __name__ == "__main__":
    writer = TestParamWriter("test_cases/integer.txt")
    writer.write_integer_tests()

    writer = TestParamWriter("test_cases/bool.txt")
    writer.write_bool_tests()

    writer = TestParamWriter("test_cases/realnumber.txt")
    writer.write_realnumber_tests()

    writer = TestParamWriter("test_cases/string.txt")
    writer.write_string_tests()
