#!/bin/sh

echo 'Creating python virtual environment "scripts/.venv"'
python3 -m venv scripts/.venv

echo 'Installing dependencies from "requirements.txt" into virtual environment'
./scripts/.venv/bin/python -m pip install -r requirements.txt

echo 'Running "python freeze"'
./scripts/.venv/bin/python ./freeze.py

# staticwebapp.config.json needs to be manually copyed because the swa-cli
# fails when it tries to do this copy when running within a build pipeline (Github and Azdo).
# See: https://github.com/Azure/static-web-apps-cli/issues/688
echo 'copying swa settings'
cp staticwebapp.config.json flaskapp/build/staticwebapp.config.json
