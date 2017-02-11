# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

from decimal import Decimal
import itertools

import pytest
from pytypeutil import (
    Typecode,
    StrictLevel,
)
from pytypeutil.type import Integer
import six


nan = float("nan")
inf = float("inf")


class Test_Integer_is_type:

    @pytest.mark.parametrize(["value", "strict_level", "expected"], [
        [str(six.MAXSIZE), StrictLevel.MIN, True],
        [str(six.MAXSIZE), StrictLevel.MIN + 1, True],
        [str(six.MAXSIZE), StrictLevel.MAX, False],
        [" 1 ", StrictLevel.MIN + 1, True],
        [True, StrictLevel.MIN + 1, False],
        [False, StrictLevel.MAX, False],
    ] + list(itertools.product(
        [0, six.MAXSIZE, -six.MAXSIZE, Decimal("1")],
        [StrictLevel.MIN, StrictLevel.MIN + 1],
        [True],
    )) + list(itertools.product(
        [
            0.5, .999, Decimal("1.1"), 1e-05, -1e-05,
            "0.5", ".999", "1e-05", "-1e-05",
            True, False,
        ],
        [StrictLevel.MIN],
        [True],
    )) + list(itertools.product(
        [
            None, nan, inf,
            "", "0xff", "test", "1a1", "11a", "a11",
        ],
        [StrictLevel.MIN,  StrictLevel.MAX],
        [False],
    )))
    def test_normal(self, value, strict_level, expected):
        type_checker = Integer(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.INTEGER
