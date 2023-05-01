#!/bin/sh
apt install python3

# mkdir restify
# cd restify

# python3 -m venv env
source env/bin/activate

python3 -m pip install django
python3 -m pip install djangorestframework
python3 -m pip install django-filter

cd restify

python3 manage.py makemigrations comments
python3 manage.py makemigrations notif
python3 manage.py makemigrations property
python3 manage.py migrate 


