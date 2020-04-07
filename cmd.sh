#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
    echo "Running Development server"
    exec python "identidock.py"
else
    echo "Running Production server"
    exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app/identidock.py --callable app --stats 0.0.0.0:9191
fi
