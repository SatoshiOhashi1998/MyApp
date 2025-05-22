@echo off
set YOUTUBE_API_KEY=AIzaSyCfnk8M5KndLVlsoEWJt3nOEVf0okdTozw
set USE_LIST_ID=PLGQ23FYBgLijz6a3PcjLwt8lDzCyQUoGo
set YOUTUBE_LIVE_LIST=PLGQ23FYBgLigZDElGcDl-h6AnslEdF3Lg
set YOUTUBE_MUSIC_LIST=PLGQ23FYBgLijz6a3PcjLwt8lDzCyQUoGo
set SAVE_EXCEL_DIR=C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\excel
set SAVE_EXCEL_MUSIC_FILE=vtuber_song.xlsm
set SAVE_EXCEL_LIVE_FILE=streaming_data.xlsx
set WEATHER_API_KEY=036123f356b5b3c1131d9da0dc46da88
set GAS_WEATHER_URL=https://script.google.com/macros/s/AKfycbzt4mtyCp6EsitzOSmGRuKH78SepE60GrKvY2PxlheVTT6ZwyvFQzX_ybW9LgRKb7x4/exec
set GAS_YouTube_URL=https://script.google.com/macros/s/AKfycbyXCmQ4AESueg8a8TSXpqo2ZGpMzhaY95CqBYkNnPq9QAYpHmAq509W8rGPalFXqtl8XA/exec
set GAS_YM_URL=https://script.google.com/macros/s/AKfycbyDF8ylIK6H_M3f3mdLVXOjaMJBCaGgXe53qTEZjXnadNr9dBsFFdMFE8e3uleSOEdIrA/exec
set GAS_TENHOU_URL=https://script.google.com/macros/s/AKfycbxCZUJml-rng19HJVbitlHET5P0zFSZc2F3JlOgGJKO-0CXAdsPnmPpy3XAkgSjySEufA/exec

cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules
rem cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\python
rem C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getYouTubePlaylist.py
rem C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getYmHistory.py
rem C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getYouTubeLive.py
rem C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe testUseXlsm.py
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getYouTubeChat.py
rem C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe useChatData.py
