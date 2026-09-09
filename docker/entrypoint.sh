#!/usr/bin/env sh
set -e

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  python manage.py migrate --noinput
  # Container images include prebuilt static assets; local mounts can regenerate them.
  if [ ! -f /app/staticfiles/staticfiles.json ]; then
    python manage.py collectstatic --noinput
  fi
fi

exec "$@"
