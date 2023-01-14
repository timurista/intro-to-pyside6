# !/bin/bash
# --add-data="."
pyinstaller --onefile --add-data="." --name=myapp --osx-bundle-identifier=com.yourcompany.myapp app.py