@echo off
echo ========================================
echo Simple Dependency Installer
echo Uses latest versions with pre-built wheels
echo ========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies (latest versions with wheels)...
pip install fastapi uvicorn[standard] pydantic pandas openpyxl numpy

echo.
echo ========================================
echo Installation complete!
echo ========================================
pause



