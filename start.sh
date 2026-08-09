#!/usr/bin/env bash
set -e

echo "==> Running migrations..."
python manage.py migrate

echo "==> Creating admin accounts..."
python manage.py create_admin

echo "==> Starting server..."
exec gunicorn guesthouse_system.wsgi:application
