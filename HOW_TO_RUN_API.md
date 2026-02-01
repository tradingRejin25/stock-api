# How to Run the Stock API Service

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Dependencies installed** - Run the following command if you haven't already:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

### Method 1: Using the Batch File (Windows - Easiest)

Simply double-click `run_api.bat` or run it from command prompt:
```bash
run_api.bat
```

### Method 2: Using Python Directly

```bash
python main.py
```

### Method 3: Using Uvicorn Command

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

## Accessing the API

Once the server is running, you can access:

- **API Root**: http://localhost:8000/
- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Trendlyne Stocks API Endpoints

### Get All Stocks
```
GET http://localhost:8000/api/trendlyne-stocks
```

### Get Stock by NSE Code
```
GET http://localhost:8000/api/trendlyne-stocks?nseCode=VENUSREM
```

### Get Stock by BSE Code
```
GET http://localhost:8000/api/trendlyne-stocks?bseCode=526953
```

### Get Stock by ISIN
```
GET http://localhost:8000/api/trendlyne-stocks?isin=INE411B01019
```

### Search Stocks by Name
```
GET http://localhost:8000/api/trendlyne-stocks?search=Venus
```

### Get Stock by Identifier (Path Parameter)
```
GET http://localhost:8000/api/trendlyne-stocks/VENUSREM
```

### Refresh Stock Data (Reload CSV Files)
```
POST http://localhost:8000/api/trendlyne-stocks/refresh
```

### Get Statistics
```
GET http://localhost:8000/api/trendlyne-stocks/statistics
```

## Example Usage

### Using curl (Command Line)

```bash
# Get all stocks
curl http://localhost:8000/api/trendlyne-stocks

# Get stock by NSE code
curl http://localhost:8000/api/trendlyne-stocks?nseCode=VENUSREM

# Search stocks
curl http://localhost:8000/api/trendlyne-stocks?search=Venus

# Refresh data
curl -X POST http://localhost:8000/api/trendlyne-stocks/refresh

# Get statistics
curl http://localhost:8000/api/trendlyne-stocks/statistics
```

### Using Python requests

```python
import requests

# Get all stocks
response = requests.get("http://localhost:8000/api/trendlyne-stocks")
stocks = response.json()
print(f"Total stocks: {stocks['count']}")

# Get specific stock
response = requests.get("http://localhost:8000/api/trendlyne-stocks?nseCode=VENUSREM")
stock = response.json()
print(stock)

# Refresh data
response = requests.post("http://localhost:8000/api/trendlyne-stocks/refresh")
print(response.json())
```

### Using Browser

Simply open:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/api/trendlyne-stocks - View all stocks (JSON)
- http://localhost:8000/api/trendlyne-stocks?nseCode=VENUSREM - View specific stock

## Adding New CSV Files

When you add new CSV files with the pattern `trendlyne-filtered (N).csv` to the `data` folder:

1. **Automatic**: The service will detect new files on the next request (if not already loaded)
2. **Manual Refresh**: Call the refresh endpoint to force reload:
   ```
   POST http://localhost:8000/api/trendlyne-stocks/refresh
   ```
3. **Restart Service**: Restart the API server to reload all files

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, you can change it in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to different port
```

Or use uvicorn command with different port:
```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Module Not Found Errors

Make sure you're in the project root directory and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### CSV Files Not Found

Ensure your CSV files are in the `data` folder with the naming pattern:
- `trendlyne-filtered (1).csv`
- `trendlyne-filtered (2).csv`
- etc.

## Stopping the Server

Press `CTRL+C` in the terminal/command prompt where the server is running.









