#!/bin/sh
python3 --version # Python 3.12.3
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to check python3 version: $status"
  exit $status
fi

pip --version # pip 24.0
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to check pip version: $status"
  exit $status
fi

python3 -m venv .venv
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to create virtual environment: $status"
  exit $status
fi

source .venv/bin/activate
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to activate virtual environment: $status"
  exit $status
fi

pip install -r requirements.txt
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to install requirements: $status"
  exit $status
fi

python3 manage.py collectstatic --noinput
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to collectstatic: $status"
  exit $status
fi

python3 manage.py makemigrations
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to makemigrations: $status"
  exit $status
fi
echo "makemigrations ->  OK"

python3 manage.py migrate
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to migrate: $status"
  exit $status
fi
echo "migrate ->  OK"

python3 manage.py shell < add_user.py
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to add user: $status"
  exit $status
fi
echo "super user ->  OK"


python3 manage.py runserver 0.0.0.0:8000
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to runserver: $status"
  exit $status
fi
echo "runserver ->  OK"
