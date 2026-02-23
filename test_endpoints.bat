@echo off
echo ========================================
echo Testing API Endpoints
echo ========================================
echo.
echo Make sure the API server is running first!
echo (Run run_api.bat in another terminal)
echo.
pause

echo.
echo Testing endpoints...
echo.

echo 1. Testing root endpoint...
curl http://localhost:8000/
echo.
echo.

echo 2. Testing health check...
curl http://localhost:8000/health
echo.
echo.

echo 3. Testing great quality stocks (first 3)...
curl "http://localhost:8000/api/quality-stocks/great" | python -m json.tool | head -n 50
echo.
echo.

echo 4. Testing search...
curl "http://localhost:8000/api/quality-stocks/search?query=tata&limit=3" | python -m json.tool
echo.
echo.

echo Tests completed!
pause



