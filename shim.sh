# A shell script that simply runs its arguments and returns an exit
# code of 0.

scan-build clang -Weverything bar.c 2>&1 | racket parse.rkt
exit 0
