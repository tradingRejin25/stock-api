# Step-by-Step Guide: Running Quality Stocks API

## Prerequisites
- Python 3.11 or later installed
- Excel file: `trendlyne_data.xlsx` in the `data` folder

---

## Step 1: Verify Excel File Location

Make sure your Excel file is here:
```
stock_api_service/
  └── data/
      └── trendlyne_data.xlsx  ← Your file should be here
```

**Check:**
- Open File Explorer
- Navigate to: `C:\Work\Trading\stock_ai\stock_api_service\data\`
- Verify `trendlyne_data.xlsx` exists

---

## Step 2: Open Terminal/PowerShell

1. Press `Windows Key + X`
2. Select **"Windows PowerShell"** or **"Terminal"**
3. Or press `Windows Key + R`, type `powershell`, press Enter

---

## Step 3: Navigate to Project Directory

In PowerShell, type:
```powershell
cd C:\Work\Trading\stock_ai\stock_api_service
```

Press Enter.

**Verify you're in the right place:**
```powershell
pwd
```
Should show: `C:\Work\Trading\stock_ai\stock_api_service`

---

## Step 4: Run the API Server

### Option A: Using Batch Script (Easiest)

Simply double-click:
```
run_api_simple.bat
```

Or in PowerShell:
```powershell
.\run_api_simple.bat
```

### Option B: Manual Setup

If the batch script doesn't work, do it manually:

**4a. Create Virtual Environment (first time only):**
```powershell
python -m venv venv
```

**4b. Activate Virtual Environment:**
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

**4c. Install Dependencies:**
```powershell
pip install fastapi uvicorn pydantic pandas openpyxl numpy
```

**4d. Run the Server:**
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Step 5: Verify Server is Running

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**This is normal!** The server is running and waiting for requests.

---

## Step 6: Test the API

### Test 1: Health Check (Quick Test)

Open in browser:
```
http://localhost:8000/health
```

**Expected:** `{"status": "healthy"}`

### Test 2: Interactive API Documentation (Best for Testing)

Open in browser:
```
http://localhost:8000/docs
```

**What to do:**
1. You'll see all available endpoints
2. Click on any endpoint (e.g., "GET /api/quality-stocks/great")
3. Click **"Try it out"** button
4. Click **"Execute"** button
5. See the response below

### Test 3: Test Great Quality Stocks

Open in browser:
```
http://localhost:8000/api/quality-stocks/great
```

**Note:** First request may take 10-30 seconds to load the Excel file.

**Expected:** JSON response with stocks array

### Test 4: Debug Endpoint (Check if Data is Loading)

Open in browser:
```
http://localhost:8000/api/quality-stocks/debug/info
```

**This shows:**
- Total stocks loaded
- Excel file path
- Sample stock data
- How many meet criteria

---

## Step 7: Available Endpoints

Once the server is running, you can access:

| Endpoint | URL | Description |
|----------|-----|-------------|
| **API Docs** | http://localhost:8000/docs | Interactive documentation |
| **Health** | http://localhost:8000/health | Server health check |
| **Root** | http://localhost:8000/ | API information |
| **Great Quality** | http://localhost:8000/api/quality-stocks/great | Great quality stocks |
| **Aggressive** | http://localhost:8000/api/quality-stocks/aggressive | Aggressive quality stocks |
| **Good Quality** | http://localhost:8000/api/quality-stocks/good | Good quality stocks |
| **All Stocks** | http://localhost:8000/api/quality-stocks/all | All quality stocks |
| **Debug Info** | http://localhost:8000/api/quality-stocks/debug/info | Debug information |
| **Search** | http://localhost:8000/api/quality-stocks/search?query=tata | Search stocks |
| **Stock by Code** | http://localhost:8000/api/quality-stocks/stock/RELIANCE | Get specific stock |

---

## Step 8: Stop the Server

When you're done:
1. Go to the terminal where the server is running
2. Press `Ctrl + C`
3. Server will stop

---

## Troubleshooting

### Issue: "Excel file not found"

**Solution:**
1. Check file location: `stock_api_service\data\trendlyne_data.xlsx`
2. Verify file name is exactly: `trendlyne_data.xlsx`
3. Check file isn't open in Excel

### Issue: "Port 8000 already in use"

**Solution:**
1. Close other applications using port 8000
2. Or change port in command: `--port 8001`
3. Then access: `http://localhost:8001`

### Issue: "Module not found" or "No module named 'pandas'"

**Solution:**
1. Make sure virtual environment is activated (you should see `(venv)` in terminal)
2. Run: `pip install -r requirements.txt`
3. Or: `pip install fastapi uvicorn pydantic pandas openpyxl numpy`

### Issue: "Execution Policy" error in PowerShell

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try again.

### Issue: "Internal Server Error"

**Solution:**
1. Check the terminal for error messages
2. Try the debug endpoint: `http://localhost:8000/api/quality-stocks/debug/info`
3. Check if Excel file has all required columns
4. Look for error messages in the terminal output

### Issue: "0 stocks returned"

**Possible causes:**
1. Excel file not loading (check debug endpoint)
2. Filtering criteria too strict
3. Data format mismatch

**Solution:**
1. Check debug endpoint to see if stocks are loading
2. Check sample stocks in debug output
3. Verify Excel file has correct column names

---

## Quick Reference Commands

```powershell
# Navigate to directory
cd C:\Work\Trading\stock_ai\stock_api_service

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn pydantic pandas openpyxl numpy

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use batch script
.\run_api_simple.bat
```

---

## Success Indicators

✅ Server shows: `INFO: Application startup complete.`  
✅ Browser can access: `http://localhost:8000/docs`  
✅ Health check returns: `{"status": "healthy"}`  
✅ API endpoints return JSON data (even if empty array)

If all of these work, your API is running successfully! 🎉

---

## Next Steps

Once the API is running:
1. Test endpoints using the interactive docs at `/docs`
2. Integrate with your Flutter app
3. Deploy to production (Render, Heroku, etc.)

---

## Need Help?

If you encounter issues:
1. Check the terminal for error messages
2. Try the debug endpoint: `/api/quality-stocks/debug/info`
3. Verify Excel file is in the correct location
4. Check that all dependencies are installed



