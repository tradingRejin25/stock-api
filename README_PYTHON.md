# Python version for stock_api_service

Use **Python 3.11 or 3.12**. Python 3.14 is not yet supported by many dependencies (no pre-built wheels; building from source requires Rust).

- **Windows:** Install from [python.org](https://www.python.org/downloads/) (3.11 or 3.12) and ensure it is on PATH, or use the Windows Store / `py` launcher.
- **Render:** Already set to 3.11.7 in `render.yaml`.

## Quick setup (Windows)

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/
2. Open a new terminal in `stock_api_service` and create a venv with that Python:
   ```powershell
   py -3.11 -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   If you only have 3.12: `py -3.12 -m venv venv`
3. Run the API: `uvicorn main:app --reload`
