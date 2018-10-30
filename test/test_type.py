# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address

import pytest
import typepy
from pytz import timezone, utc
from six import MAXSIZE, text_type
from typepy import StrictLevel


class Test_TypeClass_repr(object):
    @pytest.mark.parametrize(
        ["type_class", "value", "strict_level"],
        [
            [typepy.Integer, -MAXSIZE, StrictLevel.MIN],
            [typepy.Integer, MAXSIZE, StrictLevel.MAX],
            [typepy.RealNumber, -0.1, StrictLevel.MIN],
            [typepy.RealNumber, 0.1, StrictLevel.MAX],
            [typepy.DateTime, 1485685623, StrictLevel.MIN],
        ],
    )
    def test_smoke(self, type_class, value, strict_level):
        type_object = type_class(value, strict_level)

        assert text_type(type_object)


class Test_RealNumber(object):
    @pytest.mark.parametrize(
        ["value", "float_type", "expected"], [["0.1", float, 0.1], ["0.1", Decimal, Decimal("0.1")]]
    )
    def test_normal_float_type(self, value, float_type, expected):
        result = typepy.RealNumber(
            value, strict_level=StrictLevel.MIN, float_type=float_type
        ).convert()

        assert result == expected


class Test_DateTime(object):
    @pytest.mark.parametrize(
        ["value", "timezone", "expected"],
        [
            [datetime(2017, 1, 29, 10, 27, 3), utc, datetime(2017, 1, 29, 10, 27, 3)],
            [
                datetime(2017, 1, 29, 10, 27, 3),
                timezone("Asia/Tokyo"),
                datetime(2017, 1, 29, 10, 27, 3),
            ],
            ["2017-01-29 19:27:03", utc, datetime(2017, 1, 29, 19, 27, 3)],
            ["2017-01-29 19:27:03", timezone("Asia/Tokyo"), datetime(2017, 1, 29, 19, 27, 3)],
            [1485685623, utc, datetime(2017, 1, 29, 10, 27, 3)],
            [1485685623, timezone("Asia/Tokyo"), datetime(2017, 1, 29, 19, 27, 3)],
        ],
    )
    def test_normal_datetime_timezone(self, value, timezone, expected):
        result = typepy.DateTime(value, strict_level=StrictLevel.MIN, timezone=timezone).convert()

        assert result == timezone.localize(expected)


class Test_IpAddress(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1")],
            ["127.0.0.1", IPv4Address("127.0.0.1")],
            ["::1", IPv6Address("::1")],
        ],
    )
    def test_normal(self, value, expected):
        result = typepy.IpAddress(value, strict_level=StrictLevel.MIN).convert()

        assert result == expected
