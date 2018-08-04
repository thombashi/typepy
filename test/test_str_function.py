# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools

import pytest
from typepy import is_not_null_string, is_null_string


nan = float("nan")
inf = float("inf")


class Test_is_not_null_string(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        list(itertools.product(["nan", "テスト"], [True]))
        + list(itertools.product([None, "", "  ", "\t", "\r\n", "\n", [], 1, True, nan], [False])),
    )
    def test_normal(self, value, expected):
        assert is_not_null_string(value) == expected


class Test_is_null_string(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        list(itertools.product([None, "", "  ", "\t", "\r\n", "\n"], [True]))
        + list(itertools.product(["nan", "テスト", [], 1, True, nan], [False])),
    )
    def test_normal(self, value, expected):
        assert is_null_string(value) == expected
