#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

pids = 1

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):


  # GET
  def do_GET(self):
    path = self.path
    lst_pth = [x for x in path.split('/')]

    if lst_pth[1] == 'tasks':

      try:
        os.chdir( './' + lst_pth[1] + '/' + lst_pth[2])
        # Send response status code
        print(os.getcwd())

        with open('./script.sh') as fh:
          self.send_response(200)
          self.send_header('Content-type', 'text/json')
          self.end_headers()
          self.wfile.write(fh.read().encode())
        os.chdir('../..')

      except:
        self.send_response(400)
        self.wfile.write(bytes('Something went wrong!\n', 'utf-8'))

    else :
        #Id = self.path.split('/')

        os.chdir('./tasks')
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')

        # Send message back to client
        message = 'LA ' + os.getcwd()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, 'utf8'))
        os.chdir('..')



  def do_PUT(self):
    os.chdir('./tasks')
    os.chdir('..')

  def do_POST(self):
    if self.path == '/tasks':
# no sanity checking, no data varification
      global pids

      try:
        os.chdir('./tasks')
        os.mkdir('./' + str(pids))
        os.chdir('./' + str(pids))
        length = self.headers['content-length']
        data = self.rfile.read(int(length))

        with open ('./script.sh', 'w') as fh:
          fh.write(data.decode())

        os.chmod('./script.sh' , int(493)) # gets converted to 755 octal
        print(os.getcwd() + '/script.sh written.')
        self.send_response(201)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(bytes('{"taskid" : ' + str(pids) + '}\n' , 'utf-8'))
        pids += 1
        os.chdir('../..')

      except:
        return self.send_response(400)


def run():
  print('starting server...')

  # Server settings
  PORT = 9876
  server_address = ('127.0.0.1', PORT)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server on port ...', PORT)
  httpd.serve_forever()


run()
