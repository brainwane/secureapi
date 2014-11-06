#!/usr/bin/python

import BaseHTTPServer

PORT = 8000

class APIHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    rbufsize = 0

    def do_POST(self):
        self.send_response(200)
        self.body = self.rfile.read(2)
        self.to_send = "HTTP/1.1 200 OK\n\nThis is a response.\n"
        self.send_header("Content-Length", str(len(self.to_send)))
        self.end_headers()
        print self.body
        self.wfile.write(self.to_send)



def main(server_class=BaseHTTPServer.HTTPServer,
        handler_class=APIHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == '__main__':
    main()

