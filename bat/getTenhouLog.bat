@echo off
set GAS_TENHOU_URL=https://script.google.com/macros/s/AKfycbxCZUJml-rng19HJVbitlHET5P0zFSZc2F3JlOgGJKO-0CXAdsPnmPpy3XAkgSjySEufA/exec

set DOWNLOADS_DIR=C:\Users\user\Downloads
set EXCEL_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\excel
set CSV_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\csv
set JSON_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\json
set CURSOR_DIR=C:\Users\user\Desktop\mouse-cursor

cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe download_processor.py
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getTenhouLog.py