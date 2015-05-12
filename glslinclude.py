#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import repeat
import os.path
from os.path import isfile, join
import errno
import re


def process(string, search_path=None, filename=None):
	if isinstance(search_path, str):
		search_path = list(filter(None, map(str.strip, search_path.split(";"))))
	elif search_path is None:
		search_path = []

	if not isinstance(search_path, list):
		search_path = list(search_path)
	if filename is not None:
		search_path = [os.path.dirname(filename)] + search_path

	assert len(search_path) > 0

	def include(match):
		include_name = match.group(1)
		include_filename = next(filter(isfile, map(join, search_path, repeat(include_name))), None)
		if include_filename is None:
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), include_name)
		return process_file(include_filename, search_path=[os.path.dirname(include_filename)] + search_path)

	return re.sub(r"^[ \t]*#[ \t]*include[ \t]+\"([^\"]*)\"", include, string, flags=re.MULTILINE)


def process_file(file, search_path=None, filename=None):
	if isinstance(file, str):
		if filename is None:
			filename = file
		with open(file) as f:
			file = f.read()
	return process(file, search_path=search_path, filename=filename)
