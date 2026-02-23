@echo off
echo Installing dependencies with pre-built wheels...
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
echo Installing numpy first (with pre-built wheel)...
pip install --only-binary :all: numpy>=2.0.0

echo.
echo Installing pandas (with pre-built wheel)...
pip install --only-binary :all: pandas>=2.2.0

echo.
echo Installing other dependencies (with pre-built wheels)...
pip install --only-binary :all: fastapi>=0.115.0 uvicorn>=0.32.0 pydantic>=2.10.0 openpyxl>=3.1.0

echo.
echo Done!
pause

