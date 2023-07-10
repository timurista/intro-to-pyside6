# !/bin/bash
pyinstaller --onefile --add-data='.env:.env' --name=mychatblast --osx-bundle-identifier=com.chatblast.mychatblast app.py