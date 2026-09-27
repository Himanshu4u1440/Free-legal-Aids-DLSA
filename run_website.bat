@echo off
title DLSA Porbandar Citizen Portal
cd /d "%~dp0"
echo =======================================================
echo   Starting DLSA Porbandar Portal...
echo =======================================================
echo.
echo 1. Opening your web browser to http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
echo.
echo 2. Starting Flask Server (Keep this window OPEN while browsing)
echo    To stop the server later, press Ctrl+C or close this window.
echo =======================================================
echo.
python app.py
pause
