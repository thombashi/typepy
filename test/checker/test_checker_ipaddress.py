"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys
from ipaddress import ip_address

import pytest
from tcolorpy import tcolor

from typepy import IpAddress, StrictLevel, Typecode


class_under_test = IpAddress
nan = float("nan")
inf = float("inf")


class Test_IpAddress_is_type:
    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        [[tcolor("127.0.0.1", "red"), StrictLevel.MIN, True]]
        + list(
            itertools.product(
                ["", " ", sys.maxsize, str(sys.maxsize), inf, nan, None],
                [StrictLevel.MIN, StrictLevel.MAX],
                [False],
            )
        )
        + list(
            itertools.product(
                [ip_address("127.0.0.1"), ip_address("::1")],
                [StrictLevel.MIN, StrictLevel.MAX],
                [True],
            )
        )
        + list(itertools.product(["127.0.0.1", "::1", "800::800"], [StrictLevel.MIN], [True]))
        + list(itertools.product(["127.0.0.1", "::1", "800::800"], [StrictLevel.MAX], [False])),
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = IpAddress(value, strict_level=strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.IP_ADDRESS

    @pytest.mark.parametrize(
        ["value", "strip_ansi_escape", "expected"],
        [[tcolor("127.0.0.1", "red"), False, False], [tcolor("127.0.0.1", "red"), True, True]],
    )
    def test_normal_ansi(self, value, strip_ansi_escape, expected):
        type_checker = class_under_test(value, StrictLevel.MIN, strip_ansi_escape=strip_ansi_escape)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.IP_ADDRESS
