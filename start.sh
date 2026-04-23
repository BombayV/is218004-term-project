#!/bin/bash
mkdir -p media
npx tailwindcss -i ./input.css -o ./gamereviews/static/css/output.css
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn gamereviews.wsgi:application --bind 0.0.0.0:${PORT:-8000}
