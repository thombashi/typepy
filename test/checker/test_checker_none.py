"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys

import pytest

from typepy import NoneType, StrictLevel, Typecode


nan = float("nan")
inf = float("inf")


class Test_NoneTypeChecker_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product([None], [StrictLevel.MIN, StrictLevel.MAX], [True]))
        + list(
            itertools.product(
                ["None", True, False, 0, sys.maxsize, inf, nan],
                [StrictLevel.MIN, StrictLevel.MAX],
                [False],
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        expected_typecode = Typecode.NONE

        typeobj = NoneType(value, strict_level)

        assert typeobj.is_type() == expected
        assert typeobj.typecode == expected_typecode
