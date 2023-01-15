# !/bin/bash

# setup virtualenv
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# if not in venv
# pip3 install -r requirements.txt