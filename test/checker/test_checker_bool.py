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
from pytypeutil.type import Bool


nan = float("nan")
inf = float("inf")


class Test_Bool_is_type:

    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"], [
        ] + list(itertools.product(
            [True, False],
            [StrictLevel.MIN, StrictLevel.MAX],
            [True],
        )) + list(itertools.product(
            [0, 1, "True", "False", "true", "false"],
            [StrictLevel.MIN],
            [True],
        )) + list(itertools.product(
            [0, 1, 0.1, "True", "False", "true", "false"],
            [StrictLevel.MAX],
            [False],
        ))
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = Bool(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.BOOL
