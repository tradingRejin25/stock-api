@echo off
echo ========================================
echo   Nifty Stocks API Server
echo ========================================
echo.
echo Starting server on http://localhost:8000
echo.
echo Press CTRL+C to stop the server
echo.

cd /d %~dp0
python main.py

pause

