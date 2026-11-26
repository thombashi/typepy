"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from datetime import date, datetime

from .._common import strip_ansi_escape
from .._const import DefaultValue, ParamKey
from ..error import TypeConversionError
from ._interface import AbstractValueConverter


class DateTimeConverter(AbstractValueConverter):
    __COMMON_DST_TIMEZONE_TABLE = {
        -36000: "America/Adak",  # -1000
        -32400: "America/Anchorage",  # -0900
        -28800: "America/Los_Angeles",  # -0800
        -25200: "America/Denver",  # -0700
        -21600: "America/Chicago",  # -0600
        -18000: "America/New_York",  # -0500
        -14400: "America/Halifax",  # -0400
        -12600: "America/St_Johns",  # -0330
        -10800: "America/Miquelon",  # -0300
        7200: "Africa/Tripoli",  # 0200
    }

    def __init__(self, value, params):
        super().__init__(value, params)

        self.__datetime = None
        self.__timezone = self._params.get(ParamKey.TIMEZONE)

    def force_convert(self):
        self.__datetime = self.__from_datetime()
        if self.__datetime:
            return self.__datetime

        self.__datetime = self.__from_timestamp()
        if self.__datetime:
            return self.__datetime

        return self.__from_datetime_string()

    def __from_datetime(self):
        if not isinstance(self._value, (date, datetime)):
            return None

        if isinstance(self._value, datetime):
            self.__datetime = self._value
        elif isinstance(self._value, date):
            self.__datetime = datetime(
                year=self._value.year, month=self._value.month, day=self._value.day
            )

        if self.__timezone:
            if self.__datetime.tzinfo is None:
                self.__datetime = self.__datetime.replace(tzinfo=self.__timezone)
            else:
                self.__datetime = datetime.fromtimestamp(
                    self.__datetime.timestamp(), tz=self.__timezone
                )

        return self.__datetime

    def __from_timestamp(self):
        from ..type._integer import Integer
        from ..type._realnumber import RealNumber

        timestamp = Integer(self._value, strict_level=1).try_convert()
        if timestamp is None:
            timestamp = RealNumber(self._value, strict_level=1).try_convert()
        if timestamp is None:
            return None

        try:
            self.__datetime = datetime.fromtimestamp(float(timestamp), self.__timezone)
        except (ValueError, OSError, OverflowError):
            raise TypeConversionError(
                "timestamp is out of the range of values supported by the platform"
            )

        return self.__datetime

    def __from_datetime_string(self):
        import dateutil.parser
        from zoneinfo import ZoneInfo

        self.__validate_datetime_string()

        try:
            self.__datetime = dateutil.parser.parse(self._value)
        except (AttributeError, ValueError, OverflowError):
            if self._params.get(ParamKey.STRIP_ANSI_ESCAPE, DefaultValue.STRIP_ANSI_ESCAPE):
                try:
                    self.__datetime = dateutil.parser.parse(strip_ansi_escape(self._value))
                except (AttributeError, ValueError, OverflowError):
                    pass

        if self.__datetime is None:
            raise TypeConversionError(f"failed to parse as a datetime: type={type(self._value)}")

        if self.__timezone:
            tz = self.__timezone
        else:
            try:
                dst_timezone_name = self.__get_dst_timezone_name(self.__get_timedelta_sec())
            except (AttributeError, KeyError):
                return self.__datetime

            tz = ZoneInfo(dst_timezone_name)

        self.__datetime = self.__datetime.replace(tzinfo=tz)

        return self.__datetime

    def __get_timedelta_sec(self):
        return int(self.__datetime.utcoffset().total_seconds())

    def __get_dst_timezone_name(self, offset):
        return self.__COMMON_DST_TIMEZONE_TABLE[offset]

    def __validate_datetime_string(self):
        """
        This will require validating version string (such as "3.3.5").
        A version string could be converted to a datetime value if this
        validation is not executed.
        """

        from packaging.version import InvalidVersion, Version

        if not isinstance(self._value, str):
            raise TypeConversionError(f"invalid datetime string: type={type(self._value)}")

        try:
            Version(self._value)
        except InvalidVersion:
            return

        raise TypeConversionError(f"invalid datetime string: version string found {self._value}")
