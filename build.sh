#!/usr/bin/env bash
# exit or error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-imput
python manage.py migrate