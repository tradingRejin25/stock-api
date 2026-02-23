@echo off
echo ========================================
echo Quality Stocks API Server
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check for Excel file
set EXCEL_FOUND=0
if exist "data\trendlyne_data.xlsx" (
    set EXCEL_FOUND=1
    echo [OK] Excel file found
) else (
    echo [WARNING] Excel file not found in data folder
    echo.
    echo The API will try to find the Excel file automatically.
    echo If it fails, place trendlyne_data.xlsx at:
    echo   %CD%\data\trendlyne_data.xlsx
    echo.
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo Installing/updating dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Run the server
echo.
echo ========================================
echo Starting API Server...
echo ========================================
echo.
echo API will be available at:
echo   - Main: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo   - Health: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

