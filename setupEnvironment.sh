#!/bin/bash

if [ -d "venv" ]; then
  echo "[Removing the existing venv folder]"
  rm -rf venv
fi

echo "[Create the virtual environment]"
virtualenv venv -p /usr/bin/python3
source ./venv/bin/activate

echo "[Install Falcon and Gunicorn]"
apt-get install build-essential python3-dev
pip install cython
pip install --no-binary :all: falcon
pip install gunicorn

echo "[Install dependencies]"
pip install  --target ./venv/lib --requirement requirements.txt

echo "[install missing packages]"
pip install requests
pip install firebase_admin
pip install googlemaps
pip install gmaps 
pip install python-google-places
pip install falcon-cors
pip install ptvsd

echo "[Remember to activate the virtual environment before running gunicorn]"
