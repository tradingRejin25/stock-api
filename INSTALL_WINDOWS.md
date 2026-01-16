# Windows Installation Guide

If you're encountering build errors when installing pandas, follow these steps:

## Method 1: Upgrade pip and install (Recommended)

```powershell
# Upgrade pip, setuptools, and wheel first
python -m pip install --upgrade pip setuptools wheel

# Then install dependencies
python -m pip install -r requirements.txt
```

## Method 2: Install pandas separately with pre-built wheels

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install pandas using only pre-built wheels (no compilation)
python -m pip install --only-binary :all: pandas

# Install other dependencies
python -m pip install fastapi uvicorn[standard] pydantic openpyxl python-multipart
```

## Method 3: Use conda (Alternative)

If pip continues to fail, consider using conda:

```powershell
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html

# Create a new environment
conda create -n stock_api python=3.11

# Activate environment
conda activate stock_api

# Install dependencies
conda install pandas openpyxl -c conda-forge
pip install fastapi uvicorn[standard] pydantic python-multipart
```

## Method 4: Install Visual C++ Build Tools

If you need to build pandas from source:

1. Download and install "Microsoft C++ Build Tools" from:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. During installation, select "C++ build tools" workload

3. Then try installing again:
   ```powershell
   python -m pip install --upgrade pip setuptools wheel
   python -m pip install -r requirements.txt
   ```

## Troubleshooting

### Error: "Microsoft Visual C++ 14.0 or greater is required"

- Install Visual C++ Build Tools (Method 4 above)
- Or use Method 2 to install pre-built wheels

### Error: "Failed building wheel for pandas"

- Use Method 2 (pre-built wheels)
- Or upgrade pip: `python -m pip install --upgrade pip`

### Error: "pip is out of date"

```powershell
python -m pip install --upgrade pip
```

### Still having issues?

Try installing each package individually:

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install fastapi
python -m pip install "uvicorn[standard]"
python -m pip install pydantic
python -m pip install --only-binary :all: pandas
python -m pip install openpyxl
python -m pip install python-multipart
```

## Verify Installation

After installation, verify everything works:

```powershell
python -c "import pandas; import fastapi; print('All packages installed successfully!')"
```

