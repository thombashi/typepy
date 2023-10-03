#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import argparse
import ipaddress
import os
import sys
from datetime import datetime

import logbook
import pytablewriter as ptw

import typepy
from typepy import (
    Bool,
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
)


logbook.StderrHandler(
    level=logbook.DEBUG, format_string="[{record.level_name}] {record.channel}: {record.message}"
).push_application()

METHOD_HEADER = "Method"


class ExampleWriter:
    _METHOD_LIST = ("is_type", "validate", "convert", "try_convert", "force_convert")


class ResultMatrixWriter(ExampleWriter):
    def __init__(self):
        self.typeclass = None
        self.strict_level = None
        self.headers = None
        self.value_list = None

        self.__table_writer = ptw.RstSimpleTableWriter()
        self.__table_writer._dp_extractor.type_value_map = {
            NullString(None).typecode: '``""``',
            NoneType(None).typecode: "``None``",
            Infinity(None).typecode: '``Decimal("inf")``',
            Nan(None).typecode: '``Decimal("nan")``',
        }
        self.__table_writer.value_map = {
            True: "``True``",
            False: "``False``",
            '``"127.0.0.1"``': '``ip_address("127.0.0.1")``',
        }

    def set_stream(self, output_stream):
        self.__table_writer.stream = output_stream

    def write_type_matrix(self):
        tbl_template = ":py:class:`typepy.{0:s}`: :py:attr:`~typepy.{0:s}.strict_level` = {1:d}"
        self.__table_writer.table_name = tbl_template.format(
            self.typeclass.__name__, self.strict_level
        )
        self.__table_writer.headers = self.headers
        self.__table_writer.value_matrix = self.__get_result_matrix()
        if self.typeclass.__name__ in ["Dictionary", "List"]:
            self.__table_writer.type_hints = [String for _ in self.headers]

        self.__table_writer.write_table()
        self.__table_writer.write_null_line()

    def exeute(self, method, value):
        str_convert_type = (str, ipaddress.IPv4Address, ipaddress.IPv6Address)

        try:
            result = getattr(self.typeclass(value, self.strict_level), method)()

            if method == "validate":
                result = "NOP [#f1]_"
            elif isinstance(result, str_convert_type):
                result = f'``"{result}"``'
        except TypeError:
            result = "E [#f2]_"
        except typepy.TypeConversionError:
            result = "E [#f3]_"

        return result

    def __get_result_matrix(self):
        result_matrix = []
        for method in self._METHOD_LIST:
            result_matrix.append(
                [f":py:meth:`~.type.{self.typeclass.__name__:s}.{method:s}`"]
                + [self.exeute(method, value) for value in self.value_list]
            )

        return result_matrix


