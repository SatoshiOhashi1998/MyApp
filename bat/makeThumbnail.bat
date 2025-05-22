@echo off

rem MyAppディレクトリに移動
cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\python

rem Python仮想環境を有効にする
call C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\activate.bat

rem makeThumbnail.py を実行する
python makeThumbnail.py

rem Python仮想環境を無効にする（任意）
deactivate
