#!/usr/bin/env bash
rm -rf tasks/*
curl -X POST --data '#!/usr/bin/env bash

echo "yeah!"' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo "Two"' localhost:9876/tasks

curl -X POST --data '#!/usr/bin/env bash

echo "Three"' localhost:9876/tasks


