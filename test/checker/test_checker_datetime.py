"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
from datetime import date, datetime

import pytest
from dateutil.tz import tzoffset
from termcolor import colored

from typepy import DateTime, StrictLevel, Typecode


dateutil = pytest.importorskip("dateutil", minversion="2.7")

class_under_test = DateTime
nan = float("nan")
inf = float("inf")


class Test_DateTime_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(
            itertools.product(
                [datetime(2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400)), date(2017, 3, 22)],
                [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
                [True],
            )
        )
        + list(
            itertools.product(
                [None, "invalid time string", 9223372036854775807, "100-0004", "テスト".encode(),],
                [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
                [False],
            )
        )
        + list(
            itertools.product(
                ["2017-03-22T10:00:00+0900", 1485685623, "1485685623", "1524930937.003555"],
                [StrictLevel.MIN],
                [True],
            )
        )
        + list(
            itertools.product(
                ["2017-03-22T10:00:00+0900", 1485685623, "1485685623"], [StrictLevel.MAX], [False],
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_object = class_under_test(value, strict_level)

        assert type_object.is_type() == expected
        assert type_object.typecode == Typecode.DATETIME

    @pytest.mark.parametrize(
        ["value", "strip_ansi_escape", "expected"],
        [
            [colored("2017-03-22T10:00:00", "red"), False, False],
            [colored("2017-03-22T10:00:00", "red"), True, True],
        ],
    )
    def test_normal_ansi(self, value, strip_ansi_escape, expected):
        type_checker = class_under_test(value, StrictLevel.MIN, strip_ansi_escape=strip_ansi_escape)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.DATETIME
