#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import repeat, product
import os
import os.path
from os.path import isfile, join
import errno
import re


_file_extensions = "", ".glsl", ".vert", ".tesc", ".tese", ".geom", ".frag", ".comp"


def _remove_version_directives(string):
	return re.sub(r"^[ \t]*#[ \t]*version[ \t]+.*?$", "", string, flags=re.MULTILINE)


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
		include_filename = next(filter(isfile, (filename + ext for ext, filename in product(_file_extensions, map(join, search_path, repeat(include_name))))), None)
		if include_filename is None:
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), include_name)
		return _remove_version_directives(process_file(include_filename, search_path=[os.path.dirname(include_filename)] + search_path))

	return re.sub(r"^[ \t]*#[ \t]*include[ \t]+\"([^\"]*)\"", include, string, flags=re.MULTILINE)


def process_file(file, search_path=None, filename=None):
	if isinstance(file, str):
		if filename is None:
			filename = file
		with open(file) as f:
			file = f.read()
	return process(file, search_path=search_path, filename=filename)


if __name__ == "__main__":
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument("input", help="Input GLSL file")
	parser.add_argument("--search-path", default=os.getcwd(), help="Paths used for searching for includes (default: current working directory)")
	parser.add_argument("--output", help="Output GLSL file")

	args = parser.parse_args()

	glsl = process_file(args.input, search_path=args.search_path)

	if args.output:
		with open(args.output, "w") as f:
			f.write(glsl)
	else:
		print(glsl)
