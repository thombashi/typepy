# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools

import pytest
from six import MAXSIZE
from typepy import Binary, StrictLevel, Typecode


nan = float("nan")
inf = float("inf")


class Test_Binary_is_type(object):
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product([], [StrictLevel.MIN, StrictLevel.MAX], [False]))
        + list(
            itertools.product(
                ["abc".encode("utf_8"), "いろは".encode("utf_8")],
                [StrictLevel.MIN, StrictLevel.MAX],
                [True],
            )
        )
        + list(
            itertools.product(
                [" ".encode("utf_8"), "\n".encode("utf_8")], [StrictLevel.MIN], [True]
            )
        )
        + list(
            itertools.product(["", " ", "\n", MAXSIZE, inf, nan, None], [StrictLevel.MAX], [False])
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = Binary(value, strict_level=strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.STRING
