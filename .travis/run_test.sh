#!/bin/sh

pyver=$(python -c "from __future__ import print_function; import sys; print('{}{}'.format(*sys.version_info[0:2]))")
echo $pyver

tox

#if [ "$TRAVIS_OS_NAME" = "linux" ] && [ "$pyver" = "cov" ]; then
#    python setup.py test --addopts "-v --cov typepy --cov-report term-missing"
#fi
