"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys

import pytest

from typepy import Bytes, StrictLevel, Typecode


nan = float("nan")
inf = float("inf")


class Test_Binary_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product([], [StrictLevel.MIN, StrictLevel.MAX], [False]))
        + list(
            itertools.product(
                [b"abc", "いろは".encode()], [StrictLevel.MIN, StrictLevel.MAX], [True]
            )
        )
        + list(itertools.product([b" ", b"\n"], [StrictLevel.MIN], [True]))
        + list(
            itertools.product(
                ["", " ", "\n", sys.maxsize, inf, nan, None], [StrictLevel.MAX], [False]
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = Bytes(value, strict_level=strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.BYTES
