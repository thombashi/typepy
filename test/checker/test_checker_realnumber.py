# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools
from decimal import Decimal

import pytest
import six
from six import text_type
from termcolor import colored
from typepy import RealNumber, StrictLevel, Typecode


class_under_test = RealNumber
nan = float("nan")
inf = float("inf")


class Test_RealNumber_is_type(object):
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(
            itertools.product(
                [
                    0,
                    0.0,
                    0.0,
                    six.MAXSIZE,
                    -six.MAXSIZE,
                    text_type(six.MAXSIZE),
                    text_type(-six.MAXSIZE),
                    "0.1",
                    "-0.1",
                    "1e-05",
                ],
                [StrictLevel.MIN],
                [True],
            )
        )
        + list(itertools.product([True, inf, nan, "", "0xf"], [StrictLevel.MIN], [False]))
        + list(
            itertools.product(
                [0, 0.0, 0.0, six.MAXSIZE, -six.MAXSIZE], [StrictLevel.MIN + 1], [False]
            )
        )
        + list(
            itertools.product(
                [
                    0,
                    0.0,
                    Decimal("1"),
                    six.MAXSIZE,
                    -six.MAXSIZE,
                    "1.0",
                    text_type(six.MAXSIZE),
                    text_type(-six.MAXSIZE),
                    "0.1",
                    "-0.1",
                    "1e-05",
                ],
                [StrictLevel.MAX],
                [False],
            )
        )
        + list(
            itertools.product(
                [0.1, -0.1, 0.5, Decimal("1.1")],
                [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
                [True],
            )
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = class_under_test(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.REAL_NUMBER

    @pytest.mark.parametrize(
        ["value", "strip_ansi_escape", "expected"],
        [[colored("1.1", "red"), False, False], [colored("1.1", "red"), True, True]],
    )
    def test_normal_ansi(self, value, strip_ansi_escape, expected):
        type_checker = class_under_test(value, StrictLevel.MIN, strip_ansi_escape=strip_ansi_escape)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.REAL_NUMBER
