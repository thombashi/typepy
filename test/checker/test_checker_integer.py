"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys
from decimal import Decimal

import pytest
from termcolor import colored

from typepy import Integer, StrictLevel, Typecode


class_under_test = Integer
nan = float("nan")
inf = float("inf")


class Test_Integer_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        [
            [str(sys.maxsize), StrictLevel.MIN, True],
            [str(sys.maxsize), StrictLevel.MIN + 1, True],
            [str(sys.maxsize), StrictLevel.MAX, False],
            ["45e76582", StrictLevel.MIN, True],
            ["45e76582", StrictLevel.MIN + 1, False],
            ["45e76582", StrictLevel.MAX, False],
            ["4.5e-4", StrictLevel.MIN, True],
            ["4.5e-4", StrictLevel.MIN + 1, False],
            ["4.5e-4", StrictLevel.MAX, False],
            [" 1 ", StrictLevel.MIN + 1, True],
            [True, StrictLevel.MIN + 1, False],
            [False, StrictLevel.MAX, False],
        ]
        + list(
            itertools.product(
                [0, sys.maxsize, -sys.maxsize, Decimal("1"), int(Decimal("45e765"))],
                [StrictLevel.MIN, StrictLevel.MIN + 1],
                [True],
            )
        )
        + list(
            itertools.product(
                [
                    0.5,
                    0.999,
                    Decimal("1.1"),
                    1e-05,
                    -1e-05,
                    "0.5",
                    ".999",
                    "1e-05",
                    "-1e-05",
                    True,
                    False,
                ],
                [StrictLevel.MIN],
                [True],
            )
        )
        + list(
            itertools.product(
                [None, nan, inf, "", "0xff", "test", "1a1", "11a", "a11", "テスト".encode()],
                [StrictLevel.MIN, StrictLevel.MAX],
                [False],
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = class_under_test(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.INTEGER

    @pytest.mark.parametrize(
        ["value", "strip_ansi_escape", "expected"],
        [[colored("1", "red"), False, False], [colored("1", "red"), True, True]],
    )
    def test_normal_ansi(self, value, strip_ansi_escape, expected):
        type_checker = class_under_test(value, StrictLevel.MIN, strip_ansi_escape=strip_ansi_escape)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.INTEGER
