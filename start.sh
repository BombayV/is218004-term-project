#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn gamereviews.wsgi:application --bind 0.0.0.0:${PORT:-8000}
