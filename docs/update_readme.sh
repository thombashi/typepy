#!/bin/sh

set -eux

./make_result_matrix.py -o pages/reference/
./make_readme.py
