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


# Line preparser for bash_optparse

#import sys
import bop_errors as err

class LinePreParser(object):
	"""
	Custom line parser class.
	Splits input in tokens and removes quoting and
	whitespace.
	"""
	def __init__(self):
		self.comment_char = '#'
		self.quote_char = '"'
		self.escape_char = '\\'
		pass
	def parse_line(self, cnt, line):
		ret = []
		curr_strl = []
		in_quote = False
		in_escape = False
		in_between = True

		has_quoting = False
		#sys.stderr.write("INPUT LINE: <" + repr(line) + ">\n")
		if line[-1:] != "\n":
			line = line + "\n"
		if len(line) == 1:
			return []

		i = 0;
		while i < len(line) and line[i].isspace():
			i += 1
		if i == len(line):
			return []
		line = line[i:]

		for c in line:
			#sys.stderr.write("i=" + str(i) + " c=<" + str(c) + ">\n")
			if c.isspace() and not in_quote and not in_escape and not in_between:
				outstr = "".join(curr_strl)
				if (not has_quoting) and outstr.upper() == "NONE":
					outstr = ""
				ret.append(outstr)
				curr_strl = []
				in_between = True
				has_quoting = False
			elif c.isspace() and not in_quote and not in_escape and in_between:
				pass
			elif c == self.comment_char and not in_quote and not in_escape:
				if len(curr_strl) > 0:
					outstr = "".join(curr_strl)
					if (not has_quoting) and outstr.upper() == "NONE":
						outstr = ""
					ret.append(outstr)
				curr_strl = []
				break
			elif c == "\n" and (in_quote or in_escape):
				raise err.QuotedNewline(cnt, "")
			elif c == self.quote_char and not in_quote and not in_escape:
				in_quote = True
				in_between = False
				has_quoting = True
			elif c == self.quote_char and in_quote and not in_escape:
				in_quote = False
				assert in_between == False, "WAT (bug)"
			elif c == self.escape_char and not in_escape:
				in_escape = True
				in_between = False
			else:
				#sys.stderr.write("  -> ind=" + str(ind) + " c=<" + str(c) + ">\n")
				curr_strl.append(c)
				in_escape = False
				in_between = False
		return ret

