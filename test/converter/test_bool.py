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


class Test_Integer(object):

    @pytest.mark.parametrize(
        ["method", "strict_level", "value", "expected"],
        [
            ["convert", 0, True, True],
            ["convert", 0, "true", True],
            ["convert", 0, 1, True],
            ["convert", 0, 1.1, "E"],
            ["convert", 0, None, "E"],
            ["convert", 1, True, True],
            ["convert", 1, "true", True],
            ["convert", 1, 1, "E"],
            ["convert", 1, 1.1, "E"],
            ["convert", 1, None, "E"],
            ["convert", 2, True, True],
            ["convert", 2, "true", "E"],
            ["convert", 2, 1, "E"],
            ["convert", 2, 1.1, "E"],
            ["convert", 2, None, "E"],
            ["try_convert", 0, True, True],
            ["try_convert", 0, "true", True],
            ["try_convert", 0, 1, True],
            ["try_convert", 0, 1.1, None],
            ["try_convert", 0, None, None],
            ["try_convert", 1, True, True],
            ["try_convert", 1, "true", True],
            ["try_convert", 1, 1, None],
            ["try_convert", 1, 1.1, None],
            ["try_convert", 1, None, None],
            ["try_convert", 2, True, True],
            ["try_convert", 2, "true", None],
            ["try_convert", 2, 1, None],
            ["try_convert", 2, 1.1, None],
            ["try_convert", 2, None, None],
            ["force_convert", 0, True, True],
            ["force_convert", 0, "true", True],
            ["force_convert", 0, 1, True],
            ["force_convert", 0, 1.1, "E"],
            ["force_convert", 0, None, "E"],
            ["force_convert", 1, True, True],
            ["force_convert", 1, "true", True],
            ["force_convert", 1, 1, True],
            ["force_convert", 1, 1.1, "E"],
            ["force_convert", 1, None, "E"],
            ["force_convert", 2, True, True],
            ["force_convert", 2, "true", True],
            ["force_convert", 2, 1, True],
            ["force_convert", 2, 1.1, "E"],
            ["force_convert", 2, None, "E"],
        ]
    )
    def test_normal(self, method, strict_level, value, expected):
        assert convert_wrapper(
            pytypeutil.type.Bool(value, strict_level), method) == expected
