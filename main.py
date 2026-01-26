"""
Main FastAPI application for Stock API Service
Includes Nifty Stocks API endpoints
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nifty_stocks_routes import router as nifty_stocks_router

app = FastAPI(
    title="Stock API Service",
    description="API service for stock information and Nifty stocks",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Nifty stocks routes
app.include_router(nifty_stocks_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Stock API Service",
        "version": "1.0.0",
        "endpoints": {
            "nifty_stocks": "/api/nifty-stocks",
            "nifty_stocks_by_nse": "/api/nifty-stocks?nseCode=RELIANCE",
            "nifty_stocks_by_isin": "/api/nifty-stocks?isin=INE467B01029",
            "nifty_stocks_search": "/api/nifty-stocks?search=Reliance",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "stock-api-service"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Stock API Service...")
    print("📋 Nifty Stocks API available at: http://localhost:8000/api/nifty-stocks")
    print("📚 API Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

