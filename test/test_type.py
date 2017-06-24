# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

import datetime
from decimal import Decimal

import ipaddress
import pytest
import pytz
import six
from typepy import StrictLevel
import typepy


class Test_TypeClass_repr(object):

    @pytest.mark.parametrize(["type_class", "value", "strict_level"], [
        [typepy.type.Integer, -six.MAXSIZE, StrictLevel.MIN],
        [typepy.type.Integer, six.MAXSIZE, StrictLevel.MAX],
        [typepy.type.RealNumber, -0.1, StrictLevel.MIN],
        [typepy.type.RealNumber, 0.1, StrictLevel.MAX],
        [typepy.type.DateTime, 1485685623, StrictLevel.MIN],
    ])
    def test_smoke(self, type_class, value, strict_level):
        type_object = type_class(value, strict_level)

        assert str(type_object)


class Test_type(object):

    @pytest.mark.parametrize(["type_class", "value", "expected"], [
        [
            typepy.type.IpAddress,
            "192.168.0.1",
            ipaddress.IPv4Address("192.168.0.1"),
        ],
        [
            typepy.type.IpAddress,
            "::1",
            ipaddress.IPv6Address("::1"),
        ],
    ])
    def test_normal(self, type_class, value, expected):
        assert type_class(value).convert() == expected


class Test_RealNumber(object):

    @pytest.mark.parametrize(["value", "float_type", "expected"], [
        [
            "0.1",
            float,
            0.1
        ],
        [
            "0.1",
            Decimal,
            Decimal("0.1")
        ],
    ])
    def test_normal_float_type(self, value, float_type, expected):
        result = typepy.type.RealNumber(
            value, strict_level=StrictLevel.MIN, float_type=float_type
        ).convert()

        assert result == expected


class Test_DateTime(object):

    @pytest.mark.parametrize(["value", "timezone", "expected"], [
        [
            datetime.datetime(2017, 1, 29, 10, 27, 3),
            pytz.utc,
            datetime.datetime(2017, 1, 29, 10, 27, 3)
        ],
        [
            datetime.datetime(2017, 1, 29, 10, 27, 3),
            pytz.timezone("Asia/Tokyo"),
            datetime.datetime(2017, 1, 29, 10, 27, 3)
        ],
        [
            "2017-01-29 19:27:03",
            pytz.utc,
            datetime.datetime(2017, 1, 29, 19, 27, 3)
        ],
        [
            "2017-01-29 19:27:03",
            pytz.timezone("Asia/Tokyo"),
            datetime.datetime(2017, 1, 29, 19, 27, 3)
        ],
        [
            1485685623,
            pytz.utc,
            datetime.datetime(2017, 1, 29, 10, 27, 3)
        ],
        [
            1485685623,
            pytz.timezone("Asia/Tokyo"),
            datetime.datetime(2017, 1, 29, 19, 27, 3),
        ],
    ])
    def test_normal_timezone(self, value, timezone, expected):
        result = typepy.type.DateTime(
            value, strict_level=StrictLevel.MIN, timezone=timezone).convert()

        assert result == timezone.localize(expected)
