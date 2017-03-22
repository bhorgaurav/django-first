#!/bin/sh
pip install Django
pip install twilio
python manage.py makemigrations
python manage.py migrate