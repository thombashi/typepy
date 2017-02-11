# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import copy


class Typecode(object):
    NONE = 0
    INTEGER = 1 << 0
    FLOAT = 1 << 1
    STRING = 1 << 2
    NULL_STRING = 1 << 3
    DATETIME = 1 << 4
    INFINITY = 1 << 5
    NAN = 1 << 6
    BOOL = 1 << 7
    DICTIONARY = 1 << 8

    LIST = [
        NONE, INTEGER, FLOAT, NULL_STRING, STRING, DATETIME, INFINITY,
        NAN, BOOL, DICTIONARY,
    ]

    DEFAULT_TYPENAME_TABLE = {
        NONE: "NONE",
        INTEGER: "INTEGER",
        FLOAT: "FLOAT",
        STRING: "STRING",
        NULL_STRING: "STRING",
        DATETIME: "DATETIME",
        INFINITY: "INFINITY",
        NAN: "NAN",
        BOOL: "BOOL",
        DICTIONARY: "DICTIONARY",
    }

    TYPENAME_TABLE = copy.deepcopy(DEFAULT_TYPENAME_TABLE)

    @classmethod
    def get_typename(cls, typecode):
        type_name = cls.TYPENAME_TABLE.get(typecode)
        if type_name is None:
            raise ValueError("unknown typecode: {}".format(typecode))

        return type_name
