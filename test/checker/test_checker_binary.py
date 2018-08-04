# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools

import pytest
import six
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
                [six.b("abc"), "いろは".encode("utf_8")], [StrictLevel.MIN, StrictLevel.MAX], [True]
            )
        )
        + list(itertools.product([six.b(""), six.b(" "), six.b("\n")], [StrictLevel.MIN], [True]))
        + list(
            itertools.product(["", " ", "\n", MAXSIZE, inf, nan, None], [StrictLevel.MAX], [False])
        ),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = Binary(value, strict_level=strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.STRING
