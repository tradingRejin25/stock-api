@echo off
echo Installing Stock API Service Dependencies...
echo.

REM Try python first
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using: python
    echo.
    echo Upgrading pip, setuptools, and wheel...
    python -m pip install --upgrade pip setuptools wheel
    echo.
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if %errorlevel% == 0 (
        goto :end
    )
    echo.
    echo Standard installation failed. Trying alternative method...
    echo Installing pandas from pre-built wheel...
    python -m pip install --only-binary :all: pandas
    echo Installing other dependencies...
    python -m pip install fastapi uvicorn[standard] pydantic openpyxl python-multipart
    goto :end
)

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using: py
    py -m pip install -r requirements.txt
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using: python3
    python3 -m pip install -r requirements.txt
    goto :end
)

echo ERROR: Python is not installed or not in PATH.
echo.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
echo Or run manually:
echo   python -m pip install -r requirements.txt
echo   OR
echo   py -m pip install -r requirements.txt
echo.
pause

:end
echo.
echo Installation complete!
echo.
echo To run the server:
echo   python main.py
echo.
pause

