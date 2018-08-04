# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import pytest
import typepy

from ._common import convert_wrapper


nan = float("nan")
inf = float("inf")


class Test_String(object):
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
            ["convert", 1, "", ""],
            ["convert", 1, 1, "E"],
            ["convert", 1, "-1", "-1"],
            ["convert", 1, None, "E"],
            ["convert", 1, True, "E"],
            ["convert", 1, inf, "E"],
            ["convert", 1, nan, "E"],
            ["convert", 2, "abc", "abc"],
            ["convert", 2, "", "E"],
            ["convert", 2, 1, "E"],
            ["convert", 2, "-1", "-1"],
            ["convert", 2, None, "E"],
            ["convert", 2, True, "E"],
            ["convert", 2, inf, "E"],
            ["convert", 2, nan, "E"],
            ["try_convert", 0, "abc", "abc"],
            ["try_convert", 0, "", ""],
            ["try_convert", 0, 1, "1"],
            ["try_convert", 0, "-1", "-1"],
            ["try_convert", 0, None, "None"],
            ["try_convert", 0, True, "True"],
            ["try_convert", 0, inf, "inf"],
            ["try_convert", 0, nan, "nan"],
            ["try_convert", 1, "abc", "abc"],
            ["try_convert", 1, "", ""],
            ["try_convert", 1, 1, None],
            ["try_convert", 1, "-1", "-1"],
            ["try_convert", 1, None, None],
            ["try_convert", 1, True, None],
            ["try_convert", 1, inf, None],
            ["try_convert", 1, nan, None],
            ["try_convert", 2, "abc", "abc"],
            ["try_convert", 2, "", None],
            ["try_convert", 2, 1, None],
            ["try_convert", 2, "-1", "-1"],
            ["try_convert", 2, None, None],
            ["try_convert", 2, True, None],
            ["try_convert", 2, inf, None],
            ["try_convert", 2, nan, None],
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
            ["force_convert", 2, "abc", "abc"],
            ["force_convert", 2, "", ""],
            ["force_convert", 2, 1, "1"],
            ["force_convert", 2, "-1", "-1"],
            ["force_convert", 2, None, "None"],
            ["force_convert", 2, True, "True"],
            ["force_convert", 2, inf, "inf"],
            ["force_convert", 2, nan, "nan"],
        ],
    )
    def test_normal(self, method, strict_level, value, expected):
        assert convert_wrapper(typepy.String(value, strict_level), method) == expected
