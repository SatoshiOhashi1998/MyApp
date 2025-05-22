@echo off
echo Starting batch file...
set WEATHER_API_KEY=036123f356b5b3c1131d9da0dc46da88
set GAS_WEATHER_URL=https://script.google.com/macros/s/AKfycbzt4mtyCp6EsitzOSmGRuKH78SepE60GrKvY2PxlheVTT6ZwyvFQzX_ybW9LgRKb7x4/exec

echo Changing directory...
cd C:\Users\user\PycharmProjects\MyUtilProject\MyApp\FlaskApp\app\modules

echo Executing Python script...
C:\Users\user\PycharmProjects\MyUtilProject\venv\Scripts\python.exe getWeatherData.py