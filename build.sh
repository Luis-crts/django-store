#!/usr/bin/env bash
# exit or error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noimput
python manage.py migrate