#!/usr/bin/env python3

import requests

# POST /tasks

resp = requests.post('http://127.0.0.1:9000/tasks')
if resp.status_code != 201:
  raise ApiError('Cannot create task: {}'.format(resp.status_code))
print('Created task. ID: {}'.format(resp.json()['id']))

# GET /tasks/:taskid

# PUT /tasks/:taskid

# POST /jobs

# GET /jobs/:jobid/status

# GET /jobs/:jobid/output/...path...


