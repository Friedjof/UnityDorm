#!/bin/sh
set -eu

echo "Starting application setup..."

# Apply committed database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Avoid image processing work on the first visitor request
python manage.py warm_image_cache

# Collect static files
python manage.py collectstatic --noinput

# Create the configured superuser once
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  if ! python manage.py shell -c 'import os, sys; from django.contrib.auth import get_user_model; sys.exit(0 if get_user_model().objects.filter(username=os.environ["DJANGO_SUPERUSER_USERNAME"]).exists() else 1)'; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
  fi
fi

# Start Gunicorn server for production
echo "Starting Gunicorn server..."
exec gunicorn UnityDorm.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-2}" \
  --access-logfile - \
  --error-logfile -
