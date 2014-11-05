#!/usr/bin/python

# Takes a list of errors and turns them into a red/yellow/green score
# assessing the general quality of the code base that has those
# errors in it.



# warning levels 
# if code does not compile, user gets an F :)

# list of warnings that we know are particularly bad
# null pointers, buffer overflow, etc. - security-related
# if code fails one of those: user gets an F/D


# bugginess: warnings per LoC :)
# booleans -- Yes/No to null pointer prob, buffer overflow vuln
#
