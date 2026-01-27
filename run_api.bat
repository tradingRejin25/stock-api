@echo off
echo ========================================
echo   Stock API Service
echo ========================================
echo.
echo Starting server on http://localhost:8000
echo.
echo API Endpoints:
echo   - Nifty Stocks: http://localhost:8000/api/nifty-stocks
echo   - Trendlyne Stocks: http://localhost:8000/api/trendlyne-stocks
echo   - API Docs: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

cd /d %~dp0
python main.py

pause

