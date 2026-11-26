"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address

import pytest
from zoneinfo import ZoneInfo

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
            [datetime(2017, 1, 29, 10, 27, 3), ZoneInfo("UTC"), datetime(2017, 1, 29, 10, 27, 3)],
            [
                datetime(2017, 1, 29, 10, 27, 3),
                ZoneInfo("Asia/Tokyo"),
                datetime(2017, 1, 29, 10, 27, 3),
            ],
            ["2017-01-29 19:27:03", ZoneInfo("UTC"), datetime(2017, 1, 29, 19, 27, 3)],
            ["2017-01-29 19:27:03", ZoneInfo("Asia/Tokyo"), datetime(2017, 1, 29, 19, 27, 3)],
            [1485685623, ZoneInfo("UTC"), datetime(2017, 1, 29, 10, 27, 3)],
            [1485685623, ZoneInfo("Asia/Tokyo"), datetime(2017, 1, 29, 19, 27, 3)],
        ],
    )
    def test_normal_datetime_timezone(self, value, timezone, expected):
        result = typepy.DateTime(value, strict_level=StrictLevel.MIN, timezone=timezone).convert()

        assert result == expected.replace(tzinfo=timezone)

    def test_normal_datetime_tz_aware(self):
        utc_dt = datetime(2017, 1, 29, 10, 27, 3, tzinfo=ZoneInfo("UTC"))
        got = typepy.DateTime(
            utc_dt, strict_level=StrictLevel.MIN, timezone=ZoneInfo("Asia/Tokyo")
        ).convert()
        assert got.tzinfo.tzname(got) == "JST"

        jst_dt = typepy.DateTime(
            "2017-01-29 19:27:03+0900",
            strict_level=StrictLevel.MIN,
        ).convert()
        assert jst_dt.tzinfo.utcoffset(jst_dt) == timedelta(seconds=32400)
        got = typepy.DateTime(
            jst_dt, strict_level=StrictLevel.MIN, timezone=ZoneInfo("UTC")
        ).convert()
        assert got.tzinfo.utcoffset(got) == timedelta(0)

    def test_normal_datetime_dst_ambiguous_default_fold(self):
        # 2024-11-03 01:30 in America/New_York is ambiguous (fall-back).
        # Per PEP 495, fold defaults to 0 — the earlier occurrence (EDT, UTC-4).
        ambiguous = datetime(2024, 11, 3, 1, 30)
        got = typepy.DateTime(
            ambiguous, strict_level=StrictLevel.MIN, timezone=ZoneInfo("America/New_York")
        ).convert()
        assert got.tzinfo.utcoffset(got) == timedelta(hours=-4)
        assert got.tzinfo.tzname(got) == "EDT"

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

    @pytest.mark.parametrize(
        ["value"],
        [
            [{"1"}],
            [{"1", "2"}],
            [["1"]],
            [["1", "2"]],
            [{"a": 1}],
            [(1, 2)],
            [None],
        ],
    )
    def test_abnormal_non_string(self, value):
        from typepy.error import TypeConversionError

        with pytest.raises(TypeConversionError):
            typepy.DateTime({"1"}, strict_level=StrictLevel.MIN).convert()

        assert typepy.DateTime(value, strict_level=StrictLevel.MIN).is_type() is False
        assert typepy.DateTime(value, strict_level=StrictLevel.MIN).try_convert() is None


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
