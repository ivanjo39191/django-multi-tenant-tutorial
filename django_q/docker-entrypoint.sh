#!/bin/bash

cd /opt/app/web/


# Start mscluster
echo "Starting mscluster"
python3.10 manage.py mscluster

exec "$@"