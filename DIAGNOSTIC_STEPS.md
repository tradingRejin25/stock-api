# Diagnostic Steps for 0 Stocks Issue

## Step 1: Check if Stocks are Loading

Open in browser:
```
http://localhost:8000/api/quality-stocks/debug/info
```

**Look for:**
- `total_stocks_loaded`: Should be > 0
- `excel_file_exists`: Should be `true`
- `sample_stocks`: Should show sample data

**If `total_stocks_loaded` is 0:**
- Excel file is not loading
- Check file path in the response
- Verify file exists at that location

## Step 2: Check Sample Stock Data

In the debug endpoint response, check the `sample_stocks` array.

**Look at the values:**
- Are ROE, ROCE values reasonable? (not all 0)
- Are growth values present?
- Are there any obvious data issues?

## Step 3: Check Criteria Breakdown

The debug endpoint shows:
- `stocks_meeting_core_criteria`: Stocks meeting basic requirements
- `stocks_meeting_all_criteria`: Stocks meeting all requirements

**If core criteria count is 0:**
- The filtering criteria are too strict for your data
- We need to relax the criteria further

## Step 4: Run Diagnostic Script

In a new terminal:
```powershell
cd C:\Work\Trading\stock_ai\stock_api_service
python check_data.py
```

This will show:
- If stocks are loading
- Sample stocks with their metrics
- How many meet each criterion
- How many meet ALL criteria

## Step 5: Check Server Logs

Look at the terminal where the server is running.

**Look for:**
- `Loading stocks from: [path]`
- `Excel file loaded. Total rows: X, Columns: Y`
- `Successfully loaded X stocks`
- Any error messages

## Common Issues & Solutions

### Issue: No stocks loaded (total_stocks_loaded = 0)

**Possible causes:**
1. Excel file not found
2. Excel file is empty
3. Column names don't match
4. All rows skipped (missing NSE codes)

**Solution:**
- Check Excel file path
- Verify file has data
- Check column names match expected format

### Issue: Stocks loaded but 0 meet criteria

**Possible causes:**
1. Criteria too strict
2. Data values don't meet thresholds
3. Calculated fields causing issues

**Solution:**
- Check sample stocks in debug output
- Compare values to criteria thresholds
- We may need to relax criteria further

### Issue: Quality score calculation errors

**Possible causes:**
1. Division by zero
2. Missing data causing errors
3. Type conversion issues

**Solution:**
- Check server logs for errors
- Look for traceback messages
- Error handling should prevent crashes

## Next Steps Based on Results

### If stocks are loading but 0 meet criteria:
1. Check sample stock values
2. Compare to criteria thresholds
3. We'll relax criteria based on your data

### If no stocks are loading:
1. Check Excel file path
2. Verify file format
3. Check column names

### If there are errors:
1. Share the error message
2. Check server terminal logs
3. We'll fix the specific issue

## Quick Test Commands

```powershell
# Test if stocks load
python check_data.py

# Check debug endpoint
curl http://localhost:8000/api/quality-stocks/debug/info

# Test great quality (should show count > 0 if criteria are met)
curl http://localhost:8000/api/quality-stocks/great
```



