@echo off
echo ========================================
echo Testing Quality Stocks API
echo ========================================
echo.

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

REM Run tests
echo.
echo Running service tests...
echo.
python test_service.py

echo.
pause



