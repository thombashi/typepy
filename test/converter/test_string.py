# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import pytest
import pytypeutil

from ._common import (
    EXCEPTION_RESULT,
    convert_wrapper,
)


nan = float("nan")
inf = float("inf")


class Test_Integer(object):

    @pytest.mark.parametrize(
        ["method", "strict_level", "value", "expected"],
        [
            ["convert", 0, "abc", "abc"],
            ["convert", 0, "", ""],
            ["convert", 0, 1, "1"],
            ["convert", 0, "-1", "-1"],
            ["convert", 0, None, "None"],
            ["convert", 0, True, "True"],
            ["convert", 0, inf, "inf"],
            ["convert", 0, nan, "nan"],
            ["convert", 1, "abc", "abc"],
            ["convert", 1, "", EXCEPTION_RESULT],
            ["convert", 1, 1, EXCEPTION_RESULT],
            ["convert", 1, "-1", "-1"],
            ["convert", 1, None, EXCEPTION_RESULT],
            ["convert", 1, True, EXCEPTION_RESULT],
            ["convert", 1, inf, EXCEPTION_RESULT],
            ["convert", 1, nan, EXCEPTION_RESULT],
            ["try_convert", 0, "abc", "abc"],
            ["try_convert", 0, "", ""],
            ["try_convert", 0, 1, "1"],
            ["try_convert", 0, "-1", "-1"],
            ["try_convert", 0, None, "None"],
            ["try_convert", 0, True, "True"],
            ["try_convert", 0, inf, "inf"],
            ["try_convert", 0, nan, "nan"],
            ["try_convert", 1, "abc", "abc"],
            ["try_convert", 1, "", None],
            ["try_convert", 1, 1, None],
            ["try_convert", 1, "-1", "-1"],
            ["try_convert", 1, None, None],
            ["try_convert", 1, True, None],
            ["try_convert", 1, inf, None],
            ["try_convert", 1, nan, None],
            ["force_convert", 0, "abc", "abc"],
            ["force_convert", 0, "", ""],
            ["force_convert", 0, 1, "1"],
            ["force_convert", 0, "-1", "-1"],
            ["force_convert", 0, None, "None"],
            ["force_convert", 0, True, "True"],
            ["force_convert", 0, inf, "inf"],
            ["force_convert", 0, nan, "nan"],
            ["force_convert", 1, "abc", "abc"],
            ["force_convert", 1, "", ""],
            ["force_convert", 1, 1, "1"],
            ["force_convert", 1, "-1", "-1"],
            ["force_convert", 1, None, "None"],
            ["force_convert", 1, True, "True"],
            ["force_convert", 1, inf, "inf"],
            ["force_convert", 1, nan, "nan"],
        ]
    )
    def test_normal(self, method, strict_level, value, expected):
        assert convert_wrapper(
            pytypeutil.type.String(value, strict_level), method) == expected
