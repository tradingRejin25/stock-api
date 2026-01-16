# Quick Installation Guide

## If pandas installation is failing, follow these steps:

### Step 1: Run the fix script

```powershell
cd C:\Work\Trading\stock_api_service
.\install_pandas_fix.ps1
```

This script will:
- Find your Python installation
- Upgrade pip
- Install pandas using pre-built wheels
- Install all other dependencies
- Verify the installation

### Step 2: Manual installation (if script doesn't work)

Open PowerShell or Command Prompt and run:

```powershell
# Navigate to project
cd C:\Work\Trading\stock_api_service

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install pandas (try pre-built wheels first)
python -m pip install --only-binary :all: pandas

# If that fails, try without the flag
python -m pip install pandas

# Install other packages one by one
python -m pip install fastapi
python -m pip install "uvicorn[standard]"
python -m pip install pydantic
python -m pip install openpyxl
python -m pip install python-multipart
```

### Step 3: Verify installation

```powershell
python -c "import pandas; import fastapi; print('Success!')"
```

### Step 4: Run the server

```powershell
python main.py
```

## Common Issues

### "python is not recognized"
- Use `py` instead: `py -m pip install pandas`
- Or add Python to PATH (reinstall Python with "Add to PATH" checked)

### "pip is not recognized"
- Use: `python -m pip install pandas`
- Or: `py -m pip install pandas`

### "Failed building wheel for pandas"
- Use: `python -m pip install --only-binary :all: pandas`
- This forces pre-built wheels (no compilation needed)

### "Microsoft Visual C++ 14.0 required"
- Install Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use: `python -m pip install --only-binary :all: pandas`

## Still having issues?

1. Check Python version: `python --version` (should be 3.8+)
2. Check pip version: `python -m pip --version`
3. Upgrade pip: `python -m pip install --upgrade pip`
4. Try installing in a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --only-binary :all: pandas
python -m pip install fastapi uvicorn[standard] pydantic openpyxl python-multipart
```

