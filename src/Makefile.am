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
bop_script_name = bash_optparse-$(BOP_API_VERSION)
bop_link_name = bash_optparse

scriptdir = $(bindir)

script_DATA = \
	$(bop_script_name)

## Following are makefile rules to
## generate bash_optparse-X

do_subst = $(SED) -e 's,[@]PYTHONDIR[@],$(pkgpythondir),g' \
	   -e 's,[@]PYTHON[@],$(PYTHON),g'

$(bop_script_name) : $(bop_script_in) $(top_builddir)/config.status
	$(do_subst) < "$(bop_script_in)" > "$(bop_script_name)"

## The install hook is used to
## create a link to the generated script,
## but without version number

destscriptdir = $(DESTDIR)$(scriptdir)

install-data-hook :
	cd $(destscriptdir) && \
	    rm -f $(bop_link_name) && \
	    $(LN_S) $(bop_script_name) $(bop_link_name)

## The uninstall hook tries to remove the
## link created by the install hook.
## It only removes the link if the version
## corresponds to the current one (the test
## is done by inspecting the link target, if
## possible, or by diff'ing with the script
## otherwise).
## If the link is removed, it checks for other
## versions of the script and relinks to the
## one with the highest version number.

uninstall-hook : $(bop_script_name)
	cd $(destscriptdir); \
	if test -L $(bop_link_name) && test "x$(HAS_READLINK)" = "xyes"; then \
	  test "`readlink $(bop_link_name)`" == $(bop_script_name) && \
	      rm -f $(bop_link_name) && \
	      rmvd="yes"; \
	else \
	  test -r $(bop_link_name) && \
	      diff $(bop_link_name) $(abs_builddir)/$(bop_script_name) > /dev/null && \
	      rm -f $(bop_link_name) && \
	      rmvd="yes"; \
	fi; \
	test "x$${rmvd}" = "xyes" && echo "Removed $(bop_link_name)"; \
	if test "x$${rmvd}" = "xyes" && \
	    newtgtn=`ls $(bop_link_name)-* 2> /dev/null | \
	        cut -d- -f2 | \
	        sort -n | \
	        $(EGREP) "^[0-9]+$$" | \
	        tail -n1` && \
	    test "x$${newtgtn}" != "x" && \
	    newtgt="$(bop_link_name)-$${newtgtn}"; then \
	  $(LN_S) "$${newtgt}" $(bop_link_name) && \
	      echo "Linked $(bop_link_name) to version $${newtgt}"; \
	fi;



EXTRA_DIST = $(bop_instant_in) $(bop_script_in)
CLEANFILES = $(bop_instant_py) $(script_DATA)

