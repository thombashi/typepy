import pytest

from typepy._common import remove_thousand_sep


class Test_remove_thousand_sep:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["1,000,000,000,000", "1000000000000"],
            ["100,000,000,000", "100000000000"],
            ["10,000,000,000", "10000000000"],
            ["9,999,999,999", "9999999999"],
            ["123,456,789", "123456789"],
            ["2021-01-23", "2021-01-23"],
            ["1,000.1", "1000.1"],
        ],
    )
    def test_normal(self, value, expected):
        assert remove_thousand_sep(value) == expected
