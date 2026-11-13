#!/usr/bin/env python

import textwrap
import sys

def main():

	wmax = int(sys.argv[1])

	if (wmax >= 100):
		for i in range(1, wmax + 1):
			if i % 10 == 0 and i >= 100:
				sys.stdout.write(str(i / 100))
			else:
				sys.stdout.write(" ")
		sys.stdout.write("\n")

	for i in range(1, wmax + 1):
		if i % 10 == 0:
			sys.stdout.write(str(i % 100 / 10))
		else:
			sys.stdout.write(" ")
	sys.stdout.write("\n")

	for i in range(1, wmax + 1):
		sys.stdout.write(str(i % 10))
	sys.stdout.write("\n")
	sys.stdout.write("\n")

	usage_line = [
		['--gviz-overlap <type>', 'Graphviz overlap type (<type>=string in true/false, default=true)'],
		['--ooo <type>', 'ooo (<type>=string matching regex /low|high|sem|anim|semrand[A-J]/, default=low)']]

	max_opt_len = 0
	for l in usage_line:
		max_opt_len = max(max_opt_len, len(l[0]))

	opt_indent = "  "
	opt_min_sep = "  "

	opt_desc_wrap_width = wmax - max_opt_len - len(opt_indent) - len(opt_min_sep)

	sys.stdout.write("wrap=" + str(opt_desc_wrap_width) + "\n")

	if opt_desc_wrap_width < 10:
		wmax += (10 - opt_desc_wrap_width)

	sys.stdout.write("wmax=" + str(wmax) + "\n")

	twopt_desc = textwrap.TextWrapper(break_long_words=False, \
		break_on_hyphens=False, \
		subsequent_indent=(opt_indent + " " * max_opt_len + opt_min_sep), \
		width=wmax)


	outfile = sys.stdout

	for l in usage_line:
		opt_desc_unw = opt_indent + l[0] + opt_min_sep + " " * (max_opt_len - len(l[0])) + l[1]
		opt_desc = twopt_desc.fill(opt_desc_unw)
		#outfile.write(opt_indent + l[0] + opt_min_sep)
		#outfile.write(" " * (max_opt_len - len(l[0])))
		outfile.write(opt_desc + "\n")
	

	return 0

main()



