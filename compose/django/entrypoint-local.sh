#!/bin/bash
while ! nc -z db 5432; do sleep 1; done
cd $APPLICATION_ROOT\intage_dash
python manage.py migrate --settings=intage_dash.settings
python manage.py runserver 0.0.0.0:8000 --settings=intage_dash.settings
