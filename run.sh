#!/bin/bash


cd PRS_Project || exit  

source ../.venv/bin/activate  



python manage.py makemigrations --noinput
python manage.py migrate --noinput


python manage.py runserver