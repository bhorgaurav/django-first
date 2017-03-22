#!/bin/sh
pip install Django
pip install twilio
cd ~
python manage.py makemigrations
python manage.py migrate
python manage.py runserver