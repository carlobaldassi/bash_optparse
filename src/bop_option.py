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


# Option class for bash_optparse

import re

import bop_errors as err
import bop_checks as check
from bop_common import *

class BopOption(object):
	"""
	The option class.
	Initialization requires:
	  err.ParseCount cnt:		counter for parsing errors
	  BopSettings settings:		settings structure
	  STRING name:			name (alphanum,short)
	  STRING arg_type:		type (INT, FLOAT, STRING)
	  STRING arg_name:		arg name (for usage function)
	  STRING arg_range:		range
	  STRING default_val:		default argument
	  STRING desc:			description string for usage
	"""
	required_args = option_line_required_args
	def __init__(self, cnt, settings, name, arg_type, arg_name, arg_range, default_arg, desc):
		self.settings = settings
		self.name = name
		self.short = ""
		self.force_noshort = False
		self.short_only = False
		self.arg_type = str(arg_type)
		self.arg_name = str(arg_name)
		self.arg_range = str(arg_range)
		self.default_arg = str(default_arg)
		self.desc = str(desc)

		self.arg_range_compiled_regex = None
		self.open_boundary = [False, False]

		splitnamealt = str(name).split("|")
		test(len(splitnamealt) == 1 or len(splitnamealt) == 2, err.WrongSplitAltName, (cnt, name))

		self.name = splitnamealt[0]
		splitname = str(splitnamealt[0]).split(",")
		test(len(splitname) == 1 or len(splitname) == 2, err.WrongSplitName, (cnt, splitnamealt[0]))
		if len(splitname) > 1:
			self.name = splitname[0]
			self.short = splitname[1]
		elif len(self.name) == 1:
			self.short = self.name
			self.short_only = True

		test(check.var_name(self.name), err.InvalidName, (cnt, self.name))
		test(self.name != "help", err.ReservedOptName, (cnt, self.name))
		test(self.name != "version", err.ReservedOptName, (cnt, self.name))
		test(check.var_name_is_reserved(self.name), err.ReservedVarName, (cnt, self.name))

		test(check.optname_short(self.short) or check.directive_short(self.short), err.InvalidShortOpt, (cnt, self.short))
		self.short = check.is_empty_or_none(self.short)
		if self.short == "-":
			self.short = None
			self.force_noshort = True

		self.name_alt = None
		self.short_alt = ""
		self.force_noshort_alt = False
		self.short_only_alt = False
		if len(splitnamealt) == 2:
			self.name_alt = splitnamealt[1]
			splitname = str(splitnamealt[1]).split(",")
			test(len(splitname) == 1 or len(splitname) == 2, err.WrongSplitName, (cnt, splitnamealt[1]))
			if len(splitname) > 1:
				self.name_alt = splitname[0]
				self.short_alt = splitname[1]
			elif len(self.name_alt) == 1:
				self.short_alt = self.name_alt
				self.short_only_alt = True
			test(check.alt_opt_name(self.name_alt), err.InvalidName, (cnt, self.name_alt))
			test(self.name_alt != "help", err.ReservedOptName, (cnt, self.name_alt))
			test(self.name_alt != "version", err.ReservedOptName, (cnt, self.name_alt))
			#test(check.var_name_is_reserved(self.name_alt), err.ReservedVarName, (cnt, self.name_alt))

			test(check.optname_short(self.short_alt) or check.directive_short(self.short_alt), err.InvalidShortOpt, (cnt, self.short_alt))
			if self.short_alt == "-":
				self.short_alt = None
				self.force_noshort_alt = True

		self.short_alt = check.is_empty_or_none(self.short_alt)

		self.arg_type = self.arg_type.upper()

		if self.arg_type == "INT":
			self.parse_type_int(cnt)
		elif self.arg_type == "FLOAT":
			self.parse_type_float(cnt)
		elif self.arg_type == "STRING":
			self.parse_type_string(cnt)
		elif self.arg_type == "NONE" or self.arg_type == "":
			self.parse_type_flag(cnt)
		else:
			raise err.InvalidArgType(cnt, self.arg_type)

		self.opt_name = self.name.replace("_","-")
		self.opt_name_alt = None
		if self.name_alt != None:
			self.opt_name_alt = self.name_alt.replace("_","-")

	def abort_pre(self):
		if not self.settings.in_function:
			return ""
		else:
			return "( "

	def abort_post(self, code):
		if not self.settings.in_function:
			return ""
		else:
			return " ) || { BASH_OPTPARSE_EARLY_RETURN=true; return " + str(code) + "; }"

	def parse_with_arg_common(self, cnt):
		test(self.name_alt == None, err.InvalidDoubleName, (cnt, self.name_alt))

		self.has_arg = True
		test(check.optarg_name(self.arg_name), err.InvalidArgName, (cnt, self.arg_name))

		self.arg_range = check.is_empty_or_none(self.arg_range)

	def parse_numeric_range(self, cnt):
		if self.arg_type == "INT":
			range_error = err.InvalidIntRange
		elif self.arg_type == "FLOAT":
			range_error = err.InvalidFloatRange
		else:
			raise err.Bug(cnt, "")

		ar = self.arg_range.strip()
		if ar == "":
			ar = ":"
		if ar[0] in "](":
			self.open_boundary[0] = True
		if ar[-1] in "[)":
			self.open_boundary[1] = True
		if ar[0] in "[](" and ar[-1] in "[])":
			ar = ar[1:-1]
		ar = ar.split(':')
		for i in range(len(ar)):
			if len(ar[i].strip()) == 0:
				ar[i] = None
			elif (i == 0 and ar[i].strip().upper() == "-INF") or \
				(i == len(ar) - 1 and ar[i].strip().upper() == "INF"):
				ar[i] = None
			elif (ar[i].strip().upper() == "NONE"):
				ar[i] = None
			else:
				try:
					exec("ar[i] = " + ar[i])
				except (NameError, SyntaxError):
					raise range_error(cnt, self.arg_range)
		self.arg_range = ar

		#try:
			#exec "self.arg_range = " + self.arg_range
		#except (NameError, SyntaxError):
			#raise range_error(cnt, self.arg_range)

		test(isinstance(self.arg_range, list), range_error, (cnt, self.arg_range))
		test(len(self.arg_range) == 2 or len(self.arg_range) == 3, range_error, (cnt, self.arg_range))

		if self.arg_range[0] == None:
			self.open_boundary[0] = True
		if self.arg_range[-1] == None:
			self.open_boundary[1] = True

	def parse_string_range(self, cnt):
		range_error = err.InvalidStringRange
		try:
			exec("self.arg_range = " + self.arg_range)
		except (NameError, SyntaxError):
			try:
				self.arg_range = str(self.arg_range)
			except (NameError, SyntaxError):
				raise range_error(cnt, self.arg_range)

		#test(isinstance(self.arg_range, list) or isinstance(self.arg_range, str), range_error, (cnt, self.arg_range))
		test(isinstance(self.arg_range, str), range_error, (cnt, self.arg_range))
		test(len(self.arg_range) > 0, range_error, (cnt, self.arg_range))

		#if isinstance(self.arg_range, str):
		try:
			self.arg_range_compiled_regex = re.compile("^(" + self.arg_range + ")$")
		except:
			raise err.InvalidRegex(cnt, self.arg_range)
		#else:
			#for i, a in enumerate(self.arg_range):
				#test(isinstance(a, str) > 0, range_error, (cnt, self.arg_range))

	def set_numeric_default_val(self, cnt):
		if self.arg_type == "INT":
			invalid_error = err.InvalidIntDefaultVal
			out_of_range_error = err.OutOfRangeIntDefaultVal
		elif self.arg_type == "FLOAT":
			invalid_error = err.InvalidFloatDefaultVal
			out_of_range_error = err.OutOfRangeFloatDefaultVal
		else:
			raise err.Bug(cnt, "")

		self.default_arg = check.is_empty_or_none(self.default_arg)
		if self.default_arg != None:
			try:
				if self.arg_type == "INT":
					def_val = long(self.default_arg)
				elif self.arg_type == "FLOAT":
					def_val = float(self.default_arg)
			except ValueError:
				raise invalid_error(cnt, self.default_arg)

			test(check.is_in_range(def_val, self.arg_range, self.open_boundary), out_of_range_error, (cnt, def_val))

	def set_string_default_val(self, cnt):
		invalid_error = err.InvalidStringDefaultVal

		test(check.is_in_string_range(self.default_arg, self.arg_range_compiled_regex), invalid_error, (cnt, self.default_arg))

	def set_flag_default_val(self, cnt):
		invalid_error = err.InvalidFlagDefaultVal

		self.default_arg = check.is_empty_or_none(self.default_arg)
		if self.default_arg == None:
			self.default_arg = "false"

		test(check.is_bool_in_string(self.default_arg), invalid_error, (cnt, self.default_arg))

		self.default_arg = self.default_arg.lower()

	def parse_type_int(self, cnt):
		self.parse_with_arg_common(cnt)

		if self.arg_range != None:
			self.parse_numeric_range(cnt)

			for i in range(len(self.arg_range)):
				self.arg_range[i] == check.is_empty_or_none(self.arg_range[i])
				test(check.is_int_or_none(self.arg_range[i]), err.InvalidIntRange, (cnt, self.arg_range))

			test(check.range_boundaries_are_valid(self.arg_range, self.open_boundary), err.InvalidIntRange, (cnt, self.arg_range))

			if len(self.arg_range) == 3 and self.arg_range[1] == None:
				self.arg_range = [self.arg_range[0], self.arg_range[2]]

			test(check.range_step_is_valid(self.arg_range), err.InvalidIntRange, (cnt, self.arg_range))

		self.set_numeric_default_val(cnt)

	def parse_type_float(self, cnt):
		self.parse_with_arg_common(cnt)

		if self.arg_range != None:
			self.parse_numeric_range(cnt)

			for i in range(len(self.arg_range)):
				self.arg_range[i] == check.is_empty_or_none(self.arg_range[i])
				if isinstance(self.arg_range[i], int) or isinstance(self.arg_range[i], long):
					self.arg_range[i] = float(self.arg_range[i])
				test(check.is_float_or_none(self.arg_range[i]), err.InvalidFloatRange, (cnt, self.arg_range))

			test(check.range_boundaries_are_valid(self.arg_range, self.open_boundary), err.InvalidFloatRange, (cnt, self.arg_range))

			if len(self.arg_range) == 3 and self.arg_range[1] == None:
				self.arg_range = [self.arg_range[0], self.arg_range[2]]

			test(check.range_step_is_valid(self.arg_range), err.InvalidFloatRange, (cnt, self.arg_range))

		self.set_numeric_default_val(cnt)

	def parse_type_string(self, cnt):
		self.parse_with_arg_common(cnt)

		if self.arg_range != None:
			self.parse_string_range(cnt)

		self.set_string_default_val(cnt)

	def parse_type_flag(self, cnt):
		self.has_arg = False
		self.set_flag_default_val(cnt)

	def gen_usage_line(self):
		"""
		Returns a list containing two strings:
		an option token and a desctiption token
		"""
		opt_token = ""
		if self.short != None:
			opt_token += "-" + self.short
			if  not self.short_only:
				opt_token += ", "
		if not self.short_only:
			opt_token += "--" + self.opt_name
		if self.has_arg:
			opt_token += " <" + self.arg_name + ">"
		desc_token = self.desc
		if self.has_arg:
			desc_token += " (<" + self.arg_name + ">=" + self.arg_type.lower()
			if self.arg_type == "STRING" and self.arg_range != None:
				desc_token += " matching regex /" + self.arg_range + "/"
			elif (self.arg_type == "INT" or self.arg_type == "FLOAT") and self.arg_range != None and self.arg_range != [None, None]:
				if self.open_boundary[0] == False:
					b0 = "["
				else:
					b0 = "("
				if self.open_boundary[1] == False:
					b1 = "]"
				else:
					b1 = ")"
				if self.arg_range[0] == None:
					sr0 = "-INF"
				else:
					sr0 = str(self.arg_range[0])
				if self.arg_range[-1] == None:
					sr1 = "INF"
				else:
					sr1 = str(self.arg_range[-1])
				if len(self.arg_range) == 3:
					step_token = str(self.arg_range[1]) + ":"
				else:
					step_token = ""
				desc_token += " in " + b0 + sr0 + ":" + step_token + sr1 + b1
			if self.default_arg != None:
				#desc_token += " (default=${default_" + self.name + "})"
				desc_token += ", default=" + self.default_arg
			else:
				desc_token += ", no default value"
			desc_token += ")"
		return [opt_token, desc_token]

	def gen_usage_line_alt(self):
		"""
		Same as gen_usage_line, but for the alternate option
		(only allowed for flags)
		"""
		opt_token = ""
		if self.short_alt != None:
			opt_token += "-" + self.short_alt
			if  not self.short_only_alt:
				opt_token += ", "
		if not self.short_only_alt:
			opt_token += "--" + self.opt_name_alt
		desc_token = "Revert the effect of option "
		if not self.short_only:
			desc_token += "--" + self.opt_name
		else:
			desc_token += "-" + self.short
		return [opt_token, desc_token]

	def print_default_line(self, outfile):
		"""
		Prints the bash line which initialises the default values
		"""
		if self.default_arg != None:
			outfile.write("default_" + self.name + "=\"" + self.default_arg + "\"\n")
		else:
			outfile.write("default_" + self.name + "=\"\"\n")

	def print_getopt_block(self, outfile):
		"""
		Prints the bash getopt case block for the given option.
		"""
		outfile.write("\t\t")
		if self.short != None:
			outfile.write("-" + self.short)
			if not self.short_only:
				outfile.write("|")
		if not self.short_only:
			outfile.write("--" + self.opt_name)
		outfile.write(")\n")
		if self.has_arg:
			outfile.write("\t\t\t" + self.name + "=\"$2\"\n")
			outfile.write("\t\t\tshift 2\n")
		else:
			if self.default_arg == "true":
				outfile.write("\t\t\t" + self.name + "=\"false\"\n")
			else:
				outfile.write("\t\t\t" + self.name + "=\"true\"\n")
			outfile.write("\t\t\tshift 1\n")
		outfile.write("\t\t\t;;\n")

	def print_getopt_block_alt(self, outfile):
		"""
		Prints the bash getopt case block for the alternate form
		of the given option.
		"""
		outfile.write("\t\t")
		if self.short_alt != None:
			outfile.write("-" + self.short_alt)
			if not self.short_only_alt:
				outfile.write("|")
		if not self.short_only_alt:
			outfile.write("--" + self.opt_name_alt)
		outfile.write(")\n")
		if self.default_arg == "true":
			outfile.write("\t\t\t" + self.name + "=\"true\"\n")
		else:
			outfile.write("\t\t\t" + self.name + "=\"false\"\n")
		outfile.write("\t\t\tshift 1\n")
		outfile.write("\t\t\t;;\n")

	def print_check_optarg_type_block(self, outfile):
		"""
		Prints the bash check type line for the given option
		"""
		if self.has_arg:
			if self.default_arg == None:
				checknull_clause = "check_is_empty " + self.name + " || "
			else:
				checknull_clause = ""

			if self.arg_type == "INT":
				outfile.write(checknull_clause + "check_is_int " + self.name + " || " + \
					self.abort_pre() + "abort \"Invalid argument to option " + self.opt_name + \
					" (should be an INT): $" + self.name + "\" " + \
					str(self.settings.err_code_opt_type) + \
					self.abort_post(self.settings.err_code_opt_type) + "\n")
				outfile.write("\n")
			elif self.arg_type == "FLOAT":
				outfile.write(checknull_clause + "check_is_float " + self.name + " || " + \
					self.abort_pre() + "abort \"Invalid argument to option " + self.opt_name + \
					" (should be a FLOAT): $" + self.name + "\" " + \
					str(self.settings.err_code_opt_type) + \
					self.abort_post(self.settings.err_code_opt_type) + "\n")
				outfile.write("\n")

	def print_check_optarg_range_block(self, outfile):
		"""
		Prints the bash check range line for the given option
		"""
		if self.has_arg and self.arg_range != None and self.arg_range != [None, None]:
			if self.default_arg == None:
				checknull_clause = "check_is_empty " + self.name + " || "
			else:
				checknull_clause = ""

			if self.arg_type == "INT" or self.arg_type == "FLOAT":
				if self.open_boundary[0] == False:
					b0 = "["
				else:
					b0 = "("
				if self.open_boundary[1] == False:
					b1 = "]"
				else:
					b1 = ")"
				if self.arg_range[0] != None:
					sr0 = str(self.arg_range[0])
				else:
					sr0 = "-INF"
				if self.arg_range[-1] != None:
					sr1 = str(self.arg_range[-1])
				else:
					sr1 = "INF"
				if len(self.arg_range) == 3:
					srst = str(self.arg_range[1])
					srst_out = str(self.arg_range[1]) + ":"
				else:
					srst = "0"
					srst_out = ""
				outfile.write(checknull_clause + \
					"check_is_in_range " + self.name + " " + \
					"\"" + b0 + "\"" + " " + sr0 + " " + srst + " " + sr1 + " " + "\"" + b1 + "\"" + \
					" || " + self.abort_pre() + "abort \"out of range argument to option " + \
					self.opt_name + ": $" + self.name + \
					" (range is " + b0 + sr0 + ":" + srst_out + sr1 + b1 + \
					")\" " + str(self.settings.err_code_opt_range) + \
					self.abort_post(self.settings.err_code_opt_range) + "\n")
				outfile.write("\n")
			elif self.arg_type == "STRING":
				outfile.write("if ! bop_pygrep '^(" + self.arg_range + ")$' \"$" + self.name + "\"\n")
				outfile.write("then\n")
				outfile.write("\t" + self.abort_pre() + "abort \"Invalid argument to option " + self.opt_name + \
					": $" + self.name + " (must match regex: /" + self.arg_range + "/)\" " + \
					str(self.settings.err_code_opt_range) + \
					self.abort_post(self.settings.err_code_opt_range) + "\n")
				outfile.write("fi\n")
				outfile.write("\n")
			else:
				raise err.Bug(cnt, "")

