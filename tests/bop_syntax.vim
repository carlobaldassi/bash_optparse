" Vim syntax file
" Language:	bash (extension for bash_optparse)
" Maintainer:	Carlo Baldassi <carlobaldassi@gmail.com>
" Last Change:	2011 May 20
" Note:         This goes on top of standard bash syntax
" Note:		This is best viewed with :foldmethod=marker

syntax case ignore
syntax match bopGlobalKeywords	contained "NONE"
syntax case match
syntax match   bopErr 		contained "\S.*"

syntax cluster bopMainCluster	contains=bopSetSection,bopDescSection,bopVerSection,bopOptSection,bopArgSection,bopErr,@bopCommentItems

syntax cluster bopSetItems	contains=@bopSetLines,bopGlobalKeywords,bopSetErrs,@bopCommentItems
syntax cluster bopDescItems	contains=@bopDescText,bopGlobalKeywords,bopDescErrs,@bopCommentItems
syntax cluster bopVerItems	contains=@bopVerText,bopGlobalKeywords,bopVerErrs,@bopCommentItems
syntax cluster bopOptItems	contains=bopOptL,bopOptErrs,bopGlobalKeywords,@bopCommentItems
syntax cluster bopArgItems	contains=bopArgL,bopArgErrs,bopGlobalKeywords,@bopCommentItems

syntax cluster bopCommentItems	contains=bopCommentL


syntax cluster bopSetLines	contains=bopSetReqVerL,bopSetWrapWL,bopSetAutoSOL,bopSetErrCL


syntax cluster bopCommentSpace	contains=bopTodo
syntax keyword bopTodo		contained TODO FIXME XXX

syntax region  bopMain		matchgroup=bopSectDelim fold start="^\s*\zsBASH_OPTPARSE_BEGIN\ze\s*\(#.*\)\?$" end="^\s*\zsBASH_OPTPARSE_END\ze\s*\(#.*\)\?$" transparent contains=@bopMainCluster

syntax match   bopSetErrs	contained "\S.*" contains=@bopCommentItems
syntax case ignore
syntax region  bopSetSection	contained matchgroup=bopSectDelim fold start="^\s*\zsSETTINGS_BEGIN\ze\s*\(#.*\)\?$" end="^\s*\zsSETTINGS_END\ze\s*\(#.*\)\?$" transparent contains=@bopSetItems
syntax region  bopDescSection	contained matchgroup=bopSectDelim fold start="^\s*\zsDESCRIPTION_BEGIN\ze\s*\(#.*\)\?$" end="^\s*\zsDESCRIPTION_END\ze\s*\(#.*\)\?$" transparent contains=@bopDescItems
syntax region  bopVerSection	contained matchgroup=bopSectDelim fold start="^\s*\zsVERSION_BEGIN\ze\s*\(#.*\)\?$" end="^\s*\zsVERSION_END\ze\s*\(#.*\)\?$" transparent contains=@bopVerItems
syntax region  bopOptSection	contained matchgroup=bopSectDelim fold start="^\s*\zsOPTIONS_BEGIN\ze\s*\(#.*\)\?$" end="^\s*\zsOPTIONS_END\ze\s*\(#.*\)\?$" transparent contains=@bopOptItems
syntax region  bopArgSection	contained matchgroup=bopSectDelim fold start="^\s*\zsARGUMENTS_BEGIN\ze\s*\(#.*\)\?$" end="^\s*\zsARGUMENTS_END\ze\s*\(#.*\)\?$" transparent contains=@bopArgItems
syntax case match

syntax region  bopSetReqVerL	contained matchgroup=bopSetLabel start="^\s*\zsREQUIRED_VERSION\ze\s\+" skip="\\$" end="$" keepend transparent contains=bopSetErrs,bopSetReqVer1A,@bopCommentItems

