@echo off
echo ========================================
echo Quality Stocks API Server
echo ========================================
echo.

REM Check if Excel file exists
if not exist "data\trendlyne_data.xlsx" (
    echo ERROR: trendlyne_data.xlsx not found in data folder!
    echo Please place your Excel file at: data\trendlyne_data.xlsx
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Run the server
echo.
echo ========================================
echo Starting API Server...
echo ========================================
echo.
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

