#!/usr/bin/env python3

"""
handled Methods:
  POST /tasks
    In work code you put descriptions here.

  GET /tasks/:taskid
  PUT /tasks/:taskid
  POST /jobs
  GET /jobs/:jobid/status
  GET /jobs/:jobid/output/...path...

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen
import json, os, psutil, shutil

pids = 1
jid = 1

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

    elif lst_pth[3] == 'status':
      try:
        os.chdir( './' + lst_pth[1] + '/' + lst_pth[2] + '/output')
        with open ('./pid.txt' , 'r') as fh:
          st_dict = json.load(fh)
        try:
          print(psutil.Process(int(st_dict['pid'])).status)
          self.send_response(200)
          self.send_header('Content-type', 'text/json')
          self.end_headers()
          self.wfile.write(bytes('{"status" : "running"}\n' , 'utf-8'))
        except:
          self.send_response(200)
          self.send_header('Content-type', 'text/json')
          self.end_headers()
          if os.path.getsize('./errors.txt') == 0:
            self.wfile.write(bytes('{"status" : "success"}\n' , 'utf-8'))
          else:
            self.wfile.write(bytes('{"status" : "failed"}\n' , 'utf-8'))
        os.chdir('../../..')

      except:
        self.send_response(400)
        self.wfile.write(bytes('Something went wrong!\n', 'utf-8'))
        os.chdir('../../..')
    elif lst_pth[3] == 'output':
      try:
        os.chdir( './' + lst_pth[1] + '/' + lst_pth[2] + '/output')
        with open ( str(lst_pth[4]) , 'r') as fh:
          s = fh.read()
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(bytes( s , 'utf-8'))
        os.chdir('../../..')
      except:
        self.send_response(400)
        self.wfile.write(bytes('Something went wrong!\n', 'utf-8'))
        os.chdir('../../..')

    else:
      self.send_response(400)
      self.wfile.write(bytes('Something went wrong!\n', 'utf-8'))


  def do_PUT(self):
    path = self.path
    lst_pth = [x for x in path.split('/')]

    if lst_pth[1] == 'tasks':

      try:
        os.chdir( './' + lst_pth[1] + '/' + lst_pth[2])
        # Send response status code
        print('Updating ' + os.getcwd() + '/script.sh\n')
        length = self.headers['content-length']
        data = self.rfile.read(int(length))

        os.remove('./script.sh')

        with open ('./script.sh', 'w') as fh:
          fh.write(data.decode())

        os.chmod('./script.sh' , int(493)) # gets converted to 755 octal
        print(os.getcwd() + '/script.sh written.')
        self.send_response(202)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        #self.wfile.write(bytes('{"taskid" : ' + str(pids) + '}\n' , 'utf-8'))
        os.chdir('../..')

      except:
        self.send_response(404)
    else:
      self.send_response(400)



  def do_POST(self):
    if self.path == '/tasks':
# no sanity checking, no data varification

      try:
        global pids
        os.makedirs('./tasks/' + str(pids))
        os.chdir('./tasks/' + str(pids))

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
        self.send_response(400)

    elif self.path == '/jobs':
      try:
        global jid
        os.makedirs('./jobs/' + str(jid) + '/output')
        os.chdir('./jobs/' + str(jid) + '/output')

        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        job_dict = json.loads(data.decode())
        shutil.copyfile('../../../tasks/' + str(job_dict['taskid']) + '/script.sh', './script.sh' )
        os.chmod('./script.sh', int(493))

        fout = open ('./result.txt' , 'w')
        ferr = open ('./errors.txt' , 'w')
        p = Popen(['./script.sh'], stdout=fout, stderr=ferr, env=job_dict['envvars'])
        fout.close()
        ferr.close()
        fpid = open ('./pid.txt', 'w')
        fpid.write('{"pid" : ' + str(p.pid) + "}")
        fpid.close()

        self.send_response(202)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(bytes('{"jobid" : ' + str(jid) + '}\n' , 'utf-8'))
        jid += 1
        os.chdir('../../..')

      except:
        print('../../../tasks/' + str(job_dict['taskid']) + '/script.sh' )
        self.send_response(418)

    else:
      self.send_response(400)


def run():
  print('starting server...')

  # Server settings
  PORT = 9876
  server_address = ('127.0.0.1', PORT)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server on port ...', PORT)
  httpd.serve_forever()


run()
