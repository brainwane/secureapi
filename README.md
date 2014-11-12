A webapp and webservice to check users' source code for security vulnerabilities, using clang's static analyzer for C. By [Sumana Harihareswara](http://harihareswara.net/ces.shtml) & [Greg Hendershott](http://www.greghendershott.com/) while at [Hacker School](http://hackerschool.com).

Requires Python 2, Racket, bash, and a fairly flexible attitude to the importance of implementing GET. You can deploy it [using Docker](https://github.com/greghendershott/secureapi-docker).

Sample use
==========

1. Install clang and Racket on your OS using your preferred package manager.
1. Write some bad C code and name your file `badcode.c`.
1. In one terminal, run: `python hhserver.py`
1. In another terminal, run: `curl --data-binary @badcode.c -v http://localhost:8000`. You should see an HTTP response containing JSON -- an overall score and a list of errors.
