#!/usr/bin/python

import BaseHTTPServer

PORT = 8000

class APIHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
#        self.body = self.rfile.read(2)
#        self.send_header("Content-Length", str(2))
#        self.end_headers()
        self.wfile.write("yo")



def main(server_class=BaseHTTPServer.HTTPServer,
        handler_class=APIHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == '__main__':
    main()

