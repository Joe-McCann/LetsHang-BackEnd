#!/bin/bash

. ./venv/bin/activate
gunicorn --reload letshang.app
