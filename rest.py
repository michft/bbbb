#!/usr/bin/env python3

import http.server
import socketserver
import requests


PORT = 9000

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Service on : " , PORT)
httpd.serve_forever()







