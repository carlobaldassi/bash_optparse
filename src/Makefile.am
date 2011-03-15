## Process this file with automake to produce Makefile.in

pkgpython_PYTHON = \
	bash_optparse.py \
	bop_common.py \
	bop_errors.py \
	bop_checks.py \
	bop_preparser.py \
	bop_parser.py \
	bop_option.py \
	bop_settings.py \
	bop_instantiated_values.py \
	bop_argument.py

## Following are makefile rules to
## generate bop_instantiated_values.py

bop_instant_in = $(srcdir)/bop_instantiated_values.py.in
bop_instant_py = bop_instantiated_values.py

do_subst_py = $(SED) \
	   -e 's,[@]CURRENT_BOP_VERSION_MAJOR[@],$(BOP_MAJOR_VERSION),g' \
	   -e 's,[@]CURRENT_BOP_VERSION_MINOR[@],$(BOP_MINOR_VERSION),g' \
	   -e 's,[@]CURRENT_BOP_VERSION_MICRO[@],$(BOP_MICRO_VERSION),g'

$(bop_instant_py) : $(bop_instant_in) $(top_builddir)/config.status
	$(do_subst_py) < "$(bop_instant_in)" > "$(bop_instant_py)"

## End of bop_instantiated_values.py rules


bop_script_in = $(srcdir)/bash_optparse.in
bop_script_name = bash_optparse

scriptdir = $(bindir)

script_DATA = \
	$(bop_script_name)

## Following are makefile rules to
## generate bash_optparse

do_subst = $(SED) -e 's,[@]PYTHONDIR[@],$(pkgpythondir),g' \
	   -e 's,[@]PYTHON[@],$(PYTHON),g'

$(bop_script_name) : $(bop_script_in) $(top_builddir)/config.status
	$(do_subst) < "$(bop_script_in)" > "$(bop_script_name)"

EXTRA_DIST = $(bop_instant_in) $(bop_script_in)
CLEANFILES = $(bop_instant_py) $(script_DATA)

