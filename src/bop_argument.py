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


# Argument and vararg classes for bash_optparse

import bop_errors as err
import bop_checks as check
from bop_common import *

class BopArgument(object):
	"""
	The argument class.
	Initialization requires:
	  err.ParseCount cnt:		counter for parsing errors
	  BopSettings settings:		settings structure
	  STRING name:			name (alphanum)
	  BOOL   mandatory:		is mandatory? (True, False)
	  STRING arg_name:		arg name (for usage function)
	"""
	required_args = argument_line_required_args
	def __init__(self, cnt, settings, name, mandatory, arg_name):
		self.settings = settings
		self.name = str(name)
		mandatory = mandatory.capitalize()

		try:
			exec("self.mandatory = " + mandatory)
		except (NameError, SyntaxError):
			raise err.NotBoolean(cnt, mandatory)
		self.arg_name = str(arg_name)
		test(check.var_name(self.name), err.InvalidName, (cnt, self.name))
		test(not (self.name.startswith("BASH_OPTPARSE_") and self.name.isupper()), err.ReservedVarName, (cnt, self.name))
		test(isinstance(self.mandatory, bool), err.NotBoolean, (cnt, self.mandatory))
		test(check.optarg_name(self.arg_name), err.InvalidArgName, (cnt, self.arg_name))


class BopVararg(object):
	"""
	The vararg class.
	Initialization requires:
	  err.ParseCount cnt:		counter for parsing errors
	  BopSettings settings:		settings structure
	  STRING name:			name (VARARG od @, unused)
	  BOOL   mandatory:		is mandatory? (True, False)
	  STRING arg_name:		arg name (for usage function)
	"""
	required_args = vararg_line_required_args
	def __init__(self, cnt, settings, name, mandatory, arg_name):
		self.settings = settings
		test(str(name).upper() == "VARARGS" or name == "@", err.Bug, (cnt, ""))
		mandatory = mandatory.capitalize()
		try:
			exec("self.mandatory = " + mandatory)
		except (NameError, SyntaxError):
			raise err.NotBoolean(cnt, mandatory)
		self.arg_name = str(arg_name)

		test(isinstance(self.mandatory, bool), err.NotBoolean, (cnt, self.mandatory))
		test(check.optarg_name(self.arg_name), err.InvalidArgName, (cnt, self.arg_name))

