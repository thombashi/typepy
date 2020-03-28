"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys
from decimal import Decimal

import pytest

from typepy import Nan, StrictLevel, Typecode


nan = float("nan")
inf = float("inf")


class Test_Nan_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(
            itertools.product(
                [0.0, sys.maxsize, "0", inf, None], [StrictLevel.MIN, StrictLevel.MAX], [False]
            )
        )
        + list(itertools.product([nan, Decimal("NaN")], [StrictLevel.MIN, StrictLevel.MAX], [True]))
        + [
            ["nan", StrictLevel.MIN, True],
            ["nan", StrictLevel.MAX, False],
            ["-Nan", StrictLevel.MIN, True],
            ["-Nan", StrictLevel.MAX, False],
            ["NAN", StrictLevel.MIN, True],
            ["NAN", StrictLevel.MAX, False],
        ],
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = Nan(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.NAN
