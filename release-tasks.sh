#!/bin/bash
set -e

if [ -n "$1" ]; then
    exec "$@"
fi

python src/manage.py collectstatic --noinput  # Collect static files
