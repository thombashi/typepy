# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

import itertools

import pytest
from pytypeutil import (
    Typecode,
    StrictLevel,
)
from pytypeutil.type import NoneType
import six


nan = float("nan")
inf = float("inf")


class Test_NoneTypeChecker_is_type:

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
        ))
    )
    def test_normal(self, value, strict_level, expected):
        expected_typecode = Typecode.NONE

        typeobj = NoneType(value, strict_level)

        assert typeobj.is_type() == expected
        assert typeobj.typecode == expected_typecode
