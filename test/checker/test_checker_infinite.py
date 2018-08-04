# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools
from decimal import Decimal

import pytest
import six
from typepy import Infinity, StrictLevel, Typecode


nan = float("nan")
inf = float("inf")


class Test_Infinity_is_type(object):
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(
            itertools.product(
                [0.0, six.MAXSIZE, "0", nan, None], [StrictLevel.MIN, StrictLevel.MAX], [False]
            )
        )
        + list(
            itertools.product(
                [inf, Decimal("infinity")], [StrictLevel.MIN, StrictLevel.MAX], [True]
            )
        )
        + [
            ["inf", StrictLevel.MIN, True],
            ["inf", StrictLevel.MAX, False],
            ["-infinity", StrictLevel.MIN, True],
            ["-infinity", StrictLevel.MAX, False],
            ["INF", StrictLevel.MIN, True],
            ["INF", StrictLevel.MAX, False],
        ],
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = Infinity(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.INFINITY
