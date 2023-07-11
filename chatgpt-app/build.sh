# !/bin/bash
THIS_DIRECTORY=$(pwd)/.env
pyinstaller --onefile  --add-data="$THIS_DIRECTORY:." --name=mychatblast --osx-bundle-identifier=com.chatblast.mychatblast app.py
rm /Applications/chatgpt
cp dist/mychatblast /Applications/chatgpt