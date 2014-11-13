#!/usr/bin/python

import BaseHTTPServer
import subprocess
import os
import string
import json
import random
from urlparse import parse_qs

PORT = 8000

class APIHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    rbufsize = 0

    def do_POST(self):
        # Get interesting things from the request
        self.content_length = int(self.headers.get("Content-Length","0"))
        self.content_type = self.headers.get("Content-Type","text/plain")
        self.request_body = self.rfile.read(self.content_length)
        # If a form submission we need to get the code from the `code`
        # field, URL decoding it. urlparse.parse_qs does both for us.
        if self.content_type == "application/x-www-form-urlencoded":
            d = parse_qs(self.request_body)
            self.code = d["code"][0]  # FIXME?
        # If a file upload, need to parse the multipart MIME format
        elif self.content_type.startswith("multipart/form-data;"):
            self.code = get_multipart_payload(self.request_body)
        # Otherwise the code is simply the entire request body. (This
        # is the case when the POST happens when using us as a web
        # service.)
        else:
            self.code = self.request_body
        # Determine our response body
        self.json = parse_request(self.code)
        if self.path == "/api/v1/analyze/":
            self.response_body = self.json
        else:
            self.response_body = make_htmlpage(self.json)
        # Send our response
        self.send_response(200)
        self.send_header("Content-Length", str(len(self.response_body)))
        if self.path == "/api/v1/analyze/":
            self.send_header("Content-Type", "application/json")
        else:
            self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.response_body)

    def do_GET(self):
        def respond_with_file(name, content_type):
            self.send_response(200)
            with open(name) as f:
                self.response_body = f.read()
                self.send_header("Content-Length", str(len(self.response_body)))
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(self.response_body)
        if self.path == '/':
            respond_with_file("index.html", "text/html")
        elif self.path == '/api/v1/analyze/':
            respond_with_file("index.json", "application/json")
        elif self.path == '/favicon.ico':
            respond_with_file("favicon.ico", "image/x-icon")
        else:
            self.send_response(404)
            self.end_headers()

def get_multipart_payload(s):
    """Assume that `s` is a multipart/form-data entity consisting of a
    boundary start, zero or more headers, a blank line, and then zero
    or more 'payload' lines until a matching closing boundary. Return
    the payload.

    """
    lines = s.splitlines()
    boundary = lines[0]
    result = ""
    ix = 0
    # Skip everything up to the first blank line, after the
    # boundary start and the headers.
    while ix < len(lines) and lines[ix] != "":
        ix = ix + 1
    # Skip the blank line itself.
    if ix < len(lines):
        ix = ix + 1
    # Use everything until a line that starts with boundary.
    while ix < len (lines) and not lines[ix].startswith(boundary):
        result = result + '\n' + lines[ix]
        ix = ix + 1
    return result

def name_file():
    """ Create a randomized filename so the user cannot count
    on us always using the same filename. A mild measure against
    some kinds of attacks.
    """
    basechars = string.letters + string.digits
    filename = ""
    for i in range(20):
        filename = filename + random.choice(basechars)
    filename = filename + ".c"
    return filename

def parse_request(request_body):
    """ take a request from the client, run the C code through
    the clang static analyzer via the shim shell script,
    return the string to be used in the response body
    """
    filename = name_file()
    with open(filename, "w") as f:
        f.write(request_body)
    try:
        clang_result = subprocess.check_output(["bash", "shim.sh", filename], stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        clang_result = "shim failed!"
    os.remove(filename)
    return clang_result

def make_htmlpage(strinput):
    results = json.loads(strinput)
    score = str(results["score"])
    errorlist = "<ul>"
    def collinecompare(a,b):
        # compare line number
        # if line number is the same, compare col number
        aline, bline, acol, bcol = int(a["line"]), int(b["line"]), int(a["col"]), int(b["col"])
        if aline < bline:
            return -1
        elif aline > bline:
            return 1
        else:
            if acol < bcol:
                return -1
            elif acol > bcol:
                return 1
            else:
                return 0
    resultlist = sorted(results["items"], cmp=collinecompare)
    for item in resultlist:
        errorlist += "<li><b>Line " + str(item["line"]) + ", column " + str(item["col"]) +  "</b>: " + item["desc"] + "<br>in <pre><code>" + item["body"] + "</code></pre></li>"
    errorlist += "</ul>"
    return "<html><head></head><body>Your score is: " + score + errorlist + "</body></html>"

def main(server_class=BaseHTTPServer.HTTPServer,
        handler_class=APIHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == '__main__':
    main()
