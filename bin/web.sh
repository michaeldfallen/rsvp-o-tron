#!/bin/sh

if [ "$DEBUG" == "True" ]; then
  python app.py runserver
else
  gunicorn app:app
fi
