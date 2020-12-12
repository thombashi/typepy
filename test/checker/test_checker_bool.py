"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools

import pytest
from tcolorpy import tcolor

from typepy import Bool, StrictLevel, Typecode


class_under_test = Bool
nan = float("nan")
inf = float("inf")


class Test_Bool_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product([True, False], [StrictLevel.MIN, StrictLevel.MAX], [True]))
        + list(
            itertools.product([0, 1, "True", "False", "true", "false"], [StrictLevel.MIN], [True])
        )
        + list(
            itertools.product(
                [0, 1, 0.1, "True", "False", "true", "false"], [StrictLevel.MAX], [False]
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = class_under_test(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.BOOL

    @pytest.mark.parametrize(
        ["value", "strip_ansi_escape", "expected"],
        [[tcolor("True", "red"), False, False], [tcolor("True", "red"), True, True]],
    )
    def test_normal_ansi(self, value, strip_ansi_escape, expected):
        type_checker = class_under_test(value, StrictLevel.MIN, strip_ansi_escape=strip_ansi_escape)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.BOOL
