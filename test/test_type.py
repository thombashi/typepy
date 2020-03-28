"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys
from datetime import date, datetime
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address

import pytest
from pytz import timezone, utc

import typepy
from typepy import StrictLevel


class Test_TypeClass_repr:
    @pytest.mark.parametrize(
        ["type_class", "value", "strict_level"],
        [
            [typepy.Integer, -sys.maxsize, StrictLevel.MIN],
            [typepy.Integer, sys.maxsize, StrictLevel.MAX],
            [typepy.RealNumber, -0.1, StrictLevel.MIN],
            [typepy.RealNumber, 0.1, StrictLevel.MAX],
            [typepy.DateTime, 1485685623, StrictLevel.MIN],
        ],
    )
    def test_smoke(self, type_class, value, strict_level):
        type_object = type_class(value, strict_level)

        assert str(type_object)


class Test_RealNumber:
    @pytest.mark.parametrize(
        ["value", "float_type", "expected"], [["0.1", float, 0.1], ["0.1", Decimal, Decimal("0.1")]]
    )
    def test_normal_float_type(self, value, float_type, expected):
        result = typepy.RealNumber(
            value, strict_level=StrictLevel.MIN, float_type=float_type
        ).convert()

        assert result == expected


class Test_DateTime:
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

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [date(2017, 1, 29), datetime(2017, 1, 29, 0, 0, 0)],
            ["2017-01-29", datetime(2017, 1, 29, 0, 0, 0)],
        ],
    )
    def test_normal_date(self, value, expected):
        result = typepy.DateTime(value, strict_level=StrictLevel.MIN).convert()

        assert result == expected


class Test_IpAddress:
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
