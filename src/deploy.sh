#!/bin/sh

echo 'Creating python virtual environment "scripts/.venv"'
python3 -m venv scripts/.venv

echo 'Installing dependencies from "requirements.txt" into virtual environment'
./scripts/.venv/bin/python -m pip install -r requirements.txt

echo 'Running "Python Freeze"'
./scripts/.venv/bin/python ./freeze.py
