@echo off
echo ========================================
echo Testing Quality Stocks API
echo ========================================
echo.

echo Testing health endpoint...
curl http://localhost:8000/health
echo.
echo.

echo Testing root endpoint...
curl http://localhost:8000/
echo.
echo.

echo Testing great quality stocks (first request may take time to load Excel)...
curl http://localhost:8000/api/quality-stocks/great
echo.
echo.

echo ========================================
echo Test complete!
echo ========================================
echo.
echo If you see JSON responses above, the API is working!
echo.
pause



