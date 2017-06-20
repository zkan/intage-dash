#!/bin/bash
while ! nc -z db 5432; do sleep 1; done
sleep 5
cd $APPLICATION_ROOT\intage_dash
python manage.py migrate --settings=intage_dash.settings
python manage.py collectstatic --noinput --settings=intage_dash.settings
uwsgi --ini $APPLICATION_ROOT\uwsgi.ini
