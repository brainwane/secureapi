# A shell script that simply runs its arguments and returns an exit
# code of 0.

scan-build clang Weverything bar.c | parse.rkt
exit 0
