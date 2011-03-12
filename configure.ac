dnl Process this file with autoconf to produce a configure script.

AC_PREREQ(2.54)

dnl Name
m4_define([proj_base_name], [bash_optparse])

dnl These three define the version number
dnl the first two used for API
dnl the last one for bugfixes only
m4_define([proj_major_version], [1])
m4_define([proj_minor_version], [0])
m4_define([proj_micro_version], [0])

m4_define([api_version], [proj_major_version])

m4_define([proj_version], [proj_minor_version.proj_micro_version])

m4_define([proj_name], [proj_base_name-api_version])

AC_INIT([proj_name], [proj_version])

#BASE_NAME=enhanced_getopt
AC_SUBST(BOP_BASE_NAME, [proj_base_name])
AC_SUBST(BOP_API_VERSION, [api_version])

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

AC_PROG_LN_S
AC_PROG_SED
AC_PROG_EGREP

AC_CHECK_PROG(HAS_READLINK, [readlink], [yes], [no])
AC_SUBST(HAS_READLINK)


AC_CONFIG_FILES([
Makefile
src/Makefile
])

AC_OUTPUT