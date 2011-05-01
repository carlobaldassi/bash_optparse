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


# Enhanced option class for bash_optparse

import bop_errors as err
import bop_checks as check
from bop_common import *
from bop_instantiated_values import *

import sys
import os

class BopSettings(object):
	"""
	This has a role of a struct to hold all the
	adjustable values which can be set within
	the SETTINGS block
	"""
	def __init__(self):
		self.wrap_width = 80
		self.auto_short_opts = True
		self.in_function = False
		if os.environ['BASH_OPTPARSE_IS_IN_FUNC'] == "true":
			self.in_function = True
		self.err_code_opt_invalid = 2
		self.err_code_opt_type = 2
		self.err_code_opt_range = 2
		self.err_code_arg_num = 2

class BopRequiredVersionChecker(object):
	"""
	Check Enhanced Getopt current vs required version
	Initialization requires:
	  err.ParseCount cnt:	counter for parsing errors
	  STRING version:	required version, as major.minor
	"""
	def __init__(self, cnt, version):
		self.version = str(version)

		self.version = self.version.strip().split('.')

		test(len(self.version) == 2, err.InvalidBopMinVers, (cnt, version))

		try:
			for i, v in enumerate(self.version):
				self.version[i] = int(v)
		except:
			raise err.InvalidBopMinVers(cnt, version)

		try:
			v_maj = int(current_bop_version_major)
			v_min = int(current_bop_version_minor)
		except:
			raise err.Bug(cnt, None)

		if v_maj < self.version[0]:
			raise err.InsufficientBopVersion(cnt, version.strip())
		elif v_maj == self.version[0]:
			if v_min < self.version[1]:
				raise err.InsufficientBopVersion(cnt, version.strip())
		else:
			## TODO (?) should issue warning??
			pass
