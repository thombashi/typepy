pytypeutil
==========

.. image:: https://badge.fury.io/py/pytypeutil.svg
    :target: https://badge.fury.io/py/pytypeutil

.. image:: https://img.shields.io/pypi/pyversions/pytypeutil.svg
   :target: https://pypi.python.org/pypi/pytypeutil

.. image:: https://img.shields.io/travis/thombashi/pytypeutil/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/pytypeutil

.. image:: https://img.shields.io/appveyor/ci/thombashi/pytypeutil/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/pytypeutil

.. image:: https://coveralls.io/repos/github/thombashi/pytypeutil/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytypeutil?branch=master

.. image:: https://img.shields.io/github/stars/thombashi/pytypeutil.svg?style=social&label=Star
   :target: https://github.com/thombashi/pytypeutil

Summary
-------

A python library for variable type checker/validator/converter at run time.

Usage
=====

Type Check
----------------------

.. code:: pycon

    >>> from pytypeutil.type import Integer
    >>> Integer(1).is_type()
    True
    >>> Integer(1.1).is_type()
    False


Type Validation
----------------------

.. code:: pycon

    >>> from pytypeutil.type import Integer
    >>> Integer(1).validate()
    >>> try:
    ...     Integer(1.1).validate()
    ... except TypeError as e:
    ...     print(e)
    ...
    invalid value type: expected=INTEGER, actual=<type 'float'>


Type Conversion
----------------------

convert
~~~~~~~~~~~~~~
.. code:: pycon

    >>> from pytypeutil.type import Integer
    >>> from pytypeutil import TypeConversionError
    >>> Integer("1").convert()
    1
    >>> try:
    ...     Integer(1.1).convert()
    ... except TypeConversionError as e:
    ...     print(e)
    ...
    failed to convert from float to INTEGER

try_convert
~~~~~~~~~~~~~~
.. code:: pycon

    >>> from pytypeutil.type import Integer
    >>> Integer("1").try_convert()
    1
    >>> print(Integer(1.1).try_convert())
    None

force_convert
~~~~~~~~~~~~~~
.. code:: pycon

    >>> from pytypeutil.type import Integer
    >>> Integer("1").force_convert()
    1
    >>> Integer(1.1).force_convert()
    1


For more information
====================

More examples are available at 
http://pytypeutil.rtfd.io/en/latest/pages/reference/index.html

Features
========

Supported types are as follows:

- `bool <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#bool-type-class>`__
- `datetime <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#datetime-type-class>`__
- `dict <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#dictionary-type-class>`__
- `int <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#integer-type-class>`__
- float
    - `Real number <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#real-number-type-class>`__
    - `Infinite <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#infinity-type-class>`__
    - `Not a number <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#nan-type-class>`__
- `None <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#none-type-class>`__
- `str <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#string-type-class>`__
    - `Null string <http://pytypeutil.rtfd.io/en/latest/pages/reference/type.html#null-string-type-class>`__

Type check/validate/convert results will be decided according to ``strict_level``
which can be passed to constructors. API reference can be found in the
`document <http://pytypeutil.rtfd.io/>`__.

Installation
============

::

    pip install pytypeutil


Dependencies
============
Python 2.7+ or 3.3+

- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`__
- `pytz <https://pypi.python.org/pypi/pytz/>`__
- `six <https://pypi.python.org/pypi/six/>`__


Test dependencies
-----------------
- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__

Documentation
=============

http://pytypeutil.rtfd.io/

