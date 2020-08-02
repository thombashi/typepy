"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from decimal import Decimal

import pytest

import typepy

from ._common import EXCEPTION_RESULT, convert_wrapper


nan = float("nan")
inf = float("inf")


class Test_RealNumber:
    @pytest.mark.parametrize(
        ["method", "strict_level", "value", "expected"],
        [
            ["convert", 0, 1, Decimal("1")],
            ["convert", 0, 1.0, Decimal("1.0")],
            ["convert", 0, 1.1, Decimal("1.1")],
            ["convert", 0, "0", Decimal("0")],
            ["convert", 0, "1.0", Decimal("1.0")],
            ["convert", 0, "1.1", Decimal("1.1")],
            ["convert", 0, True, EXCEPTION_RESULT],
            ["convert", 0, None, EXCEPTION_RESULT],
            ["convert", 0, inf, EXCEPTION_RESULT],
            ["convert", 0, nan, EXCEPTION_RESULT],
            ["convert", 0, "test", EXCEPTION_RESULT],
            ["convert", 0, "", EXCEPTION_RESULT],
            ["convert", 1, 1, EXCEPTION_RESULT],
            ["convert", 1, 1.0, EXCEPTION_RESULT],
            ["convert", 1, 1.1, Decimal("1.1")],
            ["convert", 1, "0", EXCEPTION_RESULT],
            ["convert", 1, "1.0", EXCEPTION_RESULT],
            ["convert", 1, "1.1", Decimal("1.1")],
            ["convert", 1, True, EXCEPTION_RESULT],
            ["convert", 1, None, EXCEPTION_RESULT],
            ["convert", 1, inf, EXCEPTION_RESULT],
            ["convert", 1, nan, EXCEPTION_RESULT],
            ["convert", 1, "test", EXCEPTION_RESULT],
            ["convert", 1, "", EXCEPTION_RESULT],
            ["convert", 2, 1, EXCEPTION_RESULT],
            ["convert", 2, 1.0, EXCEPTION_RESULT],
            ["convert", 2, 1.1, Decimal("1.1")],
            ["convert", 2, "0", EXCEPTION_RESULT],
            ["convert", 2, "1.0", EXCEPTION_RESULT],
            ["convert", 2, "1.1", EXCEPTION_RESULT],
            ["convert", 2, True, EXCEPTION_RESULT],
            ["convert", 2, None, EXCEPTION_RESULT],
            ["convert", 2, inf, EXCEPTION_RESULT],
            ["convert", 2, nan, EXCEPTION_RESULT],
            ["convert", 2, "test", EXCEPTION_RESULT],
            ["convert", 2, "", EXCEPTION_RESULT],
            ["try_convert", 0, 1, Decimal("1")],
            ["try_convert", 0, 1.0, Decimal("1.0")],
            ["try_convert", 0, 1.1, Decimal("1.1")],
            ["try_convert", 0, "0", Decimal("0")],
            ["try_convert", 0, "1.0", Decimal("1.0")],
            ["try_convert", 0, "1.1", Decimal("1.1")],
            ["try_convert", 0, True, None],
            ["try_convert", 0, None, None],
            ["try_convert", 0, inf, None],
            ["try_convert", 0, nan, None],
            ["try_convert", 0, "test", None],
            ["try_convert", 0, "", None],
            ["try_convert", 1, 1, None],
            ["try_convert", 1, 1.0, None],
            ["try_convert", 1, 1.1, Decimal("1.1")],
            ["try_convert", 1, "0", None],
            ["try_convert", 1, "1.0", None],
            ["try_convert", 1, "1.1", Decimal("1.1")],
            ["try_convert", 1, True, None],
            ["try_convert", 1, None, None],
            ["try_convert", 1, inf, None],
            ["try_convert", 1, nan, None],
            ["try_convert", 1, "test", None],
            ["try_convert", 1, "", None],
            ["try_convert", 2, 1, None],
            ["try_convert", 2, 1.0, None],
            ["try_convert", 2, 1.1, Decimal("1.1")],
            ["try_convert", 2, "0", None],
            ["try_convert", 2, "1.0", None],
            ["try_convert", 2, "1.1", None],
            ["try_convert", 2, True, None],
            ["try_convert", 2, None, None],
            ["try_convert", 2, inf, None],
            ["try_convert", 2, nan, None],
            ["try_convert", 2, "test", None],
            ["try_convert", 2, "", None],
            ["force_convert", 0, 1, Decimal("1")],
            ["force_convert", 0, 1.0, Decimal("1.0")],
            ["force_convert", 0, 1.1, Decimal("1.1")],
            ["force_convert", 0, "0", Decimal("0")],
            ["force_convert", 0, "1.0", Decimal("1.0")],
            ["force_convert", 0, "1.1", Decimal("1.1")],
            ["force_convert", 0, True, Decimal("1")],
            ["force_convert", 0, None, EXCEPTION_RESULT],
            ["force_convert", 0, inf, Decimal("inf")],
            ["force_convert", 0, nan, Decimal("nan")],
            ["force_convert", 0, "test", EXCEPTION_RESULT],
            ["force_convert", 0, "", EXCEPTION_RESULT],
            ["force_convert", 1, 1, Decimal("1")],
            ["force_convert", 1, 1.0, Decimal("1.0")],
            ["force_convert", 1, 1.1, Decimal("1.1")],
            ["force_convert", 1, "0", Decimal("0")],
            ["force_convert", 1, "1.0", Decimal("1.0")],
            ["force_convert", 1, "1.1", Decimal("1.1")],
            ["force_convert", 1, True, Decimal("1")],
            ["force_convert", 1, None, EXCEPTION_RESULT],
            ["force_convert", 1, inf, Decimal("inf")],
            ["force_convert", 1, nan, Decimal("nan")],
            ["force_convert", 1, "test", EXCEPTION_RESULT],
            ["force_convert", 1, "", EXCEPTION_RESULT],
            ["force_convert", 2, 1, Decimal("1")],
            ["force_convert", 2, 1.0, Decimal("1.0")],
            ["force_convert", 2, 1.1, Decimal("1.1")],
            ["force_convert", 2, "0", Decimal("0")],
            ["force_convert", 2, "1.0", Decimal("1.0")],
            ["force_convert", 2, "1.1", Decimal("1.1")],
            ["force_convert", 2, True, Decimal("1")],
            ["force_convert", 2, None, EXCEPTION_RESULT],
            ["force_convert", 2, inf, Decimal("inf")],
            ["force_convert", 2, nan, Decimal("nan")],
            ["force_convert", 2, "test", EXCEPTION_RESULT],
            ["force_convert", 2, "", EXCEPTION_RESULT],
        ],
    )
    def test_normal(self, method, strict_level, value, expected):
        from typepy import Nan, StrictLevel

        actual = convert_wrapper(typepy.RealNumber(value, strict_level), method)
        if Nan(expected, strict_level=StrictLevel.MIN).is_type():
            assert Nan(actual, strict_level=StrictLevel.MIN).is_type()
        else:
            assert actual == expected
