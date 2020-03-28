Installation
============

Install from PyPI
------------------------------
::

    pip install typepy

Install additional dependency packages with the following command if using ``typepy.DateTime`` class

::

    pip install typepy[datetime]

Install from PPA (for Ubuntu)
------------------------------
::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install python3-typepy


Dependencies
============
Python 3.5+

- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__

Optioal dependencies
----------------------------------
These packages can be installed via ``pip install typepy[datetime]``:

- `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`__
- `pytz <https://pypi.org/project/pytz/>`__

Test dependencies
----------------------------------
- `pytest <https://docs.pytest.org/en/latest/>`__
- `tox <https://testrun.org/tox/latest/>`__
