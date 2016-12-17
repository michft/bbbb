#!/usr/bin/env bash


rm -rf tasks/*  jobs/*

curl -X POST --data '#!/usr/bin/env bash

echo "yeah!"
' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo "Two"
' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo "Three"
' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo $VAR1
echo $VAR2
sleep 300

exit 0
' localhost:9876/tasks

curl -X GET localhost:9876/tasks/1

echo "tasks 3 before"
cat ./tasks/3/script.sh

curl -X PUT --data '#!/usr/bin/env bash

echo "Oh yeah!"
' localhost:9876/tasks/3

echo "tasks 3 after"
cat ./tasks/3/script.sh

curl -X POST --data '{
  "taskid" : 1,
  "envvars" : {
    "VAR1" : "VALUE",
    "VAR2" : "VALUE"
  }
}
' localhost:9876/jobs


curl -X POST --data '{
  "taskid" : 4,
  "envvars" : {
    "VAR1" : "Foo",
    "VAR2" : "Bar"
  }
}
' localhost:9876/jobs



exit 0
