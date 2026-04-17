@echo off
:: Požádej o admin práva pokud je nemáme
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Přejdi do složky kde leží start.bat
cd /d "%~dp0"

echo Instaluji zavislosti...
pip install -r requirements.txt --quiet
echo.
echo Spoustim server...
python server.py
pause
