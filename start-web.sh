#!/bin/sh

set -euo pipefail

python manage.py collectstatic --no-input
python manage.py migrate
if [[ "$DJANGO_ENV" = "PRODUCTION" ]]; then
  gunicorn -b 0.0.0.0:8000 \
    --log-level ${DJANGO_LOG_LEVEL,,} \
    --access-logfile - app.wsgi:application
else
  python manage.py runserver 0.0.0.0:8000
fi
