@echo off
set YOUTUBE_API_KEY=AIzaSyCfnk8M5KndLVlsoEWJt3nOEVf0okdTozw
set YOUTUBE_LIVE_LIST=PLGQ23FYBgLigZDElGcDl-h6AnslEdF3Lg
set YOUTUBE_MUSIC_LIST=PLGQ23FYBgLijz6a3PcjLwt8lDzCyQUoGo
set SAVE_EXCEL_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\excel
set SAVE_EXCEL_MUSIC_FILE=vtuber_song.xlsm
set SAVE_EXCEL_LIVE_FILE=streaming_data.xlsx

cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe run_get_music_data.py