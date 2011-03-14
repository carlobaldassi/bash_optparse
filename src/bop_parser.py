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


# Parser classes for bash_optparse
# This is the core of the program

import textwrap

import bop_errors as err
import bop_preparser as preparser
import bop_option as opt
import bop_argument as arg
import bop_settings as settings
from bop_common import *

class Parser(object):
	"""
	The Option Parser class.
	Upon initialisation, it parses the options and arguments description from a
	custom-format text file.
	It can produce various blocks of bash commands useful for parsing the command line,
	auto-check the arguments, auto-generate the usage function etc., either individually
	or all at once.
	"""
	def __init__(self, infile):
		self.description = ""
		self.opt_list = []
		self.usage_line = []
		self.arg_list = []
		self.vararg = None
		self.version = []
		self.settings = settings.BopSettings()

		optional_arg_given = False

		opt_reader = preparser.LinePreParser()

		cnt = err.ParseCount()

		for l in infile.readlines():
			cnt.inc()
			cnt.line = l
			line = opt_reader.parse_line(cnt, l)
			cnt.line = line
			if len(line) == 0:
				continue;
			line[0] = line[0].upper()
			if line[0] == "COMMENT" or line[0] == "#":
				continue;
			if line[0] == "DESCRIPTION":
				test(len(line) == 2, err.InvalidDescLine, (cnt, len(line)))
				self.description += line[1]
			elif line[0] == "OPTION":
				test(len(line[1:]) == opt.BopOption.required_args, err.InvalidOptLine, (cnt, len(line[1:])))
				myopt = opt.BopOption(cnt, self.settings, *(line[1:]))
				for o in self.opt_list:
					test(myopt.name != o.name, err.DuplicateOpt, (cnt, myopt.name))
				self.opt_list.append(myopt)
				self.usage_line.append(myopt.gen_usage_line())
			elif line[0] == "ARGUMENT":
				test(self.vararg == None, err.ArgAfterVararg, (cnt, ""))
				test(len(line[1:]) == arg.BopArgument.required_args, err.InvalidArgLine, (cnt, len(line[1:])))
				myarg = arg.BopArgument(cnt, self.settings, *(line[1:]))
				if not myarg.mandatory:
					optional_arg_given = True
				else:
					test(not optional_arg_given, err.MandArgAfterOptArg, (cnt, ""))
				for a in self.arg_list:
					test(myarg.name != a.name, err.DuplicateArg, (cnt, myarg.name))
				self.arg_list.append(myarg)
			elif line[0] == "VARARG":
				test(self.vararg == None, err.MultipleVararg, (cnt, ""))
				test(len(line[1:]) == arg.BopVararg.required_args, err.InvalidVarargLine, (cnt, len(line[1:])))
				myvarg = arg.BopVararg(cnt, self.settings, *(line[1:]))
				if not myvarg.mandatory:
					optional_arg_given = True
				else:
					test(not optional_arg_given, err.MandVarargAfterOptArg, (cnt, ""))
				self.vararg = myvarg
			elif line[0] == "VERSION":
				test(len(line) == 2, err.InvalidVersLine, (cnt, len(line)))
				self.version.append(line[1])
			elif line[0] == "BOP_REQUIRED_VERSION":
				test(len(line) == 2, err.InvalidBopMinVersLine, (cnt, len(line)))
				settings.BopRequiredVersionChecker(cnt, *(line[1:]))
			elif line[0] == "BOP_WRAP_WIDTH":
				test(len(line) == 2, err.InvalidBopWrapWidthLine, (cnt, len(line)))
				try:
					self.settings.wrap_width = int(line[1])
				except:
					raise err.InvalidBopWrapWidth(cnt, line[1])
				test(self.settings.wrap_width >= 30, err.InvalidBopWrapWidth, (cnt, self.settings.wrap_width))
			elif line[0] == "BOP_REGEX_DELIMITER":
				test(len(line) == 2, err.InvalidBopRegexDelimiterLine, (cnt, len(line)))
				try:
					self.settings.regex_delimiter = str(line[1])
				except:
					raise err.InvalidBopRegexDelimiter(cnt, line[1])
				test(len(self.settings.regex_delimiter) == 1, err.InvalidBopRegexDelimiter, (cnt, self.settings.regex_delimiter))
			else:
				raise err.UnknownDescriptor(cnt, line[0])

		for o in self.opt_list:
			for a in self.arg_list:
				test(o.name != a.name, err.DuplicateOptArg, (cnt, o.name))

		if len(self.version) == 0:
			self.version.append("Version information unspecified")

	def print_usage(self, outfile):
		"""
		Auto-generate the "usage", "usage_brief" and "print_version" functions for bash.
		(The "usage" function is required by print_getopt_block)
		(It assumes that the default values are already initialized when called.)
		"""

		wrap_width = self.settings.wrap_width

		twusage = textwrap.TextWrapper(break_long_words=False, \
			break_on_hyphens=False, \
			subsequent_indent='  ...:    ', \
			width=wrap_width)

		twdesc = textwrap.TextWrapper(break_long_words=False, \
			break_on_hyphens=False, \
			subsequent_indent='', \
			width=wrap_width)

		outfile.write("function usage\n")
		outfile.write("{\n")
		outfile.write("\tcat << EOF\n")
		usage_string = "Usage: $(basename $0) [options]"
		for a in self.arg_list:
			usage_string += " "
			if not a.mandatory:
				usage_string += "["
			usage_string += "<" + a.arg_name + ">"
			if not a.mandatory:
				usage_string += "]"
		if self.vararg != None:
			usage_string += " "
			if not self.vararg.mandatory:
				usage_string += "["
			usage_string += "<" + self.vararg.arg_name + "...>"
			if not self.vararg.mandatory:
				usage_string += "]"
		usage_string += "\n"
		outfile.write(twusage.fill(usage_string) + "\n")
		outfile.write("\n")

		if len(self.description):
			outfile.write(twdesc.fill(self.description) + "\n")
			outfile.write("\n")

		outfile.write("Options:\n")

		self.usage_line.append(["--version", "output version number and exit"])
		self.usage_line.append(["-h, --help", "print this help and exit"])

		max_opt_len = 0
		for l in self.usage_line:
			max_opt_len = max(max_opt_len, len(l[0]))

		opt_indent = "  "
		opt_min_sep = "  "

		opt_desc_wrap_width = wrap_width - max_opt_len - len(opt_indent) - len(opt_min_sep)

		if opt_desc_wrap_width < 5:
			opt_desc_wrap_width = 5
			wrap_width += (5 - opt_desc_wrap_width)

		twopt_desc = textwrap.TextWrapper(break_long_words=False, \
			break_on_hyphens=False, \
			subsequent_indent=(opt_indent + " " * max_opt_len + opt_min_sep), \
			width=wrap_width)

		for l in self.usage_line:
			opt_desc_unw = opt_indent + l[0] + opt_min_sep + " " * (max_opt_len - len(l[0])) + l[1]
			opt_desc = twopt_desc.fill(opt_desc_unw)
			outfile.write(opt_desc + "\n")

		outfile.write("EOF\n")
		outfile.write("}\n")
		outfile.write("\n")

		outfile.write("function usage_brief\n")
		outfile.write("{\n")
		outfile.write("\tcat << EOF\n")
		outfile.write(twusage.fill(usage_string) + "\n")
		outfile.write("(Use $(basename $0) --help for more information.)\n")
		outfile.write("EOF\n")
		outfile.write("}\n")
		outfile.write("\n")

		outfile.write("function print_version\n")
		outfile.write("{\n")
		outfile.write("\tcat << EOF\n")
		for l in self.version:
			outfile.write(l + "\n")
		outfile.write("EOF\n")
		outfile.write("}\n")
		outfile.write("\n")

	def print_err_functions(self, outfile):
		"""
		Prints out the bash error functions.
		(These are required by print_getopt_block and print_check_optarg_block.)
		"""
		outfile.write("function err_mess { echo \"$(basename $0): error: $1\" >> /dev/stderr; }\n")
		outfile.write("function abort { local outval=\"$2\"; err_mess \"$1\"; [[ -n \"$outval\" ]] || outval=2; exit $outval; }\n")
		outfile.write("\n")

	def print_init_functions(self, outfile):
		"""
		Prints out the bash options initialisation functions.
		(These are required by print_init_line)
		"""
		outfile.write("function init_options { for opt in \"$@\"; do set_option_from_default \"$opt\"; done; }\n")
		outfile.write("function set_option_from_default { eval \"$1=\\\"\\$default_$1\\\"\"; }\n")
		outfile.write("\n")

	def print_check_args_functions(self, outfile):
		"""
		Prints out the bash check functions.
		(These are required by print_check_optarg_block)
		"""
		outfile.write("function check_is_empty { eval \"[[ -z \\\"\\$$1\\\" ]]\"; }\n")
		outfile.write("function check_is_int { eval \"[[ -n \\\"\\$$1\\\" ]] && echo \\\"\\$$1\\\" | egrep -q \\\"^[-+]?[[:digit:]]+\\$\\\"\"; }\n")
		outfile.write("function check_is_float { eval \"[[ -n \\\"\\$$1\\\" ]] && echo \\\"\\$$1\\\" | egrep -q \\\"^[-+]?([[:digit:]]+(\\.[[:digit:]]*)?|\\.[[:digit:]]+)([eE][-+]?[[:digit:]]+)?\\$\\\"\"; }\n")
		outfile.write("\n")
		outfile.write("function check_is_in_range\n")
		outfile.write("{\n")
		outfile.write("\teval \"local x=\\$$1\"\n")
		outfile.write("\tlocal openlow=\"$2\"\n")
		outfile.write("\tlocal lower=\"$3\"\n")
		outfile.write("\tlocal step=\"$4\"\n")
		outfile.write("\tlocal upper=\"$5\"\n")
		outfile.write("\tlocal openup=\"$6\"\n")
		outfile.write("\tlocal ol=0 ou=0\n")
		outfile.write("\t[[ \"$openlow\" == \"(\" ]] && ol=1\n")
		outfile.write("\t[[ \"$openup\" == \")\" ]] && ou=1\n")
		outfile.write("\t[[ \"$lower\" != \"-Inf\" ]] && [[ \"$(echo \"$x\" | gawk -v l=$lower -v o=$ol '($1 < l || ($1 == l && o == 1)) {print 1}')\" == 1 ]] && return 1\n")
		outfile.write("\t[[ \"$upper\" != \"Inf\" ]] && [[ \"$(echo \"$x\" | gawk -v u=$upper -v o=$ou '($1 > u || ($1 == u && o == 1)) {print 1}')\" == 1 ]] && return 1\n")
		outfile.write("\tif [[ \"$step\" != \"0\" ]]\n")
		outfile.write("\tthen\n")
		outfile.write("\t\tif echo \"$x\" | gawk -v l=$lower -v u=$upper -v s=$step \\\n")
		outfile.write("\t\t\t'{\n")
		outfile.write("\t\t\t\tif (s > 0) {\n")
		outfile.write("\t\t\t\t\td = ($1 - l)\n")
		outfile.write("\t\t\t\t} else {\n")
		outfile.write("\t\t\t\t\td = (u - $1);\n")
		outfile.write("\t\t\t\t\ts = -s\n")
		outfile.write("\t\t\t\t}\n")
		outfile.write("\t\t\t\tr = d % (s * (1 - 1e-15))\n")
		outfile.write("\t\t\t\tif (r < 0) { r = -r }\n")
		outfile.write("\t\t\t\tif (r > d * 5e-15) {\n")
		outfile.write("\t\t\t\t\texit 0\n")
		outfile.write("\t\t\t\t} else {\n")
		outfile.write("\t\t\t\t\texit 1\n")
		outfile.write("\t\t\t\t}\n")
		outfile.write("\t\t\t}'\n")
		outfile.write("\t\tthen\n")
		outfile.write("\t\t\treturn 1\n")
		outfile.write("\t\tfi\n")
		outfile.write("\tfi\n")
		outfile.write("\treturn 0\n")
		outfile.write("}\n")
		outfile.write("\n")

	def print_pygrep_functions(self, outfile):
		"""
		Prints out the bash bop_pygrep function.
		(This is required when checking for STRING regex options range)
		"""
		outfile.write("function bop_pygrep\n")
		outfile.write("{\n")
		outfile.write("\t/usr/bin/env python -c \"\n")
		outfile.write("import re\n")
		outfile.write("import sys\n")
		outfile.write("\n")
		outfile.write("regex = re.compile(sys.argv[1])\n")
		outfile.write("line = sys.argv[2]\n")
		outfile.write("\n")
		outfile.write("if re.search(regex, line) != None:\n")
		outfile.write("\tsys.exit(0)\n")
		outfile.write("else:\n")
		outfile.write("\tsys.exit(1)\n")
		outfile.write("\" \"$1\" \"$2\"\n")
		outfile.write("}\n")
		outfile.write("\n")

	def print_defaults(self, outfile):
		"""
		Prints the bash lines which define the default values.
		(Use before print_init_line.)
		"""
		for o in self.opt_list:
			o.print_default_line(outfile)

	def print_init_line(self, outfile):
		"""
		Prints the bash line which initialises the default values.
		(Requires the function init_options, which can be provided by print_init_functions.)
		(Call print_defaults before this function.)
		"""
		outfile.write("init_options \\\n")
		for i, o in enumerate(self.opt_list):
			outfile.write("\t" + o.name)
			if i != len(self.opt_list) - 1:
				outfile.write(" \\")
			outfile.write("\n")
		outfile.write("\n")

	def print_getopt_block(self, outfile):
		"""
		Prints the getopt block which parses the command line
		(this parses both the options and the arguments.)

		Requires some functions to be defined in advance:
		1) usage (no arguments, provided by print_usage)
		2) err_mess (one message argument, provided by print_err_functions)
		"""
		outfile.write("PARAMETERS=$(getopt -o \"h\" -l \"version, help,")
		for i, o in enumerate(self.opt_list):
			outfile.write(" " + o.opt_name)
			if o.has_arg:
				outfile.write(":")
			if i != len(self.opt_list) - 1:
				outfile.write(",")
		outfile.write("\" -- \"$@\")\n")
		outfile.write("\n")
		outfile.write("[ $? -ne 0 ] && { usage_brief; exit 1; }\n")
		outfile.write("\n")
		outfile.write("eval set -- \"$PARAMETERS\"\n")
		outfile.write("\n")
		outfile.write("while true\n")
		outfile.write("do\n")
		outfile.write("\tcase \"$1\" in\n")
		for o in self.opt_list:
			o.print_getopt_block(outfile)
		outfile.write("\t\t--)\n")
		outfile.write("\t\t\tshift\n")
		outfile.write("\t\t\tbreak\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\t\t-h|--help)\n")
		outfile.write("\t\t\tusage\n")
		outfile.write("\t\t\texit 0\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\t\t--version)\n")
		outfile.write("\t\t\tprint_version\n")
		outfile.write("\t\t\texit 0\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\t\t*)\n")
		outfile.write("\t\t\tusage_brief\n")
		outfile.write("\t\t\texit 1\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\tesac\n")
		outfile.write("done\n")
		outfile.write("\n")
		for a in self.arg_list:
			if a.mandatory:
				outfile.write("[[ -n \"$1\" ]] || { err_mess \"argument missing: " + a.arg_name + "\"; usage_brief; exit 1; }\n")
				outfile.write(a.name + "=\"$1\"\n")
				outfile.write("shift\n")
			else:
				outfile.write("[[ -n \"$1\" ]] && { " + a.name + "=\"$1\"; shift; }\n") 
			outfile.write("\n")
		if self.vararg == None:
			outfile.write("[[ -n \"$1\" ]] && { err_mess \"extra arguments in the command line: $@\"; usage_brief; exit 1; }\n")
			outfile.write("\n")
		elif self.vararg.mandatory:
			outfile.write("[[ -n \"$1\" ]] || { err_mess \"mandatory extra arguments required in the command line\"; usage_brief; exit 1; }\n")
			outfile.write("\n")

	def print_check_optarg_block(self, outfile):
		"""
		Prints the bash commands which check the type and range of
		each option.
		(Requires print_check_args_functions.)
		"""
		for o in self.opt_list:
			o.print_check_optarg_type_block(outfile)
			o.print_check_optarg_range_block(outfile)

	def print_script(self, outfile):
		"""
		Call all other print functions to
		produce the full script.
		"""
		self.print_usage(outfile)

		self.print_defaults(outfile)

		self.print_err_functions(outfile)

		self.print_init_functions(outfile)

		self.print_check_args_functions(outfile)

		self.print_pygrep_functions(outfile)

		self.print_init_line(outfile)

		self.print_getopt_block(outfile)

		self.print_check_optarg_block(outfile)

