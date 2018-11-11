#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import repeat, product
import os
import os.path
from os.path import isfile, join
import errno
import re
import warnings


_file_extensions = "", ".glsl", ".vert", ".tesc", ".tese", ".geom", ".frag", ".comp"

_profile_names = "core", "compatibility", "es"
_profile_name_default = "core"


class GLSLIncludeVersionDirectiveWarning(UserWarning):
	pass


def _remove_version_directives(string):
	return re.sub(r"^[ \t]*#[ \t]*version[ \t]+.*?$", "", string, flags=re.MULTILINE)


def iter_version_directives(string):
	for version, profile in re.findall(r"^[ \t]*#[ \t]*version[ \t]+(\d+)(?:[ \t]+(\w+))?", string, flags=re.MULTILINE):
		if not profile:
			profile = _profile_name_default
		yield version + " " + profile


def _process(string, search_path, filename=None):
	if filename is not None:
		search_path = [os.path.dirname(filename)] + search_path
	assert len(search_path) > 0

	def include(match):
		include_name = match.group(1)
		include_filename = next(filter(isfile, (filename + ext for ext, filename in product(_file_extensions, map(join, search_path, repeat(include_name))))), None)
		if include_filename is None:
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), include_name)
		with open(include_filename) as f:
			contents = f.read()
		return _process(contents, search_path, include_filename)

	return re.sub(r"^[ \t]*#[ \t]*include[ \t]+\"([^\"]*)\"", include, string, flags=re.MULTILINE)


def process(string, search_path=None, filename=None):
	if isinstance(search_path, str):
		search_path = list(filter(None, map(str.strip, search_path.split(";"))))
	elif search_path is None:
		search_path = []
	elif not isinstance(search_path, list):
		search_path = list(search_path)

	string = _process(string, search_path, filename)

	version_directives = sorted(set(iter_version_directives(string)), reverse=True)

	if len(version_directives) > 1:
		warnings.warn("Version directive mismatch %s" % " vs ".join(map(repr, version_directives)), GLSLIncludeVersionDirectiveWarning)
	elif len(version_directives) == 0:
		warnings.warn("Missing version directive", GLSLIncludeVersionDirectiveWarning)

	string = _remove_version_directives(string)
	string = string.lstrip()

	if version_directives:
		string = "#version %s\n\n%s" % (version_directives[0], string)

	return string


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

	if not args.output:
		warnings.simplefilter("ignore", category=GLSLIncludeVersionDirectiveWarning)

	glsl = process_file(args.input, search_path=args.search_path)

	if args.output:
		os.makedirs(os.path.dirname(args.output), exist_ok=True)
		with open(args.output, "w") as f:
			f.write(glsl)
	else:
		print(glsl)
