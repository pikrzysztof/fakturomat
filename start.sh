#!/usr/bin/env bash
set -x
echo yes | python3 manage.py collectstatic --clear
exec python3 manage.py runserver 0.0.0.0:8080
