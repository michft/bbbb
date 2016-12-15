#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os


pids = 1

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):


  # GET
  def do_GET(self):
      if self.path == '/tasks':
        os.chdir('./tasks')
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = 'Hello world!' + os.getcwd()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, 'utf8'))
        os.chdir('..')

      else :
        #Id = self.path.split('/')
        os.chdir('./tasks')
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = 'LA ' + os.getcwd()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, 'utf8'))
        os.chdir('..')



  def do_PUT(self):
    os.chdir('/tasks')
    os.chdir('..')

  def do_POST(self):

# no sanity checking, no data varification
      os.chdir('./tasks')
      global pids

      try:
        os.mkdir('./' + str(pids))
      except:
        pass
      os.chdir('./' + str(pids))
      print(os.getcwd())
      pids += 1
      os.chdir('../..')

def run():
  print('starting server...')

  # Server settings
  PORT = 9876
  server_address = ('127.0.0.1', PORT)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server on port ...', PORT)
  httpd.serve_forever()


run()
