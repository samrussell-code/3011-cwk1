@echo off

cd PRS_Project || exit

call ..\.venv\Scripts\activate

python manage.py makemigrations --noinput
python manage.py migrate --noinput

python manage.py runserver
