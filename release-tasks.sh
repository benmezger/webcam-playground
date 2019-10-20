#!/bin/bash
set -e

if [ -n "$1" ]; then
    exec "$@"
fi

python manage.py collectstatic --noinput  # Collect static files
