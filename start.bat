@echo off
echo Instaluji zavislosti...
pip install -r requirements.txt --quiet
echo.
echo Spoustim server...
python server.py
pause
