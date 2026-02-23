"""
API routes for ML stock movement prediction.
- Predict: 10-day horizon; optional technicals (RSI, SMA); store_for_training for calibration.
- Candles: accept OHLCV + optional rsi, sma5, sma20, sma50 from Flutter; stored in Render CSV.
- Train: train from stored candles (all past available); model adapts when accuracy is low.
- Insights: accuracy, confidence, adaptive_retrain_suggested.
- All responses include process_time_ms for Render/processing delay handling.
"""
import time
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from ml.predictor import StockMovementPredictor
from ml import storage

router = APIRouter(prefix="/api/ml", tags=["ML Prediction"])

predictor = StockMovementPredictor(use_demo_model=True)


@router.get("/health")
async def ml_health():
    """ML module health: confirms ML routes are deployed and model is loadable."""
    t0 = time.perf_counter()
    try:
        has_model = predictor._model is not None
        out = {"status": "ok", "model_loaded": has_model, "message": "ML module is deployed."}
    except Exception as e:
        out = {"status": "error", "model_loaded": False, "message": str(e)}
    out["process_time_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    return out


class CandleItem(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    rsi: Optional[float] = None
    sma5: Optional[float] = None
    sma20: Optional[float] = None
    sma50: Optional[float] = None


class PredictRequest(BaseModel):
    symbol: Optional[str] = None
    candles: List[CandleItem]
    store_for_training: bool = False
    forward_days: int = 10


class PredictResponse(BaseModel):
    direction: str
    confidence: float
    method: str
    forward_days: int = 10
    prob_up: float = 0.0
    prob_down: float = 0.0
    prob_sideways: float = 0.0
    process_time_ms: Optional[float] = None


@router.post("/predict", response_model=PredictResponse)
async def predict_movement(request: PredictRequest):
    """
    Predict stock movement for the next forward_days (default 10) using OHLCV + optional RSI, MAs.
    Send at least 21 daily candles (oldest first). Optional: rsi, sma5, sma20, sma50 per candle.
    If store_for_training=true, candles are saved and prediction logged for adaptive learning.
    Response includes process_time_ms for Render/processing delay (e.g. cold start).
    """
    t0 = time.perf_counter()
    if not request.candles or len(request.candles) < 21:
        raise HTTPException(
            status_code=400,
            detail="At least 21 candles required (oldest first). Use 60–252 for better results.",
        )
    candles = [c.model_dump() for c in request.candles]
    result = predictor.predict(candles, min_candles=21, forward_days=request.forward_days)

    symbol = (request.symbol or "").strip() or "unknown"
    if request.store_for_training:
        storage.merge_candles_into_csv(symbol, candles)
        last_date = candles[-1].get("date", "") if candles else ""
        storage.log_prediction(
            symbol=symbol,
            last_candle_date=last_date,
            direction=result["direction"],
            confidence=result["confidence"],
            method=result["method"],
            forward_days=request.forward_days,
        )
        full_candles = storage.get_candles_for_symbol(symbol)
        if full_candles:
            storage.resolve_predictions_for_symbol(symbol, full_candles)

    process_time_ms = round((time.perf_counter() - t0) * 1000, 1)
    return PredictResponse(
        direction=result["direction"],
        confidence=result["confidence"],
        method=result["method"],
        forward_days=result.get("forward_days", 10),
        prob_up=result.get("prob_up", 0),
        prob_down=result.get("prob_down", 0),
        prob_sideways=result.get("prob_sideways", 0),
        process_time_ms=process_time_ms,
    )


class StoreCandlesRequest(BaseModel):
    symbol: str
    candles: List[CandleItem]


@router.post("/candles")
async def store_candles(request: StoreCandlesRequest):
    """
    Store OHLCV candles for a symbol (e.g. 1-year data from the app).
    Merges with any existing data. Resolves pending predictions when new candles allow.
    Response includes process_time_ms (Render/processing delay).
    """
    t0 = time.perf_counter()
    if not request.symbol or not request.candles:
        raise HTTPException(status_code=400, detail="symbol and candles required.")
    candles = [c.model_dump() for c in request.candles]
    count = storage.merge_candles_into_csv(request.symbol.strip(), candles)
    full_candles = storage.get_candles_for_symbol(request.symbol.strip())
    resolved = storage.resolve_predictions_for_symbol(request.symbol.strip(), full_candles) if full_candles else 0
    return {
        "stored_rows": count,
        "predictions_resolved": resolved,
        "message": "Candles merged for training. Use POST /api/ml/train when ready.",
        "process_time_ms": round((time.perf_counter() - t0) * 1000, 1),
    }


@router.post("/train")
async def train_from_stored(
    auto: bool = Query(False, description="If true, train only when insights recommend (adaptive)."),
):
    """
    Train from all past available candle data (every stored CSV, every valid window per symbol).
    Uses 10-day forward labels. If auto=true, trains only when recommend_retrain or
    adaptive_retrain_suggested. Response includes process_time_ms (training can be slow on Render).
    """
    t0 = time.perf_counter()
    if auto:
        insights = storage.get_insights()
        if not insights.get("recommend_retrain") and not insights.get("adaptive_retrain_suggested"):
            return {
                "ok": False,
                "skipped": True,
                "message": "Retrain not recommended. Send more data or check GET /api/ml/insights.",
                "insights": insights,
                "process_time_ms": round((time.perf_counter() - t0) * 1000, 1),
            }
    try:
        from ml.train import train_from_stored as do_train
        metrics = do_train()
        predictor.reload_model()
        return {
            "ok": True,
            "message": "Model trained from all stored candles (10-day horizon) and reloaded.",
            "metrics": metrics,
            "process_time_ms": round((time.perf_counter() - t0) * 1000, 1),
        }
    except ValueError as e:
        # No stored data or not enough data: return 200 so client can show message, not a generic error
        return {
            "ok": False,
            "message": str(e),
            "detail": "Send candles via POST /api/ml/candles or predict with store_for_training=true, then train again.",
            "process_time_ms": round((time.perf_counter() - t0) * 1000, 1),
        }


@router.get("/insights")
async def get_insights():
    """
    Aggregate insights: overall/recent accuracy, per-symbol stats, recommend_retrain,
    adaptive_retrain_suggested. Includes process_time_ms for delay handling.
    """
    t0 = time.perf_counter()
    out = storage.get_insights()
    out["process_time_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    return out
