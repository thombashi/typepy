"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys
from decimal import Decimal

import pytest
from tcolorpy import tcolor

from typepy import RealNumber, StrictLevel, Typecode


class_under_test = RealNumber
nan = float("nan")
inf = float("inf")


class Test_RealNumber_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(
            itertools.product(
                [
                    0,
                    0.0,
                    0.0,
                    sys.maxsize,
                    -sys.maxsize,
                    str(sys.maxsize),
                    str(-sys.maxsize),
                    "0.1",
                    "-0.1",
                    "1e-05",
                    "4.5e-4",
                    "45e76",
                    int(Decimal("45e765")),
                ],
                [StrictLevel.MIN],
                [True],
            )
        )
        + list(
            itertools.product(
                [0, 0.0, 0.0, sys.maxsize, -sys.maxsize, "4.5e444"], [StrictLevel.MIN + 1], [False]
            )
        )
        + list(itertools.product(["1.1", "4.5e-4"], [StrictLevel.MIN + 1], [True]))
        + list(
            itertools.product(
                [
                    0,
                    0.0,
                    Decimal("1"),
                    sys.maxsize,
                    -sys.maxsize,
                    "1.0",
                    str(sys.maxsize),
                    str(-sys.maxsize),
                    "0.1",
                    "-0.1",
                    "1e-05",
                ],
                [StrictLevel.MAX],
                [False],
            )
        )
        + list(
            itertools.product(
                [True, inf, nan, "", "0xf", "テスト".encode()],
                [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
                [False],
            )
        )
        + list(
            itertools.product(
                [0.1, -0.1, 0.5, Decimal("1.1")],
                [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
                [True],
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = class_under_test(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.REAL_NUMBER

    @pytest.mark.parametrize(
        ["value", "strip_ansi_escape", "expected"],
        [[tcolor("1.1", "red"), False, False], [tcolor("1.1", "red"), True, True]],
    )
    def test_normal_ansi(self, value, strip_ansi_escape, expected):
        type_checker = class_under_test(value, StrictLevel.MIN, strip_ansi_escape=strip_ansi_escape)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.REAL_NUMBER
