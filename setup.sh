#!/bin/sh
pip install twilio
cd django-first
python manage.py makemigrations
python manage.py migrate
python manage.py runserver