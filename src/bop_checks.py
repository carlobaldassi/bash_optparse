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


# Check functions for bash_optparse

import re

def var_name(name):
	"""
	Check if a variable name is valid
	(must start with a letter, allowed characters are letters,
	digits and underscores)
	"""
	if re.match(r'^[A-Za-z][A-Za-z0-9_]*$', name) == None:
		return False
	elif re.match(r'^default_', name) != None:
		return False
	else:
		return True

def optname_short(short):
	"""
	Check if a short option is valid
	(must be empty or a single alphanumeric character)
	"""
	if re.match(r'^[A-Za-z0-9]?$', short) == None:
		return False
	else:
		return True

def optarg_name(name):
	"""
	Check if an optarg name is valid
	(must begin and end with non-whitespace)
	"""
	if re.match(r'^\S(.*\S)?$', name) == None:
		return False
	else:
		return True

def arg_type(arg_type):
	"""
	Check argument type (unused)
	"""
	if arg_type == "INT" or arg_type == "FLOAT" or arg_type == "STRING":
		return True
	else:
		return False

def range_boundaries_are_valid(r, ob):
	"""
	Check if the range boundaries are valid
	(used for INT and FLOAT values;
	assumes r is a list of 2 or 3 items,
	does not check type)
	"""
	if r[0] == None or r[-1] == None or r[0] < r[-1]:
		return True
	elif r[0] == r[-1] and ob[0] == False and ob[1] == False:
		return True
	else:
		return False

def range_step_is_valid(r):
	"""
	Check if the range step is valid
	(used for INT and FLOAT values;
	assumes r is a list of 2 or 3 items,
	does not check type)
	"""
	if len(r) == 2:
		return True
	elif r[1] > 0 and r[0] != None:
		return True
	elif r[1] < 0 and r[-1] != None:
		return True
	else:
		return False

def is_in_range(x, r, ob):
	"""
	Check if a value is within a given range
	(used for INT and FLOAT values; range format is checked elsewhere)
	"""
	if r == None:
		return True
	if r[0] != None and (x < r[0] or (x == r[0] and ob[0] == True)):
		return False
	if r[-1] != None and (x > r[-1] or (x == r[-1] and ob[1] == True)):
		return False
	if len(r) == 3:
		if r[1] > 0 and abs((x - r[0]) % (r[1] * (1 - 1e-15))) > (x - r[0]) * 5e-15:
			return False
		elif r[1] < 0 and abs((r[-1] - x) % ((-r[1]) * (1 - 1e-15))) > (r[-1] - x) * 5e-15:
			return False
		else:
			return True
	return True

def is_in_string_range(x, regex):
	"""
	Check if a value is valid according to a STING range,
	i.e. if it matches the range regex
	(used for STRING values range check; range format is checked elsewhere)
	"""
	if regex == None:
		return True
	else:
		if re.match(regex, x):
			return True
		else:
			return False

def is_int_or_none(r):
	"""
	Is the argument an int, or None?
	"""
	return r == None or isinstance(r, int) or isinstance(r, long)

def is_float_or_none(r):
	"""
	Is the argument a float, or None?
	"""
	return r == None or isinstance(r, float)

def is_empty_or_none(string_token):
	"""
	Is the argument an empty string, or None?
	"""
	if string_token == None or (isinstance(string_token, str) and (string_token == "" or string_token.upper() == "NONE")):
		return None
	else:
		return string_token
