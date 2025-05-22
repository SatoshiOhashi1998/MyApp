@echo off
set YOUTUBE_API_KEY=AIzaSyCfnk8M5KndLVlsoEWJt3nOEVf0okdTozw
set GAS_YouTube_URL=https://script.google.com/macros/s/AKfycbyXCmQ4AESueg8a8TSXpqo2ZGpMzhaY95CqBYkNnPq9QAYpHmAq509W8rGPalFXqtl8XA/exec
set GAS_YM_URL=https://script.google.com/macros/s/AKfycbyDF8ylIK6H_M3f3mdLVXOjaMJBCaGgXe53qTEZjXnadNr9dBsFFdMFE8e3uleSOEdIrA/exec

set DOWNLOADS_DIR=C:\Users\user\Downloads
set EXCEL_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\excel
set CSV_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\csv
set JSON_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\json
set CURSOR_DIR=C:\Users\user\Desktop\mouse-cursor

cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe download_processor.py
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getYmHistory.py
