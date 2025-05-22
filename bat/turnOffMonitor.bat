@echo off
REM Pythonの実行環境に応じて、以下のパスを適宜変更してください
set PYTHON_EXECUTABLE="C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe"

REM Pythonスクリプトのパスを指定します
set PYTHON_SCRIPT_PATH="C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules\useMonitor.py"

REM Pythonスクリプトを実行して関数を呼び出します
%PYTHON_EXECUTABLE% %PYTHON_SCRIPT_PATH% turn_off_monitor
