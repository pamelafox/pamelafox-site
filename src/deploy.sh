#!/bin/sh

echo 'Creating python virtual environment "scripts/.venv"'
python3 -m venv scripts/.venv

echo 'Installing dependencies from "requirements.txt" into virtual environment'
./scripts/.venv/bin/python -m pip install -r requirements.txt

echo 'Running "Build static web app"'
npx -y @azure/static-web-apps-cli@1.0.6 build

mv flaskapp/build ../swa-package
