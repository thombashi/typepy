"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys

import pytest

from typepy import NullString, StrictLevel, String, Typecode


nan = float("nan")
inf = float("inf")


class Test_String_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product([], [StrictLevel.MIN, StrictLevel.MAX], [False]))
        + list(
            itertools.product(
                ["None", "いろは", "いろは".encode()], [StrictLevel.MIN, StrictLevel.MAX], [True]
            )
        )
        + list(
            itertools.product(
                ["", " ", "\n", sys.maxsize, inf, nan, None], [StrictLevel.MIN], [True]
            )
        )
        + list(
            itertools.product(
                ["", " ", "\n", sys.maxsize, inf, nan, None], [StrictLevel.MAX], [False]
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = String(value, strict_level=strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.STRING


class Test_NullString_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        [[None, StrictLevel.MIN, True]]
        + list(
            itertools.product(
                ["", " ", "\t", "\n", " \r\n"], [StrictLevel.MIN, StrictLevel.MAX], [True]
            )
        )
        + list(
            itertools.product(
                [sys.maxsize, "None", inf, "いろは", "いろは".encode()],
                [StrictLevel.MIN, StrictLevel.MAX],
                [False],
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_object = NullString(value, strict_level)

        assert type_object.is_type() == expected
        assert type_object.typecode == Typecode.NULL_STRING
