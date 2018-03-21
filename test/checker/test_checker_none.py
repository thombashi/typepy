# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools

import pytest
import six
from typepy import StrictLevel, Typecode
from typepy.type import NoneType


nan = float("nan")
inf = float("inf")


class Test_NoneTypeChecker_is_type(object):

    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product(
            [None],
            [StrictLevel.MIN, StrictLevel.MAX],
            [True]
        )) + list(itertools.product(
            [
                "None",
                True, False, 0, six.MAXSIZE, inf, nan,
            ],
            [StrictLevel.MIN, StrictLevel.MAX],
            [False]
        )))
    def test_normal(self, value, strict_level, expected):
        expected_typecode = Typecode.NONE

        typeobj = NoneType(value, strict_level)

        assert typeobj.is_type() == expected
        assert typeobj.typecode == expected_typecode
