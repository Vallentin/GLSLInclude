#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


def _read(filename):
	with open(os.path.join(os.path.dirname(__file__), filename)) as f:
		return f.read()


setup(
	name="GLSLInclude",
	version="1.0",
	long_description=_read("README.md"),
	license="zlib",
	author="Christian Vallentin",
	url="https://github.com/Vallentin/GLSLInclude",
	py_modules=["glslinclude"]
)
