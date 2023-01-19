# !/bin/bash

# setup virtualenv
# set python version to 3.8
mkdir -p venv
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# if not in venv
# pip3 install -r requirements.txt