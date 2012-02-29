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
import bop_checks as check
import bop_option as opt
import bop_argument as arg
import bop_settings as settings
from bop_common import *
from bop_instantiated_values import *

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

		current_block = None
		optional_arg_given = False

		settings_block_given = False
		description_block_given = False
		version_block_given = False
		options_block_given = False
		arguments_block_given = False

		insert_space_in_description = False
		insert_space_in_version = False

		opt_reader = preparser.LinePreParser()

		cnt = err.ParseCount()

		for l in infile.readlines():
			cnt.inc()
			cnt.line = l
			line = opt_reader.parse_line(cnt, l)
			cnt.line = line
			if len(line) == 0:
				continue;

			if current_block == None:
				if len(line) > 1:
					raise err.InvalidBlockBeginLine(cnt, line)
				line[0] = line[0].upper()
				if line[0] == "SETTINGS_BEGIN":
					test(not settings_block_given, err.DuplicateBlock, (cnt, "SETTINGS"))
					current_block = "SETTINGS_BLOCK"
					settings_block_given = True
				elif line[0] == "DESCRIPTION_BEGIN":
					test(not description_block_given, err.DuplicateBlock, (cnt, "DESCRIPTION"))
					current_block = "DESCRIPTION_BLOCK"
					description_block_given = True
				elif line[0] == "VERSION_BEGIN":
					test(not version_block_given, err.DuplicateBlock, (cnt, "VERSION"))
					current_block = "VERSION_BLOCK"
					version_block_given = True
				elif line[0] == "OPTIONS_BEGIN":
					test(not options_block_given, err.DuplicateBlock, (cnt, "OPTIONS"))
					current_block = "OPTIONS_BLOCK"
					options_block_given = True
				elif line[0] == "ARGUMENTS_BEGIN":
					test(not arguments_block_given, err.DuplicateBlock, (cnt, "ARGUMENTS"))
					current_block = "ARGUMENTS_BLOCK"
					arguments_block_given = True
				else:
					raise err.UnknownDescriptor(cnt, line[0])
			elif current_block == "SETTINGS_BLOCK":
				if line[0] == "SETTINGS_END":
					current_block = None
					continue
				if line[0] == "REQUIRED_VERSION":
					test(len(line) == 2, err.InvalidBopMinVersLine, (cnt, len(line)))
					settings.BopRequiredVersionChecker(cnt, *(line[1:]))
				elif line[0] == "WRAP_WIDTH":
					test(len(line) == 2, err.InvalidBopWrapWidthLine, (cnt, len(line)))
					try:
						self.settings.wrap_width = int(line[1])
					except:
						raise err.InvalidBopWrapWidth(cnt, line[1])
					test(self.settings.wrap_width >= 30, err.InvalidBopWrapWidth, (cnt, self.settings.wrap_width))
				elif line[0] == "AUTO_SHORT_OPTS":
					test(len(line) == 2, err.InvalidBopAutoShortOptsLine, (cnt, len(line)))
					try:
						exec("self.settings.auto_short_opts = " + line[1].capitalize())
					except (NameError, SyntaxError):
						raise err.InvalidBopAutoShortOpts(cnt, line[1])
					test(isinstance(self.settings.auto_short_opts, bool), err.InvalidBopAutoShortOpts, (cnt, line[1]))
				elif line[0] == "ONE_DASH_LONG_OPTS":
					test(len(line) == 2, err.InvalidBopOneDashLongOptsLine, (cnt, len(line)))
					try:
						exec("self.settings.one_dash_long_opts = " + line[1].capitalize())
					except (NameError, SyntaxError):
						raise err.InvalidBopOneDashLongOpts(cnt, line[1])
					test(isinstance(self.settings.one_dash_long_opts, bool), err.InvalidBopOneDashLongOpts, (cnt, line[1]))
				elif line[0] == "IN_FUNCTION":
					test(len(line) == 2, err.InvalidBopInFunctionLine, (cnt, len(line)))
					try:
						exec("self.settings.in_function = " + line[1].capitalize())
					except (NameError, SyntaxError):
						raise err.InvalidBopInFunction(cnt, line[1])
					test(isinstance(self.settings.in_function, bool), err.InvalidBopInFunction, (cnt, line[1]))
				elif line[0] == "ERR_CODE_OPT_INVALID":
					test(len(line) == 2, err.InvalidBopErrCodeLine, (cnt, len(line)))
					try:
						self.settings.err_code_opt_invalid = int(line[1])
					except:
						raise err.InvalidBopErrCode(cnt, line[1])
				elif line[0] == "ERR_CODE_OPT_TYPE":
					test(len(line) == 2, err.InvalidBopErrCodeLine, (cnt, len(line)))
					try:
						self.settings.err_code_opt_type = int(line[1])
					except:
						raise err.InvalidBopErrCode(cnt, line[1])
				elif line[0] == "ERR_CODE_OPT_RANGE":
					test(len(line) == 2, err.InvalidBopErrCodeLine, (cnt, len(line)))
					try:
						self.settings.err_code_opt_range = int(line[1])
					except:
						raise err.InvalidBopErrCode(cnt, line[1])
				elif line[0] == "ERR_CODE_ARG_NUM":
					test(len(line) == 2, err.InvalidBopErrCodeLine, (cnt, len(line)))
					try:
						self.settings.err_code_arg_num = int(line[1])
					except:
						raise err.InvalidBopErrCode(cnt, line[1])

				else:
					raise err.UnknownSetting(cnt, line[0])
			elif current_block == "DESCRIPTION_BLOCK":
				if line[0] == "DESCRIPTION_END":
					current_block = None
					continue
				for i in range(len(line)):
					if len(line[i]) == 0:
						continue
					if insert_space_in_description and not line[i][0].isspace():
						self.description += " "
					self.description += line[i]
					if line[i][-1].isspace():
						insert_space_in_description = False
					else:
						insert_space_in_description = True
			elif current_block == "VERSION_BLOCK":
				if line[0] == "VERSION_END":
					current_block = None
					continue
				#test(len(line) == 1, err.InvalidVersLine, (cnt, len(line)))
				insert_space_in_version = False
				vline = ""
				for i in range(len(line)):
					if len(line[i]) == 0:
						continue
					if insert_space_in_version and not line[i][0].isspace():
						vline += " "
					vline += line[i]
					if line[i][-1].isspace():
						insert_space_in_version = False
					else:
						insert_space_in_version = True
				self.version.append(vline)
			elif current_block == "OPTIONS_BLOCK":
				if line[0] == "OPTIONS_END":
					current_block = None
					continue
				test(len(line) == opt.BopOption.required_args, err.InvalidOptLine, (cnt, len(line)))
				myopt = opt.BopOption(cnt, self.settings, *line)

				test(myopt.opt_name_alt == None or myopt.opt_name != myopt.opt_name_alt, err.DuplicateOpt, (cnt, myopt.opt_name))
				test(myopt.short == None or myopt.short_alt == None or myopt.short != myopt.short_alt, err.DuplicateShortOpt, (cnt, myopt.short))

				for o in self.opt_list:
					test(myopt.name != o.name, err.DuplicateOpt, (cnt, myopt.name))
					test(myopt.short == None or myopt.short != o.short, err.DuplicateShortOpt, (cnt, myopt.short))

					test(myopt.opt_name_alt == None or myopt.opt_name_alt != o.opt_name, err.DuplicateOpt, (cnt, myopt.opt_name_alt))
					test(o.opt_name_alt == None or myopt.opt_name != o.opt_name_alt, err.DuplicateOpt, (cnt, myopt.opt_name))
					test(myopt.opt_name_alt == None or o.opt_name_alt == None or myopt.opt_name_alt != o.opt_name_alt, err.DuplicateOpt, (cnt, myopt.opt_name_alt))

					test(myopt.short_alt == None or o.short == None or myopt.short_alt != o.short, err.DuplicateShortOpt, (cnt, myopt.short_alt))
					test(myopt.short == None or o.short_alt == None or myopt.short != o.short_alt, err.DuplicateShortOpt, (cnt, myopt.short))
					test(myopt.short_alt == None or o.short_alt == None or myopt.short_alt != o.short_alt, err.DuplicateShortOpt, (cnt, myopt.short_alt))
				self.opt_list.append(myopt)
			elif current_block == "ARGUMENTS_BLOCK":
				if line[0] == "ARGUMENTS_END":
					current_block = None
					continue
				if line[0].upper() == "VARARGS" or line[0] == "@":
					test(self.vararg == None, err.MultipleVararg, (cnt, ""))
					test(len(line) == arg.BopVararg.required_args, err.InvalidVarargLine, (cnt, len(line)))
					myvarg = arg.BopVararg(cnt, self.settings, *line)
					if not myvarg.mandatory:
						optional_arg_given = True
					else:
						test(not optional_arg_given, err.MandVarargAfterOptArg, (cnt, ""))
					self.vararg = myvarg
				else:
					test(self.vararg == None, err.ArgAfterVararg, (cnt, ""))
					test(len(line) == arg.BopArgument.required_args, err.InvalidArgLine, (cnt, len(line)))
					myarg = arg.BopArgument(cnt, self.settings, *line)
					if not myarg.mandatory:
						optional_arg_given = True
					else:
						test(not optional_arg_given, err.MandArgAfterOptArg, (cnt, ""))
					for a in self.arg_list:
						test(myarg.name != a.name, err.DuplicateArg, (cnt, myarg.name))
					self.arg_list.append(myarg)
			else:
				raise err.Bug(cnt, "")

		test(current_block == None, err.BlockNotClosed, (cnt, current_block))

		for o in self.opt_list:
			for a in self.arg_list:
				test(o.name != a.name, err.DuplicateOptArg, (cnt, o.name))

		if self.settings.auto_short_opts:
			for o in self.opt_list:
				if (o.short != None or o.force_noshort) and \
					(o.name_alt == None or o.short_alt != None or o.force_noshort_alt):
					continue
				if not (o.short != None or o.force_noshort):
					for c in o.name:
						if not check.optname_short(c):
							continue
						found = False
						for o1 in self.opt_list:
							if c == o1.short or c == o1.short_alt:
								found = True
								break
						if not found:
							o.short = c
							break
				if not (o.name_alt == None or o.short_alt != None or o.force_noshort_alt):
					for c in o.name_alt:
						if not check.optname_short(c):
							continue
						found = False
						for o1 in self.opt_list:
							if c == o1.short or c == o1.short_alt:
								found = True
								break
						if not found:
							o.short_alt = c
							break

		for o in self.opt_list:
			self.usage_line.append(o.gen_usage_line())
			if o.name_alt != None:
				self.usage_line.append(o.gen_usage_line_alt())


		self.usage_line.append(["--version", "output version information and exit"])
		self.usage_line.append(["--help", "print this help and exit"])

		if len(self.version) == 0:
			self.version.append("Version information unspecified")

		if not self.settings.in_function:
			self.exit_command = "exit"
		else:
			self.exit_command = "BASH_OPTPARSE_EARLY_RETURN=true; return"

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
		if not self.settings.in_function:
			name_command = "$(basename $0)"
		else:
			name_command = "${FUNCNAME[3]}"

		usage_string = "Usage: " + name_command + " [options]"
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

		if not self.settings.in_function:
			name_command = "$(basename $0)"
		else:
			name_command = "${FUNCNAME[3]}"

		outfile.write("function usage_brief\n")
		outfile.write("{\n")
		outfile.write("\tcat << EOF\n")
		outfile.write(twusage.fill(usage_string) + "\n")
		outfile.write("(Use " + name_command + " --help for more information.)\n")
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
		if not self.settings.in_function:
			name_command = "$(basename $0)"
		else:
			name_command = "${FUNCNAME[3]}"
		outfile.write("function err_mess { echo \"" + name_command + ": error: $1\" >> /dev/stderr; }\n")
		outfile.write("function abort { local outval=\"$2\"; err_mess \"$1\"; [[ -n \"$outval\" ]] || outval=2; exit $outval; }\n")
		outfile.write("\n")

	def print_init_functions(self, outfile):
		"""
		Prints out the bash options initialisation functions.
		(These are required by print_init_line)
		"""
		outfile.write("function init_options { for opt in \"$@\"; do set_option_from_default \"$opt\"; done; }\n")
		outfile.write("function init_array_options { for opt in \"$@\"; do set_option_from_default_if_null \"$opt\"; done; }\n")
		outfile.write("function set_option_from_default { eval \"$1=\\\"\\$default_$1\\\"\"; }\n")
		outfile.write("function set_option_from_default_if_null { eval \"[[ \\${#$1[@]} -eq 0 ]] && $1=\\\"\\$default_$1\\\"\"; }\n")
		outfile.write("\n")

	def print_check_args_functions(self, outfile):
		"""
		Prints out the bash check functions.
		(These are required by print_check_optarg_block)
		"""
		outfile.write("function check_is_set { eval \"[[ \${#$1[@]} -gt 0 ]]\"; }\n")
		outfile.write("function check_is_int { [[ -n \"$1\" ]] && echo \"$1\" | egrep -q \"^[-+]?[[:digit:]]+$\"; }\n")
		outfile.write("function check_is_float { [[ -n \"$1\" ]] && echo \"$1\" | egrep -q \"^[-+]?([[:digit:]]+(\.[[:digit:]]*)?|\.[[:digit:]]+)([eE][-+]?[[:digit:]]+)?$\"; }\n")
		outfile.write("\n")
		outfile.write("function check_is_in_range\n")
		outfile.write("{\n")
		outfile.write("\tlocal x=\"$1\"\n")
		outfile.write("\tlocal openlow=\"$2\"\n")
		outfile.write("\tlocal lower=\"$3\"\n")
		outfile.write("\tlocal step=\"$4\"\n")
		outfile.write("\tlocal upper=\"$5\"\n")
		outfile.write("\tlocal openup=\"$6\"\n")
		outfile.write("\tlocal ol=0 ou=0\n")
		outfile.write("\t[[ \"$openlow\" == \"(\" ]] && ol=1\n")
		outfile.write("\t[[ \"$openup\" == \")\" ]] && ou=1\n")
		outfile.write("\t[[ \"$lower\" != \"-INF\" ]] && [[ \"$(echo \"$x\" | gawk -v l=$lower -v o=$ol '($1 < l || ($1 == l && o == 1)) {print 1}')\" == 1 ]] && return 1\n")
		outfile.write("\t[[ \"$upper\" != \"INF\" ]] && [[ \"$(echo \"$x\" | gawk -v u=$upper -v o=$ou '($1 > u || ($1 == u && o == 1)) {print 1}')\" == 1 ]] && return 1\n")
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
		outfile.write("\t" + python_binary + " -c \"\n")
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
		outfile.write("BASH_OPTPARSE_EARLY_RETURN=false\n\n")
		for o in self.opt_list:
			o.print_default_line(outfile)
		outfile.write("\n")

	def print_unset_args(self, outfile):
		"""
		Prints the bash lines which unset the arguments variables.
		"""
		for a in self.arg_list:
			a.print_unset_line(outfile)
		outfile.write("\n")

	def print_init_line(self, outfile):
		"""
		Prints the bash line which initialises the default values.
		(Requires the function init_options, which can be provided by print_init_functions.)
		(Call print_defaults before this function.)
		"""
		outfile.write("init_options \\\n")
		i = 0
		for o in self.opt_list:
			if (not o.is_array) and o.default_arg != None:
				if i > 0:
					outfile.write(" \\\n")
				outfile.write("\t" + o.name)
				i += 1
		outfile.write("\n\n")

	def print_init_arrays_line(self, outfile):
		"""
		Prints the bash line which initialises the default values for array-like variables.
		(Requires the function init_array_options, which can be provided by print_init_functions.)
		(Call print_defaults before this function.)
		"""
		outfile.write("init_array_options \\\n")
		i = 0
		for o in self.opt_list:
			if o.is_array and o.default_arg != None:
				if i > 0:
					outfile.write(" \\\n")
				outfile.write("\t" + o.name)
				i += 1
		outfile.write("\n\n")

	def print_getopt_block(self, outfile):
		"""
		Prints the getopt block which parses the command line
		(this parses both the options and the arguments.)

		Requires some functions to be defined in advance:
		1) usage (no arguments, provided by print_usage)
		2) err_mess (one message argument, provided by print_err_functions)
		"""
		short_opts_strl = [ ]
		long_opts_strl = [ "version", "help" ]
		for i, o in enumerate(self.opt_list):
			if o.short != None:
				if o.has_arg:
					short_opts_strl.append(o.short + ":")
				else:
					short_opts_strl.append(o.short)
			if o.has_arg:
				long_opts_strl.append(o.opt_name + ":")
			else:
				long_opts_strl.append(o.opt_name)
			if o.name_alt != None:
				if o.short_alt != None:
					short_opts_strl.append(o.short_alt)
				long_opts_strl.append(o.opt_name_alt)

		short_opts_str = "".join(short_opts_strl)
		long_opts_str = ", ".join(long_opts_strl)

		if (self.settings.one_dash_long_opts):
			one_dash_long_opts_str = "-a "
		else:
			one_dash_long_opts_str = ""
		if not self.settings.in_function:
			name_command = "$(basename $0)"
		else:
			name_command = "${FUNCNAME[3]}"

		outfile.write("PARAMETERS=$(getopt --name \"" + name_command + "\" " + one_dash_long_opts_str + "-o \"" + short_opts_str + "\" -l \"" + long_opts_str + "\" -- \"$@\")\n")
		outfile.write("\n")
		outfile.write("[ $? -ne 0 ] && { usage_brief; " + self.exit_command + " " + str(self.settings.err_code_opt_invalid) + "; }\n")
		outfile.write("\n")
		outfile.write("eval set -- \"$PARAMETERS\"\n")
		outfile.write("\n")
		outfile.write("while true\n")
		outfile.write("do\n")
		outfile.write("\tcase \"$1\" in\n")
		for o in self.opt_list:
			o.print_getopt_block(outfile)
			if o.name_alt != None:
				o.print_getopt_block_alt(outfile)
		outfile.write("\t\t--)\n")
		outfile.write("\t\t\tshift\n")
		outfile.write("\t\t\tbreak\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\t\t--help)\n")
		outfile.write("\t\t\tusage\n")
		outfile.write("\t\t\t" + self.exit_command + " 0\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\t\t--version)\n")
		outfile.write("\t\t\tprint_version\n")
		outfile.write("\t\t\t" + self.exit_command + " 0\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\t\t*)\n")
		outfile.write("\t\t\tusage_brief\n")
		outfile.write("\t\t\t" + self.exit_command + " " + str(self.settings.err_code_opt_invalid) + "\n")
		outfile.write("\t\t\t;;\n")
		outfile.write("\tesac\n")
		outfile.write("done\n")
		outfile.write("\n")
		for a in self.arg_list:
			if a.mandatory:
				outfile.write("[[ -n \"$1\" ]] || { err_mess \"argument missing: " + a.arg_name + \
					"\"; usage_brief; " + self.exit_command + " " + \
					str(self.settings.err_code_arg_num) + "; }\n")
				outfile.write(a.name + "=\"$1\"\n")
				outfile.write("shift\n")
			else:
				outfile.write("[[ -n \"$1\" ]] && { " + a.name + "=\"$1\"; shift; }\n") 
			outfile.write("\n")
		if self.vararg == None:
			outfile.write("[[ -n \"$1\" ]] && { err_mess \"extra arguments in the command line: $@\"; usage_brief; " + \
				self.exit_command + " " + str(self.settings.err_code_arg_num) + "; }\n")
			outfile.write("\n")
		elif self.vararg.mandatory:
			outfile.write("[[ -n \"$1\" ]] || { err_mess \"mandatory extra arguments required in the command line\"; usage_brief; " + \
				self.exit_command + " " + str(self.settings.err_code_arg_num) + "; }\n")
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

		self.print_unset_args(outfile)

		self.print_err_functions(outfile)

		self.print_init_functions(outfile)

		self.print_check_args_functions(outfile)

		self.print_pygrep_functions(outfile)

		self.print_init_line(outfile)

		self.print_getopt_block(outfile)

		self.print_init_arrays_line(outfile)

		self.print_check_optarg_block(outfile)

