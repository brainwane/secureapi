#!/usr/bin/python

import BaseHTTPServer
import subprocess
import os
import string
import random

PORT = 8000

class APIHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    rbufsize = 0

    def do_POST(self):
        # Get interesting things from the request
        self.content_length = int(self.headers.get("Content-Length","0"))
        self.request_body = self.rfile.read(self.content_length)
        # Determine our response body
        self.response_body = parse_request(self.request_body)
        # Send our response
        self.send_response(200)
        self.send_header("Content-Length", str(len(self.response_body)))
        self.end_headers()
        self.wfile.write(self.response_body)

def name_file():
    basechars = string.letters + string.digits
    filename = ""
    for i in range(20):
        filename = filename + random.choice(basechars)
    filename = filename + ".c"
    return filename

def parse_request(request_body):
    """ take a request from the client, return the string to
    be used in the response body
    """
    filename = name_file()
    with open(filename, "w") as f:
        f.write(request_body)
    try:
        clang_result = subprocess.check_output(["bash", "shim.sh"], stderr=subprocess.STDOUT, universal_newlines=True)
    # TODO: must use new randomized filename as argument to shim.sh file!
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

