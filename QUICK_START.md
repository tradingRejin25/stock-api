# Quick Start - Quality Stocks API

## ✅ Server is Running!

When you see:
```
INFO:     Application startup complete.
```

**This is normal!** The server is running and waiting for requests. It's not stuck.

## 🧪 Test the API

### Option 1: Open in Browser

1. **API Documentation (Interactive)**:
   ```
   http://localhost:8000/docs
   ```
   - Click "Try it out" on any endpoint
   - Execute and see results

2. **Health Check**:
   ```
   http://localhost:8000/health
   ```

3. **Great Quality Stocks**:
   ```
   http://localhost:8000/api/quality-stocks/great
   ```
   ⚠️ **Note**: First request may take 10-30 seconds to load the Excel file!

4. **All Endpoints**:
   ```
   http://localhost:8000/
   ```

### Option 2: Use Test Script

Open a **new terminal window** and run:
```powershell
cd stock_api_service
.\test_server.bat
```

### Option 3: Use PowerShell

In a **new PowerShell window**:
```powershell
# Health check
Invoke-RestMethod http://localhost:8000/health

# Get great quality stocks
$response = Invoke-RestMethod http://localhost:8000/api/quality-stocks/great
Write-Host "Found $($response.count) great quality stocks"
```

## 📝 Available Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/quality-stocks/great` - Great quality stocks
- `GET /api/quality-stocks/aggressive` - Aggressive quality stocks
- `GET /api/quality-stocks/good` - Good quality stocks
- `GET /api/quality-stocks/all` - All quality stocks
- `GET /api/quality-stocks/stock/{nse_code}` - Get specific stock
- `GET /api/quality-stocks/search?query={query}` - Search stocks

## ⚠️ First Request Warning

The **first API request** will take longer (10-30 seconds) because:
1. The Excel file needs to be loaded
2. All stocks need to be parsed
3. Quality scores need to be calculated

Subsequent requests will be much faster!

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## ✅ Success Indicators

- Server shows: `INFO: Application startup complete.`
- Browser can access: `http://localhost:8000/docs`
- Health check returns: `{"status": "healthy"}`
- API endpoints return JSON data

If all of these work, your API is running successfully! 🎉



