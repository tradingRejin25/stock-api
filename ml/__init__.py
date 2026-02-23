"""
Minimal ML module for stock movement prediction.
Uses 1-year (or shorter) OHLCV data to predict short-term direction.
See docs/ML_STOCK_PREDICTION.md for approach and extensions.
"""
from .features import build_features_from_candles
from .predictor import StockMovementPredictor

__all__ = ["build_features_from_candles", "StockMovementPredictor"]
