"""
Feature engineering from OHLCV + optional technicals (RSI, SMA from Flutter).
Input: list of candles (oldest first); optional per-candle: rsi, sma5, sma20, sma50.
Output: flat feature vector for prediction (12 base + 4 extended = 16 when used with new model).
"""
import numpy as np
from typing import List, Dict, Any, Optional

N_FEATURES_LEGACY = 12
N_FEATURES = 16


def _safe_div(a: float, b: float, default: float = 0.0) -> float:
    if b is None or b == 0 or (isinstance(b, float) and np.isnan(b)):
        return default
    return float(a) / float(b)


def _compute_rsi(closes: np.ndarray, period: int = 14) -> float:
    """RSI 0-100 -> normalised 0-1 for features."""
    if len(closes) < period + 1:
        return 0.5
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 1.0 if avg_gain > 0 else 0.5
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return max(0.0, min(1.0, rsi / 100.0))


def build_features_from_candles(
    candles: List[Dict[str, Any]],
    min_candles: int = 21,
) -> Optional[np.ndarray]:
    """
    Build a fixed feature vector from the last min_candles (or more) candles.
    Candles should be ordered oldest first (index 0 = oldest).
    Returns None if not enough data.
    """
    if not candles or len(candles) < min_candles:
        return None

    # Use last min_candles (e.g. 21) for feature computation
    closes = np.array([float(c["close"]) for c in candles[-min_candles:]])
    highs = np.array([float(c["high"]) for c in candles[-min_candles:]])
    lows = np.array([float(c["low"]) for c in candles[-min_candles:]])
    volumes = np.array([float(c.get("volume", 0) or 0) for c in candles[-min_candles:]])

    n = len(closes)
    current_close = closes[-1]

    # Returns (1d, 3d, 5d, 10d)
    ret_1d = _safe_div(closes[-1] - closes[-2], closes[-2]) if n >= 2 else 0.0
    ret_3d = _safe_div(closes[-1] - closes[-4], closes[-4]) if n >= 4 else 0.0
    ret_5d = _safe_div(closes[-1] - closes[-6], closes[-6]) if n >= 6 else 0.0
    ret_10d = _safe_div(closes[-1] - closes[-11], closes[-11]) if n >= 11 else 0.0
    ret_20d = _safe_div(closes[-1] - closes[0], closes[0]) if n >= 20 else 0.0

    # Volume: current / 20d average (avoid zero)
    vol_avg_20 = float(np.mean(volumes)) if n else 1.0
    volume_ratio = _safe_div(volumes[-1], vol_avg_20, 1.0)

    # Range (high-low)/close for last day and 5d avg
    range_1d = _safe_div(highs[-1] - lows[-1], current_close)
    range_5d = (
        np.mean([_safe_div(highs[-i] - lows[-i], closes[-i]) for i in range(1, 6)])
        if n >= 5
        else range_1d
    )

    # Momentum: close vs SMA5, SMA20, SMA50
    sma5 = float(np.mean(closes[-5:])) if n >= 5 else current_close
    sma20 = float(np.mean(closes))
    sma50 = float(np.mean(closes[-50:])) if n >= 50 else sma20
    momentum_5 = _safe_div(current_close - sma5, sma5)
    momentum_20 = _safe_div(current_close - sma20, sma20)
    momentum_50 = _safe_div(current_close - sma50, sma50)

    # Volatility: std of returns over 5d and 20d
    returns = np.diff(closes) / (closes[:-1] + 1e-12)
    vol_5d = float(np.std(returns[-5:])) if len(returns) >= 5 else 0.0
    vol_20d = float(np.std(returns)) if len(returns) >= 2 else 0.0

    # RSI: use last candle's rsi if provided by Flutter, else compute
    last_c = candles[-min_candles:][-1]
    if last_c.get("rsi") is not None and last_c.get("rsi") != "":
        try:
            rsi_raw = float(last_c["rsi"])
            rsi_norm = max(0.0, min(1.0, rsi_raw / 100.0))
        except (TypeError, ValueError):
            rsi_norm = _compute_rsi(closes, 14)
    else:
        rsi_norm = _compute_rsi(closes, 14)

    # 12 base (backward compatible) + 4 extended (RSI, momentum_50, 10d momentum, relative vol)
    momentum_10 = _safe_div(current_close - float(np.mean(closes[-10:])), current_close) if n >= 10 else 0.0
    rel_vol = float(np.std(closes[-5:]) / (current_close + 1e-12)) if n >= 5 else 0.0

    features = np.array(
        [
            ret_1d, ret_3d, ret_5d, ret_10d, ret_20d,
            volume_ratio, range_1d, range_5d,
            momentum_5, momentum_20, vol_5d, vol_20d,
            rsi_norm, momentum_50, momentum_10, rel_vol,
        ],
        dtype=np.float64,
    )
    features = np.nan_to_num(features, nan=0.0, posinf=0.0, neginf=0.0)
    return features
