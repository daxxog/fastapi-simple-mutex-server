#!/bin/bash
# to use this -->
# source ./env.sh

pyenv install -s
if [ ! -d env ]; then
    python3 -m venv env
    source env/bin/activate
    env/bin/pip install --upgrade pip setuptools wheel
    env/bin/pip install -r requirements.dev.txt
else
    source env/bin/activate
fi
