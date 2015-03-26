#!/bin/sh

python app.py db upgrade

if [ "$DEBUG" == "True" ]; then
  python app.py runserver
else
  gunicorn app:app
fi
