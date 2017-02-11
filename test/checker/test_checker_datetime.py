# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
from datetime import datetime
import itertools

from dateutil.tz import tzoffset
import pytest
import six

from pytypeutil import (
    Typecode,
    StrictLevel,
)
from pytypeutil.type import DateTime


nan = float("nan")
inf = float("inf")


class Test_DateTime_is_type:

    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product(
            [datetime(2017, 3, 22, 10, 0, tzinfo=tzoffset(None, 32400))],
            [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
            [True]
        )) + list(itertools.product(
            [None, "invalid time string", six.MAXSIZE],
            [StrictLevel.MIN, StrictLevel.MIN + 1, StrictLevel.MAX],
            [False]
        )) + list(itertools.product(
            ["2017-03-22T10:00:00+0900",  "100-0004"],
            [StrictLevel.MIN],
            [True]
        )) + list(itertools.product(
            ["2017-03-22T10:00:00+0900",  "100-0004"],
            [StrictLevel.MAX],
            [False]
        ))
    )
    def test_normal(self, value, strict_level, expected):
        type_object = DateTime(value, strict_level)

        assert type_object.is_type() == expected
        assert type_object.typecode == Typecode.DATETIME
