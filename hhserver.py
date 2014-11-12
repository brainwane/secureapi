#!/usr/bin/python

import BaseHTTPServer
import subprocess
import os
import string
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
        else:
            self.code = self.request_body
        # Determine our response body
        if self.path == "/api/v1/analyze/":
            self.response_body = parse_request(self.code)
        else:
            self.response_body = "<html><head></head><body>This is your reportcard.</body></html>" # TODO -- parse_request, and then a bunch of other stuff for HTML version
        # Send our response
        self.send_response(200)
        self.send_header("Content-Length", str(len(self.response_body)))
        if self.path == "/api/v1/analyze/":
            self.send_header("Content-Type", "application/json")
        else:
            self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.response_body)

# add conditional
# webservice goes down 1 path, browser-based requests down another

# if self.path = /api/v1/analyze:
#    do foo


    def do_GET(self):
        self.send_response(200)
        with open("index.html") as f:
            self.response_body = f.read()
        self.send_header("Content-Length", str(len(self.response_body)))
        self.end_headers()
        self.wfile.write(self.response_body)

        # TODO: set up a different GET response for webservice requests
        # that sends a capabilities doc suggesting a POST template

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

def main(server_class=BaseHTTPServer.HTTPServer,
        handler_class=APIHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == '__main__':
    main()

