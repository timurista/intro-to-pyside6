# !/bin/bash
THIS_DIRECTORY=$(pwd)/.env
pyinstaller --clean --onefile  --add-data="$THIS_DIRECTORY:." --name=mychatblast --osx-bundle-identifier=com.chatblast.mychatblast --icon=app.ico --windowed app.py
rm -rf /Applications/chatgpt.app
cp -r dist/mychatblast.app /Applications/chatgpt.app