#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/1/14 10:33
# @Author: CHEN MIAOMIAO
from setuptools import find_packages, setup
setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
