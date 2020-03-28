"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys

import pytest

from typepy import is_empty_sequence, is_hex, is_not_empty_sequence


nan = float("nan")
inf = float("inf")


class Test_is_hex:
    @pytest.mark.parametrize(["value"], [["0x00"], ["0xffffffff"], ["a"], ["f"]])
    def test_normal(self, value):
        assert is_hex(value)

    @pytest.mark.parametrize(
        ["value"], [[None], [nan], [inf], [0], [1], [0.5], ["test"], ["g"], [True]]
    )
    def test_abnormal(self, value):
        assert not is_hex(value)


class Test_is_empty_sequence:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [(), True],
            [[], True],
            ["", True],
            [range(0), True],
            [[1], False],
            [["a"] * 20000, False],
            [(1,), False],
            [("a",) * 20000, False],
            ["aaa", False],
            [range(0, 10), False],
            [True, False],
            [False, False],
            [sys.maxsize, False],
            [0.1, False],
            [nan, False],
            [inf, False],
        ],
    )
    def test_normal(self, value, expected):
        assert is_empty_sequence(value) == expected


class Test_is_not_empty_sequence:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [[1], True],
            [["a"] * 20000, True],
            [(1,), True],
            [("a",) * 20000, True],
            ["a" * 20000, True],
            [range(0, 10), True],
            [(), False],
            [[], False],
            [None, False],
            [range(0), False],
            [True, False],
            [False, False],
            [sys.maxsize, False],
            [0.1, False],
            [nan, False],
            [inf, False],
        ],
    )
    def test_normal(self, value, expected):
        assert is_not_empty_sequence(value) == expected
