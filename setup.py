# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import errno
import io
import os.path
import sys

import setuptools


MODULE_NAME = "typepy"
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info = {}


class ReleaseCommand(setuptools.Command):

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import re
        from pkg_resources import parse_version
        from pkg_resources.extern.packaging.version import Version, LegacyVersion

        pkg_version = pkg_info["__version__"]

        if not isinstance(parse_version(pkg_version), Version):
            sys.stderr.write("invalid version string: {}\n".format(pkg_version))
            sys.exit(errno.EINVAL)

        tag = "v{}".format(pkg_version)

        print("Pushing git tags: {}".format(tag))

        os.system("git tag {}".format(tag))
        os.system("git push --tags")
        os.system("twine upload dist/*")


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding=ENCODING) as f:
    long_description = f.read()

with io.open(
        os.path.join("docs", "pages", "introduction", "summary.txt"),
        encoding=ENCODING) as f:
    summary = f.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

setuptools_require = ["setuptools>=20.2.2"]
needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner_require = ["pytest-runner"] if needs_pytest else []

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url="https://github.com/thombashi/{:s}".format(MODULE_NAME),

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=[
        "library", "type-checking", "type-conversion", "validator",
    ],
    license=pkg_info["__license__"],
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["test*"]),

    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require + pytest_runner_require,
    tests_require=tests_requires,
    extras_require={
        "test": tests_requires,
        "docs": docs_requires,
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={
        "release": ReleaseCommand,
    })
