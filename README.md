A web app and web service to check your source code for security
vulnerabilities, using clang's static analyzer for C family languages.

By [Sumana Harihareswara](http://harihareswara.net/ces.shtml) &
[Greg Hendershott](http://www.greghendershott.com/) while at
[Hacker School](http://hackerschool.com).

Requires Python 2.7, Racket 6.1, bash, and a fairly flexible attitude
to the importance of implementing GET. You can deploy it
[using Docker](https://github.com/greghendershott/secureapi-docker).

Sample use
==========

1. Install clang and Racket on your OS using your preferred package
   manager.

2. Write some bad C code and name your file `badcode.c`.

3. In one terminal, run: `python hhserver.py`

4. Use the server in two ways:

    - In another terminal, run:

      ```sh
      curl --data-binary @badcode.c -v http://localhost:8000/api/v1/analyze
      ```

      The HTTP response is a report in JSON format. The report
      contains an overall score from -∞ to 10, as well as a detailed
      list of issues.

    - In your browser, visit `http://localhost:8000/`. Supply code in
      the text box, or, upload a C file. Click submit to get the
      report as a web page.
