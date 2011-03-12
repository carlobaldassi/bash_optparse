# Bash optparse
# Copyright (C) 2011 Carlo Baldassi (the "Author") <carlobaldassi@gmail.com>.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the Licence, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org.licences/>.


# Error definitions for bash_optparse

from bop_common import *
from bop_instantiated_values import *

class ParseCount(object):
	"""
	A small class which is used to keep track
	of the line number and content during parsing
	"""
	def __init__(self):
		self.lnum = 0
		self.line = ""
	def __str__(self):
		return str(self.lnum)
	def inc(self):
		self.lnum += 1

def mess(cnt, mess):
	"""
	Error message with line parsing information
	"""
	return "bash_optparse: parse error in line " + str(cnt.lnum) + ": " + mess + "\n" + \
	       "... parsed line: " + repr(cnt.line) + "\n"

def simple_mess(mess):
	"""
	Error message without line parsing information
	"""
	return "bash_optparse: error: " + mess + "\n"

class Base(Exception):
	"""
	Base exception class for the module.
	All parsing errors derive from this one.
	"""
	def __init__(self, cnt):
		self.cnt = cnt

class Bug(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "this is a bug!")

class QuotedNewline(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "escaped or quoted newline")

class InvalidName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid variable name: `" + self.value + "'")

class ReservedName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "option name is reserved: `" + self.value + "'")

class InvalidArgName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid argument name: `" + self.value + "'")

class InvalidArgType(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid argument type: `" + self.value + "'")

class InvalidIntRange(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid INT argument range: `" + repr(self.value) + "'")

class InvalidIntDefaultVal(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid default argument (not an int): `" + self.value + "'")

class OutOfRangeIntDefaultVal(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "default argument out of range: `" + str(self.value) + '"')

class InvalidFloatRange(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid FLOAT argument range: `" + repr(self.value) + "'")

class InvalidFloatDefaultVal(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid default argument (not a float): `" + self.value + "'")

class OutOfRangeFloatDefaultVal(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "default argument out of range: `" + str(self.value) + "'")

class InvalidStringRange(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid STRING argument range: `" + str(self.value) + "'")

class InvalidRegex(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid regex (failed to compile): `" + str(self.value) + "'")

class InvalidStringDefaultVal(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid STRING default argument: `" + self.value + "'")

class NotBoolean(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "not a boolean : `" + self.value + "'")

class InvalidDescLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "DESCRIPTION line requires 2 items, " + str(self.value) + " given")

class InvalidOptLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "OPTION line requires " + str(option_line_required_args) + " items, " + str(self.value) + " given")

class DuplicateOpt(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate OPTION name: `" + self.value + "'")

class ArgAfterVararg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "no ARGUMENT lines allowed afeter VARARG")

class InvalidArgLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "ARGUMENT line requires " + str(argument_line_required_args) + " items, " + str(self.value) + " given")

class MandArgAfterOptArg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "mandatory ARGUMENT after optional ARGUMENT")

class DuplicateArg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate ARGUMENT name: `" + self.value + "'")

class MultipleVararg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "only one VARARG line allowed")

class InvalidVarargLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "VARARG line requires " + str(vararg_line_required_args) + " items, " + str(self.value) + " given")

class MandVarargAfterOptArg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "mandatory VARARG after optional ARGUMENT")

class InvalidVersLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "VERSION line requires 2 items, " + str(self.value) + " given")

class InvalidBopMinVersLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "BOP_MIN_VERSION line requires 2 items, " + str(self.value) + " given")

class InvalidBopMinVers(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid version in BOP_MIN_VERSION line: " + str(self.value))

class InsufficientBopVersion(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return simple_mess("a more recent version of bash_optparse is required: " + str(self.value) + " (current is " + current_bop_version_major + "." + current_bop_version_minor + ")")

class InvalidBopWrapWidthLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "BOP_WRAP_WIDTH line requires 2 items, " + str(self.value) + " given")

class InvalidBopWrapWidth(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "wrap witdh must be an integer >= 30, " + str(self.value) + " given")

class InvalidBopRegexDelimiterLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "BOP_REGEX_DELIMITER line requires 2 items, " + str(self.value) + " given")

class InvalidBopRegexDelimiter(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "the regex delimiter must be a single character, \`" + str(self.value) + "\' given")

class UnknownDescriptor(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "unknown line descriptor: `" + self.value + "'")

class DuplicateOptArg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate OPTION and ARGUMENT name: `" + self.value + "'")
