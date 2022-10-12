#!/bin/bash
cd /opt/app/web/

# Apply database migrations
echo "Apply database migrations"
python3.10 manage.py migrate

# Start server
echo "Starting server"
# python3.10 manage.py runserver 0.0.0.0:8000
uwsgi --ini uwsgi.ini
exec "$@"
