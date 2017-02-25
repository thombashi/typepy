# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import datetime

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
