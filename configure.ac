dnl Process this file with autoconf to produce a configure script.

AC_PREREQ(2.60)

dnl Name
m4_define([proj_name], [bash_optparse])

dnl These three define the version number
dnl the first two used for API
dnl the last one for bugfixes only
m4_define([proj_major_version], [2])
m4_define([proj_minor_version], [0])
m4_define([proj_micro_version], [0])

m4_define([proj_version], [proj_major_version.proj_minor_version.proj_micro_version])

AC_INIT([proj_name], [proj_version])

AC_SUBST(BOP_NAME, [proj_name])

AC_SUBST(BOP_MAJOR_VERSION, [proj_major_version])
AC_SUBST(BOP_MINOR_VERSION, [proj_minor_version])
AC_SUBST(BOP_MICRO_VERSION, [proj_micro_version])

dnl AC_DEFINE(PROJ_NAME, PACKAGE_NAME, [Project name])
dnl AC_DEFINE(PROJ_VERSION, PACKAGE_VERSION, [Project version])

dnl AC_DEFINE(API_VERSION, API_VERSION, [API version])

dnl AC_DEFINE(API_MAJOR_VERSION, api_major_version, [API major version])
dnl AC_DEFINE(API_MINOR_VERSION, api_minor_version, [API minor version])

AC_CONFIG_SRCDIR([src/bash_optparse.py])
dnl AM_CONFIG_HEADER(config.h)

AM_INIT_AUTOMAKE(no-define)

AM_PATH_PYTHON([2.6])

AM_MAINTAINER_MODE

AC_PROG_SED
AC_PROG_EGREP

AC_ARG_VAR(BASH_EXEC, [location of the bash executable])

AC_PATH_PROG(BASH_EXEC, bash, , )

if test "x$BASH_EXEC" == "x"
then
	AC_MSG_ERROR([cannot find bash. If it is installed, you may set the PATH or the BASH_EXEC variables to the install location.], 1)
fi

AC_MSG_CHECKING([bash version])
bash_version=`$BASH_EXEC --version | $EGREP 'GNU bash, version' | $SED -e 's,.*version\s\+\(\S*\).*,\1,'`
AC_MSG_RESULT($bash_version)

AS_VERSION_COMPARE($bash_version, 4.0.0,
	AC_MSG_ERROR([insufficient bash version $bash_version, at least 4.0.0 is required], 1),
	, ,)

AC_CONFIG_FILES([
Makefile
src/Makefile
doc/Makefile
utils/Makefile
completion/Makefile
])

AC_OUTPUT
