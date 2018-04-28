# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import itertools
from ipaddress import ip_address

import pytest
import six
from typepy import IpAddress, StrictLevel, Typecode


nan = float("nan")
inf = float("inf")


class Test_IpAddress_is_type(object):

    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product(
            ["",  " ", six.MAXSIZE, str(six.MAXSIZE), inf, nan, None],
            [StrictLevel.MIN, StrictLevel.MAX],
            [False]
        )) + list(itertools.product(
            [ip_address("127.0.0.1"), ip_address("::1")],
            [StrictLevel.MIN, StrictLevel.MAX],
            [True],
        )) + list(itertools.product(
            ["127.0.0.1", "::1", "800::800"],
            [StrictLevel.MIN],
            [True],
        )) + list(itertools.product(
            ["127.0.0.1", "::1", "800::800"],
            [StrictLevel.MAX],
            [False],
        ))
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = IpAddress(value, strict_level=strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.IP_ADDRESS
