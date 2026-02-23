@echo off
echo ========================================
echo Quality Stocks API - Setup Checker
echo ========================================
echo.

REM Check current directory
echo Current directory:
cd
echo.

REM Check for Excel file in data folder
echo Checking for Excel file...
if exist "data\trendlyne_data.xlsx" (
    echo [OK] Excel file found at: data\trendlyne_data.xlsx
    echo.
) else (
    echo [ERROR] Excel file NOT found!
    echo.
    echo Please place your trendlyne_data.xlsx file at:
    echo   %CD%\data\trendlyne_data.xlsx
    echo.
    echo Or provide the full path when running the service.
    echo.
)

REM Check for Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version
    echo [OK] Python is installed
) else (
    echo [ERROR] Python is not installed or not in PATH
)
echo.

REM Check for virtual environment
echo Checking virtual environment...
if exist "venv" (
    echo [OK] Virtual environment exists
) else (
    echo [INFO] Virtual environment will be created on first run
)
echo.

REM Check requirements.txt
if exist "requirements.txt" (
    echo [OK] requirements.txt found
) else (
    echo [ERROR] requirements.txt not found!
)
echo.

echo ========================================
echo Setup Check Complete
echo ========================================
echo.
pause

