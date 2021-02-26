#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages


setup(
    name="lwtrng",
    description="Small Random Number Generator core",
    author="Kazumoto Kojima",
    author_email="kkojima@rr.iij4u.or.jp",
    test_suite="test",
    license="BSD",
    python_requires="~=3.6",
    packages=find_packages(exclude=("test*", "sim*", "doc*", "examples*")),
    package_data={
        'lwtrng': ['lwtrng/pp/verilog/**'],
    },
    include_package_data=True,
)
