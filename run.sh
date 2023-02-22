#!/bin/bash
python3 -m venv ./pyvenv
./pyvenv/bin/pip3 install -r requirements.txt
./pyvenv/bin/python3 manage.py makemigrations --run-syncdb
./pyvenv/bin/python3 manage.py migrate --run-syncdb
docker-compose up --build