#!/bin/sh

set -euo pipefail

python manage.py collectstatic --no-input
python manage.py migrate
if [[ "$DJANGO_ENV" = "PRODUCTION" ]]; then
  DJANGO_LOG_LEVEL_LOWER=$(echo "$DJANGO_LOG_LEVEL" | tr '[:upper:]' '[:lower:]')
  gunicorn -b 0.0.0.0:8000 app.wsgi:application
else
  python manage.py runserver 0.0.0.0:8000
fi