class ResultMatrixManager:
    class ExampleBool:
        HEADER = [METHOD_HEADER] + ["``True``", '``"true"``', 1]
        VALUE = [True, "true", 1]

    class ExampleString:
        HEADER = [METHOD_HEADER] + ['``"abc"``', '``""``', '``"  "``', "``None``", "``1``"]
        VALUE = ["abc", "", "  ", None, 1]

    class ExampleNumber:
        HEADER = [METHOD_HEADER] + [
            "``1``",
            "``1.0``",
            "``1.1``",
            '``"1"``',
            '``"1.0"``',
            '``"1.1"``',
            "``True``",
        ]
        VALUE = [1, 1.0, 1.1, "1", "1.0", "1.1", True]

    class ExampleInfinity:
        HEADER = [METHOD_HEADER] + ['``float("inf")``', '``"Infinity"``', "``0.1``"]
        VALUE = [float("inf"), "Infinity", 0.1]

    class ExampleNan:
        HEADER = [METHOD_HEADER] + ['``float("nan")``', '``"NaN"``', "``0.1``"]
        VALUE = [float("nan"), "NaN", 0.1]

    class ExampleDateTime:
        HEADER = [METHOD_HEADER] + [
            "``datetime(2017, 1, 23, 4, 56)``",
            '``"2017-01-22T04:56:00+0900"``',
            "``1485685623``",
            '``"1485685623"``',
        ]
        VALUE = [datetime(2017, 1, 23, 4, 56), "2017-01-22T04:56:00+0900", 1485685623, "1485685623"]

    class ExampleIpAddress:
        HEADER = [METHOD_HEADER] + [
            "``ip_address('127.0.0.1')``",
            "``'127.0.0.1'``",
            "``'::1'``",
            "``'192.168.0.256'``",
            "``None``",
        ]
        VALUE = [ipaddress.ip_address("127.0.0.1"), "127.0.0.1", "::1", "192.168.0.256", None]

    class ExampleList:
        HEADER = [METHOD_HEADER] + [
            "``[]``",
            '``["a", "b"]``',
            '``("a", "b")``',
            '``{"a": 1}``',
            '``"abc"``',
        ]
        VALUE = [[], ["a", "b"], ("a", "b"), {"a": 1}, "abc"]

    class ExampleDictionary:
        HEADER = [METHOD_HEADER] + ["``{}``", '``{"a": 1}``', '``(("a", 1), )``']
        VALUE = [{}, {"a": 1}, (("a", 1),)]

    def __init__(self):
        self.strict_level_list = None

        self.__ewriter = ResultMatrixWriter()

    def set_stream(self, output_stream):
        self.__ewriter.set_stream(output_stream)

    def write_none(self):
        self.__ewriter.typeclass = NoneType
        self.__ewriter.headers = self.ExampleString.HEADER
        self.__ewriter.value_list = self.ExampleString.VALUE
        self.__write()

    def write_ipaddress(self):
        self.__ewriter.typeclass = IpAddress
        self.__ewriter.headers = self.ExampleIpAddress.HEADER
        self.__ewriter.value_list = self.ExampleIpAddress.VALUE
        self.__write()

    def write_bool(self):
        self.__ewriter.typeclass = Bool
        self.__ewriter.headers = self.ExampleBool.HEADER
        self.__ewriter.value_list = self.ExampleBool.VALUE
        self.__write()

    def write_string(self):
        self.__ewriter.typeclass = String
        self.__ewriter.headers = self.ExampleString.HEADER
        self.__ewriter.value_list = self.ExampleString.VALUE
        self.__write()

    def write_null_string(self):
        self.__ewriter.typeclass = NullString
        self.__ewriter.headers = self.ExampleString.HEADER
        self.__ewriter.value_list = self.ExampleString.VALUE
        self.__write()

    def write_integer(self):
        self.__ewriter.typeclass = Integer
        self.__ewriter.headers = self.ExampleNumber.HEADER
        self.__ewriter.value_list = self.ExampleNumber.VALUE
        self.__write()

    def write_realnumber(self):
        self.__ewriter.typeclass = RealNumber
        self.__ewriter.headers = self.ExampleNumber.HEADER
        self.__ewriter.value_list = self.ExampleNumber.VALUE
        self.__write()

    def write_infinity(self):
        self.__ewriter.typeclass = Infinity
        self.__ewriter.headers = self.ExampleInfinity.HEADER
        self.__ewriter.value_list = self.ExampleInfinity.VALUE
        self.__write()

    def write_nan(self):
        self.__ewriter.typeclass = Nan
        self.__ewriter.headers = self.ExampleNan.HEADER
        self.__ewriter.value_list = self.ExampleNan.VALUE
        self.__write()

    def write_datetime(self):
        self.__ewriter.typeclass = DateTime
        self.__ewriter.headers = self.ExampleDateTime.HEADER
        self.__ewriter.value_list = self.ExampleDateTime.VALUE
        self.__write()

    def write_list(self):
        self.__ewriter.typeclass = List
        self.__ewriter.headers = self.ExampleList.HEADER
        self.__ewriter.value_list = self.ExampleList.VALUE
        self.__write()

    def write_dictionary(self):
        self.__ewriter.typeclass = Dictionary
        self.__ewriter.headers = self.ExampleDictionary.HEADER
        self.__ewriter.value_list = self.ExampleDictionary.VALUE
        self.__write()

    def __write(self):
        for strict_level in self.strict_level_list:
            self.__ewriter.strict_level = strict_level
            self.__ewriter.write_type_matrix()


class PathMaker:
    def __init__(self, output_dir, encoding="utf8"):
        self.__output_dir = output_dir
        self.__encoding = encoding

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def open_write(self, filename):
        file_path = os.path.join(self.__output_dir, filename)
        print(file_path)

        return open(file_path, "w", encoding=self.__encoding)


def parse_option():
    parser = argparse.ArgumentParser()

    parser.add_argument("--type", choices=["reference", "example"])

    parser.add_argument(
        "-o", "--output-dir", default=".", required=True, help="default=%(default)s"
    )

    return parser.parse_args()


def make_filename(name, prefix="matrix_", suffix="_type", extension=".txt"):
    return f"{prefix:s}{name:s}{suffix:s}{extension:s}"


def write_result_matrix(output_dir_path):
    manager = ResultMatrixManager()
    opener = PathMaker(output_dir_path)

    manager.strict_level_list = (0,)
    with opener.open_write(make_filename("none")) as f:
        manager.set_stream(f)
        manager.write_none()

    manager.strict_level_list = (0, 1)
    with opener.open_write(make_filename("ipaddress")) as f:
        manager.set_stream(f)
        manager.write_ipaddress()

    with opener.open_write(make_filename("infinity")) as f:
        manager.set_stream(f)
        manager.write_infinity()

    with opener.open_write(make_filename("nan")) as f:
        manager.set_stream(f)
        manager.write_nan()

    with opener.open_write(make_filename("list")) as f:
        manager.set_stream(f)
        manager.write_list()

    with opener.open_write(make_filename("dictionary")) as f:
        manager.set_stream(f)
        manager.write_dictionary()

    with opener.open_write(make_filename("nullstring")) as f:
        manager.set_stream(f)
        manager.write_null_string()

    manager.strict_level_list = (0, 1, 2)
    with opener.open_write(make_filename("bool")) as f:
        manager.set_stream(f)
        manager.write_bool()

    with opener.open_write(make_filename("datetime")) as f:
        manager.set_stream(f)
        manager.write_datetime()

    with opener.open_write(make_filename("integer")) as f:
        manager.set_stream(f)
        manager.write_integer()

    with opener.open_write(make_filename("realnumber")) as f:
        manager.set_stream(f)
        manager.write_realnumber()

    with opener.open_write(make_filename("string")) as f:
        manager.set_stream(f)
        manager.write_string()


def write_example(output_dir_path):
    opener = PathMaker(output_dir_path)  # noqa


def main():
    options = parse_option()

    write_result_matrix(options.output_dir)
    write_example(options.output_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
