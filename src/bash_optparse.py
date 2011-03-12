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


# This is the starting point for the program

import sys
#import optparse

import bop_errors as err
import bop_parser as parser

def main():
	fin = sys.stdin
	fout = sys.stdout

	try:
		mop = parser.Parser(fin)
		mop.print_script(fout)
	except err.Base as exc:
		sys.stderr.write(str(exc))
		return 1
	else:
		return 0

if __name__ == "__main__":
	sys.exit(main())