syntax match   bopSetReqVer1A	contained transparent "\S\+\ze\s*\($\|#\)"me=e-1 contains=@bopSetReqVerQNQ
syntax cluster bopSetReqVerQNQ	contains=bopSetReqVerQ,bopSetReqVerNQ,bopSetReqVerQErr
syntax region  bopSetReqVerQ	contained matchgroup=bopQuotes start=+"+ end=+"+ transparent contains=@bopSetReqVerCont
syntax match   bopSetReqVerNQ	contained +[^"]\++ transparent contains=@bopSetReqVerCont
syntax match   bopSetReqVerQErr	contained +"[^"]*\([^"]*"\)\@!+ transparent contains=bopSetErrs
syntax cluster bopSetReqVerCont	contains=bopSetErrs,bopSetReqVerArgs,@bopCommentItems
syntax match   bopSetReqVerArgs	contained "\s*\d\+\.\d\+\s*"

syntax region  bopSetWrapWL	contained matchgroup=bopSetLabel start="^\s*\zsWRAP_WIDTH\ze\s\+" skip="\\$" end="$" keepend transparent contains=bopSetErrs,bopSetWrapW1A,@bopCommentItems

syntax match   bopSetWrapW1A	contained transparent "\S\+\ze\s*\($\|#\)"me=e-1 contains=@bopSetWrapWQNQ
syntax cluster bopSetWrapWQNQ	contains=bopSetWrapWQ,bopSetWrapWNQ,bopSetWrapWQErr
syntax region  bopSetWrapWQ	contained matchgroup=bopQuotes start=+"+ end=+"+ transparent contains=@bopSetWrapWCont
syntax match   bopSetWrapWNQ	contained +[^"]\++ transparent contains=@bopSetWrapWCont
syntax match   bopSetWrapWQErr	contained +"[^"]*\([^"]*"\)\@!+ transparent contains=bopSetErrs
syntax cluster bopSetWrapWCont	contains=bopSetErrs,bopSetWrapWInv,bopSetWrapWArgs,@bopCommentItems
syntax match   bopSetWrapWInv	contained "\s*\([0-2]\?\d\)\s*"
syntax match   bopSetWrapWArgs	contained "\s*\(0*[1-9]\d\d\+\|0*[3-9]\d\)\s*"

syntax region  bopSetAutoSOL	contained matchgroup=bopSetLabel start="^\s*\zsAUTO_SHORT_OPTS\ze\s\+" skip="\\$" end="$" keepend transparent contains=bopSetErrs,bopSetAutoSO1A,@bopCommentItems

syntax match   bopSetAutoSO1A	contained transparent "\S\+\ze\s*\($\|#\)"me=e-1 contains=@bopSetAutoSOQNQ
syntax cluster bopSetAutoSOQNQ	contains=bopSetAutoSOQ,bopSetAutoSONQ,bopSetAutoSOQErr
syntax region  bopSetAutoSOQ	contained matchgroup=bopQuotes start=+"+ end=+"+ transparent contains=@bopSetAutoSOCont
syntax match   bopSetAutoSONQ	contained +[^"]\++ transparent contains=@bopSetAutoSOCont
syntax match   bopSetAutoSOQErr	contained +"[^"]*\([^"]*"\)\@!+ transparent contains=bopSetErrs
syntax cluster bopSetAutoSOCont	contains=bopSetErrs,bopSetAutoSOArgs,@bopCommentItems
syntax case ignore
syntax match   bopSetAutoSOArgs	contained "\(TRUE\|FALSE\)"
syntax case match

syntax region  bopSetErrCL	contained matchgroup=bopSetLabel start="^\s*\zsERR_CODE_\(OPT_\(INVALID\|TYPE\|RANGE\)\|ARG_NUM\)\ze\s\+" skip="\\$" end="$" keepend transparent contains=bopSetErrs,bopSetErrC1A,@bopCommentItems

syntax match   bopSetErrC1A	contained transparent "\S\+\ze\s*\($\|#\)"me=e-1 contains=@bopSetErrCQNQ
syntax cluster bopSetErrCQNQ	contains=bopSetErrCQ,bopSetErrCNQ,bopSetErrCQErr
syntax region  bopSetErrCQ	contained matchgroup=bopQuotes start=+"+ end=+"+ transparent contains=@bopSetErrCCont
syntax match   bopSetErrCNQ	contained +[^"]\++ transparent contains=@bopSetErrCCont
syntax match   bopSetErrCQErr	contained +"[^"]*\([^"]*"\)\@!+ transparent contains=bopSetErrs
syntax cluster bopSetErrCCont	contains=bopSetErrs,bopSetErrCArgs,@bopCommentItems
syntax case ignore
syntax match   bopSetErrCArgs	contained "-\?\d\+"
syntax case match

syntax cluster bopDescText	contains=bopDescTextQ,bopDescTextNQ
syntax match   bopDescTextNQ	contained "\S.*" contains=bopGlobalKeywords,bopDescTextQ,bopDescSpecial,bopDescSkipLB,@bopCommentItems
syntax region  bopDescTextQ	contained matchgroup=bopQuotes start=+"+ end=+"\|\n+ oneline contains=bopDescSpecial,bopDescSkipLB,bopDescErr
syntax match   bopDescErr	contained +\(\\.\|[^\\"]\)\+\n+
syntax match   bopDescSpecial	contained "\\."
syntax match   bopDescSkipLB	contained "\\\n"

syntax cluster bopVerText	contains=bopVerTextQ,bopVerTextNQ
syntax match   bopVerTextNQ	contained "\S.*" contains=bopGlobalKeywords,bopVerTextQ,bopVerSpecial,bopVerSkipLB,@bopCommentItems
syntax region  bopVerTextQ	contained matchgroup=bopQuotes start=+"+ end=+"\|\n+ oneline contains=bopVerSpecial,bopVerSkipLB,bopVerErr
syntax match   bopVerErr	contained +\(\\.\|[^\\"]\)\+\n+
syntax match   bopVerSpecial	contained "\\."
syntax match   bopVerSkipLB	contained "\\\n"

syntax region  bopOptErr	contained start=+\S.*+ skip="\\$" end="$" contains=bopOptSkipLB,@bopCommentItems
syntax region  bopOptL		contained start="^\s*\(OPTIONS_END\s*$\)\@!\S\+" skip="\\$" end="$" keepend contains=bopOptL1,bopOptL1Alt,bopOptErr,bopOptSpecial,bopOptSkipLB,@bopCommentItems,bopGlobalKeywords
syntax region  bopOptL1		contained matchgroup=bopOptName start=+^\s*\(help\>\|version\>\|default_\|BASH_OPTPARSE_\)\@!\a\(\a\|\d\|_\)*\(,\(-\|\a\)\)\?\ze\s\++ skip="\\$" end="$" contains=bopOptErr,bopOptL2S,bopOptL2F,bopOptL2I,bopOptL2N,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL1Alt	contained matchgroup=bopOptName start=+^\s*\(help\>\|version\>\|default_\|BASH_OPTPARSE_\)\@!\a\(\a\|\d\|_\)*\(,\(-\|\a\)\)\?|\(help\>\|version\>\)\@!\a\(\a\|\d\|[-_]\)*\(,\(-\|\a\)\)\?\ze\s\++ skip="\\$" end="$" contains=bopOptErr,bopOptL2N,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems

syntax case ignore
syntax region  bopOptL2S	contained matchgroup=bopOptType start=+\s*\("\s*"\)*\(STRING\|"STRING"\)\("\s*"\)*\s\++ skip="\\$" end="$" contains=bopOptL3S,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL2F	contained matchgroup=bopOptType start=+\s*\("\s*"\)*\(FLOAT\|"FLOAT"\)\("\s*"\)*\s\++ skip="\\$" end="$" contains=bopOptL3F,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL2I	contained matchgroup=bopOptType start=+\s*\("\s*"\)*\(INT\|"INT"\)\("\s*"\)*\s\++ skip="\\$" end="$" contains=bopOptL3I,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL2N	contained matchgroup=bopOptType start=+\s*\("\s*"\)*\(NONE\|""\|"NONE"\)\("\s*"\)*\s\++ skip="\\$" end="$" contains=bopOptL3N,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems

syntax region  bopOptL3S	contained matchgroup=bopOptAName start=+\s*\zs\("\s\)\@!\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL4S,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL3F	contained matchgroup=bopOptAName start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL4F0,bopOptL4F1,bopOptL4F2,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL3I	contained matchgroup=bopOptAName start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL4I0,bopOptL4I1,bopOptL4I2,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL3N	contained matchgroup=bopOptAName start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL4N,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems

syntax region  bopOptL4S	contained matchgroup=bopOptARange start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL5S,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4F0	contained matchgroup=bopOptARange start=+\s*\zs\("\s*"\)*\("\s*"\|NONE\|"\s*NONE\s*"\)\("\s*"\)*+ skip="\\$" end="$" contains=bopOptL5IF0,bopOptL5F,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4F1	contained matchgroup=bopOptARange start=+\s*\zs\%("\s*"\)*\("\?\)\s\{-}\%(\%([-+]\?\%(\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\|-INF\|NONE\)\?\s\{-}:\s\{-}\%(\%([-+]\?\%(0\+\s*:\)\@!\%(\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\|NONE\)\?\s\{-}:\s\{-}\)\?\%([-+]\?\%(\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\|INF\|NONE\)\?\)\s\{-}\1\%("\s*"\)*\ze\s\++ skip="\\$" end="$" contains=bopOptL5IF0,bopOptL5F,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4F2	contained matchgroup=bopOptARange start=+\s*\zs\%("\s*"\)*\("\?\)\s\{-}\%([]\[(]\s\{-}\%([-+]\?\%(\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\|-INF\|NONE\)\?\s\{-}:\s\{-}\%(\%([-+]\?\%(0\+\s*:\)\@!\%(\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\|NONE\)\?\s\{-}:\s\{-}\)\?\%([-+]\?\%(\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\|INF\|NONE\)\?\s\{-}[]\[)]\)\s\{-}\1\%("\s*"\)*\ze\s\++ skip="\\$" end="$" contains=bopOptL5IF0,bopOptL5F,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4I0	contained matchgroup=bopOptARange start=+\s*\zs\%("\s*"\)*\%("\s*"\|NONE\|"\s*NONE\s*"\)\%("\s*"\)*+ skip="\\$" end="$" contains=bopOptL5IF0,bopOptL5I,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4I1	contained matchgroup=bopOptARange start=+\s*\zs\%("\s*"\)*\("\?\)\s\{-}\%(\%([-+]\?\d\+\|-INF\|NONE\)\?\s\{-}:\s\{-}\%(\%([-+]\?\%(0\+\s*:\)\@!\d\+\|NONE\)\?\s\{-}:\s\{-}\)\?\%([-+]\?\d\+\|INF\|NONE\)\?\)\s\{-}\1\%("\s*"\)*\ze\s\++ skip="\\$" end="$" contains=bopOptL5IF0,bopOptL5I,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4I2	contained matchgroup=bopOptARange start=+\s*\zs\%("\s*"\)*\("\?\)\s\{-}\%([]\[(]\s\{-}\%([-+]\?\d\+\|-INF\|NONE\)\?\s\{-}:\s\{-}\%(\%([-+]\?\%(0\+\s*:\)\@!\d\+\|NONE\)\?\s\{-}:\s\{-}\)\?\%([-+]\?\d\+\|INF\|NONE\)\?\s\{-}[]\[)]\)\s\{-}\1\%("\s*"\)*\ze\s\++ skip="\\$" end="$" contains=bopOptL5IF0,bopOptL5I,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL4N	contained matchgroup=bopOptARange start=+\s*\zs\%("\%(\\.\|[^\\"]\)*"\|\%(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL5N,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems

syntax region  bopOptL5S	contained matchgroup=bopOptADef start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL6,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL5IF0	contained matchgroup=bopOptADef start=+\s*\zs\%("\(NONE\)\?"\|NONE\)\+\ze\s\++ skip="\\$" end="$" contains=bopOptL6,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL5F	contained matchgroup=bopOptADef start=+\s*\zs\%("\s*"\)*\("\?\)\s\{-}\%([-+]\?\d\+\%(\.\d*\)\?\|\.\d\+\)\%(e[-+]\d\+\)\?\s\{-}\1\%("\s*"\)*\ze\s\++ skip="\\$" end="$" contains=bopOptL6,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL5I	contained matchgroup=bopOptADef start=+\s*\zs\%("\s*"\)*\("\?\)\s\{-}[-+]\?\d\+\s\{-}\1\%("\s*"\)*\ze\s\++ skip="\\$" end="$" contains=bopOptL6,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax region  bopOptL5N	contained matchgroup=bopOptADef start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptL6,bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems

syntax region  bopOptL6		contained matchgroup=bopOptDesc start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopOptErr,bopOptSpecial,bopOptSkipLB,bopGlobalKeywords,@bopCommentItems
syntax case match

syntax match   bopOptSpecial	contained "\\."
syntax match   bopOptSkipLB	contained "\\\n"


syntax region  bopArgErr	contained start=+\S.*+ skip="\\$" end="$" contains=bopArgSkipLB,@bopCommentItems
syntax region  bopArgL		contained start="^\s*\(ARGUMENTS_END\s*$\)\@!\S\+" skip="\\$" end="$" keepend contains=bopArgL1,bopArgL1VA,bopArgErr,bopArgSpecial,bopArgSkipLB,@bopCommentItems,bopGlobalKeywords
syntax region  bopArgL1		contained matchgroup=bopArgName start=+^\s*\(default_\|BASH_OPTPARSE_\)\@!\a\(\a\|\d\|_\)*\(,\(-\|\a\)\)\?\ze\s\++ skip="\\$" end="$" contains=bopArgErr,bopArgL2,bopArgSpecial,bopArgSkipLB,bopGlobalKeywords,@bopCommentItems

syntax case ignore
syntax region  bopArgL1VA	contained matchgroup=bopArgName start=+^\s*\%(VARARGS\|@\)\ze\s\++ skip="\\$" end="$" contains=bopArgErr,bopArgL2,bopArgSpecial,bopArgSkipLB,bopGlobalKeywords,@bopCommentItems

syntax region  bopArgL2		contained matchgroup=bopArgMand start=+\s*\("\?\)\%(TRUE\|FALSE\)\1\ze\s\++ skip="\\$" end="$" contains=bopArgErr,bopArgL3,bopArgSpecial,bopArgSkipLB,bopGlobalKeywords,@bopCommentItems

syntax region  bopArgL3		contained matchgroup=bopArgDesc start=+\s*\zs\("\(\\.\|[^\\"]\)*"\|\(\\.\|[^\\"[:space:]]\)\+\)\++ skip="\\$" end="$" contains=bopArgErr,bopArgSpecial,bopArgSkipLB,bopGlobalKeywords,@bopCommentItems

syntax case match

syntax match   bopArgSpecial	contained "\\."
syntax match   bopArgSkipLB	contained "\\\n"


syntax region  bopCommentL	contained matchgroup=bopCommentDelim start="#" skip="\\$" end="$" keepend contains=@bopCommentSpace


hi def link bopErr		Error
hi def link bopSetErrs		bopErr
hi def link bopSetWrapWInv	bopErr
hi def link bopDescErr		bopErr
hi def link bopVerErr		bopErr
hi def link bopOptErr		bopErr
hi def link bopArgErr		bopErr

hi def link bopGlobalKeywords	Statement
hi def link bopSetLabel		Label
hi def link bopQuotes		Delimiter

hi def link bopSetReqVerArgs	Number
hi def link bopSetWrapWArgs	Number
hi def link bopSetAutoSOArgs	Number
hi def link bopSetErrCArgs	Number
hi def link bopTodo		Todo

hi def link bopDescTextNQ	Number
hi def link bopDescTextQ	String
hi def link bopDescSpecial	SpecialChar
hi def link bopDescSkipLB	SpecialChar

hi def link bopVerTextNQ	Number
hi def link bopVerTextQ		String
hi def link bopVerSpecial	SpecialChar
hi def link bopVerSkipLB	SpecialChar

hi def link bopOptL		Number
"hi def link bopOptL1		Error
"hi def link bopOptL1Alt		Error
hi def link bopOptName		String
hi def link bopOptType		Label
hi def link bopOptAName		PreProc
hi def link bopOptARange	StatusLine
hi def link bopOptADef		StatusLineNC
hi def link bopOptDesc		Todo
hi def link bopOptSpecial	SpecialChar
hi def link bopOptSkipLB	SpecialChar

hi def link bopArgL		Number
"hi def link bopArgL1		Error
hi def link bopArgName		String
hi def link bopArgMand		Label
hi def link bopArgDesc		Todo
hi def link bopArgSpecial	SpecialChar
hi def link bopArgSkipLB	SpecialChar

hi def link bopSectDelim	Delimiter
hi def link bopCommentL		Comment
hi def link bopCommentDelim	Comment
