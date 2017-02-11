# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

from pytypeutil import StrictLevel
from pytypeutil.type import Integer


class Test_DataPeroperty_repr:

    @pytest.mark.parametrize(["type_class", "value", "strict_level"], [
        [Integer, 0, StrictLevel.MIN],
        [Integer, 0, StrictLevel.MIN + 1],
        [Integer, 0, StrictLevel.MAX],
    ])
    def test_normal(self, type_class, value, strict_level):
        type_object = type_class(value, strict_level)

        assert str(type_object)
