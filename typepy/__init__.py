# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

import typepy.type

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._const import StrictLevel
from ._function import (
    is_empty_sequence,
    is_empty_string,
    is_hex,
    is_not_empty_sequence,
    is_not_empty_string,
    is_not_null_string,
    is_null_string,
)
from ._typecode import Typecode
from .error import TypeConversionError
from .type import (
    Binary,
    Bool,
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
)
