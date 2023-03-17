# !/bin/bash
pyinstaller --onefile --add-data="." --name=mychatblast --osx-bundle-identifier=com.chatblast.mychatblast app.py