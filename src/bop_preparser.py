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
		self.sep_char = ','
		self.quote_char = '"'
		self.escape_char = '\\'
		pass
	def parse_line(self, cnt, line):
		ret = []
		curr_strl = []
		ind = 0
		in_quote = False
		in_escape = False
		quote_inds = []
		#sys.stderr.write("INPUT LINE: <" + repr(line) + ">\n")
		if line[-1:] != "\n":
			line = line + "\n"
		if len(line) == 1:
			return []
		for i, c in enumerate(line):
			#sys.stderr.write("i=" + str(i) + " c=<" + str(c) + ">\n")
			if (c == self.sep_char or c == "\n") and not in_quote and not in_escape:
				first_char = 0
				last_char = len(curr_strl) - 1
				first_quote_ind = None
				last_quote_ind = None
				for q in quote_inds:
					if q[0] != q[1]:
						if first_quote_ind == None:
							first_quote_ind = q[0]
						last_quote_ind = q[1]
				if first_quote_ind != None:
					while curr_strl[first_char].isspace() and first_char < first_quote_ind and first_char < last_char:
						first_char += 1
				else:
					while curr_strl[first_char].isspace() and first_char < last_char:
						first_char += 1
				if last_quote_ind != None:
					while curr_strl[last_char].isspace() and last_char >= last_quote_ind and last_char >= first_char:
						last_char -= 1
				else:
					while curr_strl[last_char].isspace() and last_char >= first_char:
						last_char -= 1

				#sys.stderr.write("fqi=" + str(first_quote_ind) + " lqi=" + str(last_quote_ind) + "\n")
				#sys.stderr.write("first=" + str(first_char) + " last=" + str(last_char) + "\n")
				#sys.stderr.write("TOKEN: <" + "".join(curr_strl[first_char:last_char + 1]) + ">\n")
				ret.append("".join(curr_strl[first_char:last_char + 1]))
				curr_strl = []
				ind = 0
				in_quote = False
				in_escape = False
				quote_inds = []
			elif c == "\n" and (in_quote or in_escape):
				raise err.QuotedNewline(cnt, "")
			elif c == self.quote_char and not in_quote and not in_escape:
				in_quote = True
				#if first_quote_ind == None:
					#first_quote_ind = ind
				quote_inds.append([ind, None])
			elif c == self.quote_char and in_quote and not in_escape:
				in_quote = False
				assert quote_inds[-1][1] == None, "WAT"
				quote_inds[-1][1] = ind
				#last_quote_ind = ind

			elif c == self.escape_char and not in_escape:
				in_escape = True
			else:
				#sys.stderr.write("  -> ind=" + str(ind) + " c=<" + str(c) + ">\n")
				curr_strl.append(c)
				in_escape = False
				ind += 1
		return ret

