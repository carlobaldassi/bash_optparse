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
		return mess(self.cnt, "this is a bug in bash_optparse!")

class QuotedNewline(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "escaped or quoted newline")

class WrongSplitAltName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "too many `|' in variable name: `" + self.value + "'")

class WrongSplitName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "too many `,' in variable name: `" + self.value + "'")

class InvalidName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid variable name: `" + self.value + "'")

class ReservedVarName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "variable name is reserved: `" + self.value + "'")

class ReservedOptName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "option name is reserved: `" + self.value + "'")

class InvalidShortOpt(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid short option: `" + self.value + "'")

class ReservedShortOpt(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "short option name is reserved: `" + self.value + "'")

class InvalidDoubleName(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "double variable names are only allowed in options without arguments: `" + self.value + "'")

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

class InvalidFlagDefaultVal(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid flag default argument: `" + self.value + "'")

class NotBoolean(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "not a boolean : `" + self.value + "'")

#class InvalidDescLine(Base):
	#def __init__(self, cnt, value):
		#Base.__init__(self, cnt)
		#self.value = value
	#def __str__(self):
		#return mess(self.cnt, "DESCRIPTION lines require 1 item, " + str(self.value) + " given (try using quotes)")

#class InvalidVersLine(Base):
	#def __init__(self, cnt, value):
		#Base.__init__(self, cnt)
		#self.value = value
	#def __str__(self):
		#return mess(self.cnt, "VERSION line requires 1 item, " + str(self.value) + " given (try using quotes)")

class InvalidOptLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "OPTION lines require " + str(option_line_required_args) + " items, " + str(self.value) + " given")

class DuplicateOpt(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate OPTION name: `" + self.value + "'")

class DuplicateShortOpt(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate short OPTION: `" + self.value + "'")

class ArgAfterVararg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "no ARGUMENT lines allowed after VARARG")

class InvalidArgLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "ARGUMENT lines require " + str(argument_line_required_args) + " items, " + str(self.value) + " given")

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

class InvalidBopMinVersLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "MIN_VERSION line requires 2 items, " + str(self.value) + " given")

class InvalidBopMinVers(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "invalid version in MIN_VERSION line: " + str(self.value))

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
		return mess(self.cnt, "WRAP_WIDTH line requires 2 items, " + str(self.value) + " given")

class InvalidBopWrapWidth(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "wrap witdh must be an integer >= 30, " + str(self.value) + " given")

class InvalidBopAutoShortOptsLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "AUTO_SHORT_OPTS line requires 2 items, " + str(self.value) + " given")

class InvalidBopAutoShortOpts(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "AUTO_SHORT_OPTS must be TRUE or FALSE, " + str(self.value) + " given")

class InvalidBopOneDashLongOptsLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "ONE_DASH_OPTS line requires 2 items, " + str(self.value) + " given")

class InvalidBopOneDashLongOpts(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "ONE_DASH_OPTS must be TRUE or FALSE, " + str(self.value) + " given")


class InvalidBopInFunctionLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "IN_FUNCTION line requires 2 items, " + str(self.value) + " given")

class InvalidBopInFunction(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "IN_FUNCTION must be TRUE or FALSE, " + str(self.value) + " given")

class InvalidBopErrCodeLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "ERR_CODE_* lines require 2 items, " + str(self.value) + " given")

class InvalidBopErrCode(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "error codes must be integers, " + str(self.value) + " given")

#class InvalidBopRegexDelimiterLine(Base):
	#def __init__(self, cnt, value):
		#Base.__init__(self, cnt)
		#self.value = value
	#def __str__(self):
		#return mess(self.cnt, "REGEX_DELIMITER line requires 2 items, " + str(self.value) + " given")

#class InvalidBopRegexDelimiter(Base):
	#def __init__(self, cnt, value):
		#Base.__init__(self, cnt)
		#self.value = value
	#def __str__(self):
		#return mess(self.cnt, "the regex delimiter must be a single character, \`" + str(self.value) + "\' given")

class InvalidBlockBeginLine(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "expected block-begin line, with a single token")

class DuplicateBlock(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate " + self.value + " block")

class BlockNotClosed(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "non closed block: " + self.value)

class UnknownDescriptor(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "unknown block descriptor: `" + self.value + "'")

class UnknownSetting(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "unknown setting descriptor: `" + self.value + "'")

class DuplicateOptArg(Base):
	def __init__(self, cnt, value):
		Base.__init__(self, cnt)
		self.value = value
	def __str__(self):
		return mess(self.cnt, "duplicate OPTION and ARGUMENT name: `" + self.value + "'")

