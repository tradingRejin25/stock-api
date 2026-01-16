# Setup Guide

## Python Installation

Python is not currently installed or not in your system PATH. Follow these steps:

### Option 1: Install Python from python.org (Recommended)

1. Download Python 3.11 or later from: https://www.python.org/downloads/
2. **IMPORTANT**: During installation, check the box "Add Python to PATH"
3. Run the installer and complete the installation
4. Restart your terminal/PowerShell

### Option 2: Install Python via Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. Python will be automatically added to PATH

### Verify Installation

After installing Python, verify it works:

```powershell
python --version
# Should show: Python 3.11.x or Python 3.12.x

python -m pip --version
# Should show: pip version
```

## Install Project Dependencies

Once Python is installed, navigate to this directory and run:

```powershell
# Navigate to project directory
cd C:\Work\Trading\stock_api_service

# First, upgrade pip (important for Windows)
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
python -m pip install -r requirements.txt
```

Or if `python` doesn't work, try:

```powershell
py -m pip install --upgrade pip setuptools wheel
py -m pip install -r requirements.txt
```

### If you get pandas build errors:

See **INSTALL_WINDOWS.md** for detailed troubleshooting steps. Quick fix:

```powershell
# Install pandas using pre-built wheels (no compilation needed)
python -m pip install --only-binary :all: pandas

# Then install other dependencies
python -m pip install fastapi uvicorn[standard] pydantic openpyxl python-multipart
```

## Alternative: Use Virtual Environment (Recommended)

It's best practice to use a virtual environment:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Run the API Server

After installing dependencies:

```powershell
python main.py
```

Or:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting

### "python is not recognized"
- Python is not installed or not in PATH
- Reinstall Python and ensure "Add Python to PATH" is checked
- Or use `py` launcher: `py -m pip install -r requirements.txt`

### "pip is not recognized"
- Use: `python -m pip install -r requirements.txt`
- Or: `py -m pip install -r requirements.txt`

### Permission Errors
- Run PowerShell as Administrator
- Or use a virtual environment (recommended)

### Module Not Found Errors
- Ensure you're in the project directory
- Ensure virtual environment is activated (if using one)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

