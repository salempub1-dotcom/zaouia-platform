#!/usr/bin/env sh
set -e

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  python manage.py migrate --noinput
  if [ -n "${ZAOUIA_ADMIN_EMAIL:-}" ] || [ -n "${ZAOUIA_ADMIN_PASSWORD:-}" ]; then
    python manage.py bootstrap_admin
  fi
  # Container images include prebuilt static assets; local mounts can regenerate them.
  if [ ! -f /app/staticfiles/staticfiles.json ]; then
    python manage.py collectstatic --noinput
  fi
fi

# Do not pass bootstrap credentials to Gunicorn or Celery child processes.
unset ZAOUIA_ADMIN_EMAIL ZAOUIA_ADMIN_PASSWORD
exec "$@"
