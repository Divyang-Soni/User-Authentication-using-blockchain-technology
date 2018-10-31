#!/bin/bash
echo 'Activate Virtual Env'
. ~/venv3/bin/activate
echo 'Installing Dependencies'
pip install -r requirements.txt
echo 'Run api Server'
python app.py