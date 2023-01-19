# !/bin/bash
# --add-data="."
set +a
source .env
set -a

HOOKFILE=/tmp/.env-pydot.py

# activate the venv
source venv/bin/activate

# hack to set env vars in pyinstaller
echo """
import os
os.environ['OPENAI_API_KEY'] = '$OPENAI_API_KEY'
""" > $HOOKFILE

# check if mac and use --windowed flag
if [[ "$OSTYPE" == "darwin"* ]]; then
    FLAG="--windowed"
else
    FLAG=""
fi

pyinstaller --onefile  \
    --add-data="splash.png:splash.png" \
    $FLAG \
    --runtime-hook=$HOOKFILE \
    --path=venv/lib/python3.8/site-packages \
    --name=chatblast --osx-bundle-identifier=com.yourcompany.myapp app.py