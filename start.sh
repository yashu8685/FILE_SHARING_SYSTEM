#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn FS.wsgi:application --bind 0.0.0.0:$PORT

#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn FS.wsgi:application