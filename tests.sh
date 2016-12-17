#!/usr/bin/env bash


rm -rf tasks/*  jobs/*

curl -X POST --data '#!/usr/bin/env bash

echo "yeah!" >> ./output/file.txt
exit 0
' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

cat ./fileNotHere
echo "Two"
exit 0
' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo "Three"
exit 0
' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo $VAR1
echo $VAR2
sleep 5

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
  "taskid" : 2,
  "envvars" : {
    "VAR1" : "breaks",
    "VAR2" : "shell"
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

curl -X GET localhost:9876/jobs/1/status

curl -X GET localhost:9876/jobs/2/status

curl -X GET localhost:9876/jobs/3/status

exit 0
