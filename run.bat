@echo off
echo Starting Stock API Service...
echo.

REM Try python first
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using: python
    python main.py
    goto :end
)

REM Try py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using: py
    py main.py
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using: python3
    python3 main.py
    goto :end
)

echo ERROR: Python is not installed or not in PATH.
echo.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit 1

:end

