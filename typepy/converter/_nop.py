# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from ._interface import AbstractValueConverter


class NopConverter(AbstractValueConverter):

    def force_convert(self):
        return self._value
