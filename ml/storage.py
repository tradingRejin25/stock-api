"""
Store candles (from Flutter app) and prediction outcomes for training and calibration.
- Candles: one CSV per symbol under data/candles/<safe_symbol>.csv (no manual upload).
- Predictions: JSONL log; resolve actual outcome when later candles arrive.
"""
from __future__ import annotations

import csv
import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Base dir: stock_api_service/data (sibling to ml/)
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CANDLES_DIR = _DATA_DIR / "candles"
PREDICTIONS_FILE = _DATA_DIR / "ml_predictions.jsonl"

# Label thresholds (must match train.py)
FORWARD_DAYS = 10  # Default prediction horizon: next 10 days
FORWARD_DAYS_LEGACY = 5  # Resolve old 5-day predictions
UP_THRESHOLD = 0.01
DOWN_THRESHOLD = -0.01

# CSV: base OHLCV + optional technicals from Flutter
BASE_FIELDS = ["date", "open", "high", "low", "close", "volume"]
TECHNICAL_FIELDS = ["rsi", "sma5", "sma20", "sma50"]
CSV_FIELDS = BASE_FIELDS + TECHNICAL_FIELDS


def _safe_symbol(symbol: str) -> str:
    """Filename-safe symbol (e.g. NSE_EQ|INE123 -> NSE_EQ_INE123)."""
    if not symbol or not symbol.strip():
        return "unknown"
    s = re.sub(r"[^\w\-.]", "_", symbol.strip())[:80]
    return s or "unknown"


def _ensure_candles_dir() -> Path:
    CANDLES_DIR.mkdir(parents=True, exist_ok=True)
    return CANDLES_DIR


def _parse_date(d: str) -> Optional[str]:
    """Normalize to YYYY-MM-DD."""
    if not d:
        return None
    d = d.strip()[:10]
    if len(d) == 10 and d[4] == "-" and d[7] == "-":
        return d
    try:
        dt = datetime.fromisoformat(d.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def _row_from_candle(c: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    """Build a CSV row from a candle dict; include optional technicals if present."""
    row = {
        "date": date_str,
        "open": float(c.get("open", 0)),
        "high": float(c.get("high", 0)),
        "low": float(c.get("low", 0)),
        "close": float(c.get("close", 0)),
        "volume": float(c.get("volume", 0) or 0),
    }
    for key in TECHNICAL_FIELDS:
        val = c.get(key)
        if val is not None and val != "":
            try:
                row[key] = float(val)
            except (TypeError, ValueError):
                row[key] = ""
        else:
            row[key] = ""
    return row


def merge_candles_into_csv(symbol: str, candles: List[Dict[str, Any]]) -> int:
    """
    Merge incoming candles into the symbol's CSV (dedupe by date, keep latest).
    Candles may include optional technicals: rsi, sma5, sma20, sma50 (from Flutter).
    Returns number of rows now in the file (after merge).
    """
    _ensure_candles_dir()
    safe = _safe_symbol(symbol or "unknown")
    path = CANDLES_DIR / f"{safe}.csv"
    by_date: Dict[str, Dict[str, Any]] = {}

    if path.exists():
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or BASE_FIELDS)
            for row in reader:
                date_str = _parse_date(row.get("date", ""))
                if date_str:
                    r = {"date": date_str, "open": float(row.get("open", 0)), "high": float(row.get("high", 0)),
                         "low": float(row.get("low", 0)), "close": float(row.get("close", 0)),
                         "volume": float(row.get("volume", 0) or 0)}
                    for k in TECHNICAL_FIELDS:
                        r[k] = row.get(k, "")
                    by_date[date_str] = r

    for c in candles:
        date_str = _parse_date(c.get("date") or c.get("Date", ""))
        if not date_str:
            continue
        try:
            by_date[date_str] = _row_from_candle(c, date_str)
        except (TypeError, ValueError):
            continue

    if not by_date:
        return 0
    rows = sorted(by_date.values(), key=lambda x: x["date"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def log_prediction(
    symbol: str,
    last_candle_date: str,
    direction: str,
    confidence: float,
    method: str,
    forward_days: int = FORWARD_DAYS,
) -> str:
    """Append a prediction record; returns prediction_id. forward_days is the prediction horizon (e.g. 10)."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    pred_id = str(uuid.uuid4())[:8]
    date_norm = _parse_date(last_candle_date) or last_candle_date[:10]
    record = {
        "id": pred_id,
        "symbol": symbol or "unknown",
        "ts": datetime.utcnow().isoformat() + "Z",
        "last_candle_date": date_norm,
        "forward_days": forward_days,
        "direction": direction,
        "confidence": round(confidence, 2),
        "method": method,
        "actual_direction": None,
        "actual_return": None,
        "resolved_at": None,
    }
    with open(PREDICTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return pred_id


def _load_all_predictions() -> List[Dict[str, Any]]:
    if not PREDICTIONS_FILE.exists():
        return []
    out = []
    with open(PREDICTIONS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _candles_by_date(candles: List[Dict[str, Any]]) -> Dict[str, float]:
    out = {}
    for c in candles:
        d = _parse_date(c.get("date") or c.get("Date", ""))
        if d:
            try:
                out[d] = float(c.get("close", 0))
            except (TypeError, ValueError):
                pass
    return out


def resolve_predictions_for_symbol(symbol: str, candles: List[Dict[str, Any]]) -> int:
    """
    Given new candles for a symbol, resolve any pending predictions that now have
    enough forward data (per-record forward_days, or 5 for legacy). Updates records in-place.
    Returns number of predictions resolved.
    """
    by_date = _candles_by_date(candles)
    if not by_date:
        return 0
    dates_sorted = sorted(by_date.keys())
    resolved_count = 0
    all_records = _load_all_predictions()
    for r in all_records:
        if r.get("resolved_at"):
            continue
        if (r.get("symbol") or "").strip() != (symbol or "").strip():
            continue
        last_d = _parse_date(r.get("last_candle_date", ""))
        if not last_d or last_d not in by_date:
            continue
        forward_days = int(r.get("forward_days") or FORWARD_DAYS_LEGACY)
        idx = dates_sorted.index(last_d) if last_d in dates_sorted else -1
        if idx < 0 or idx + forward_days >= len(dates_sorted):
            continue
        close_t = by_date[last_d]
        forward_date = dates_sorted[idx + forward_days]
        close_fwd = by_date[forward_date]
        ret = (close_fwd - close_t) / (close_t + 1e-12)
        if ret > UP_THRESHOLD:
            actual = "up"
        elif ret < DOWN_THRESHOLD:
            actual = "down"
        else:
            actual = "sideways"
        r["actual_direction"] = actual
        r["actual_return"] = round(ret, 4)
        r["resolved_at"] = datetime.utcnow().isoformat() + "Z"
        resolved_count += 1

    if resolved_count > 0:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(PREDICTIONS_FILE, "w", encoding="utf-8") as f:
            for r in all_records:
                f.write(json.dumps(r) + "\n")
    return resolved_count


def get_candles_for_symbol(symbol: str) -> List[Dict[str, Any]]:
    """Load all stored candles for a symbol (for resolution and training); includes optional technicals."""
    safe = _safe_symbol(symbol or "unknown")
    path = CANDLES_DIR / f"{safe}.csv"
    if not path.exists():
        return []
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            date_str = _parse_date(row.get("date", ""))
            if not date_str:
                continue
            try:
                c = {
                    "date": date_str,
                    "open": float(row.get("open", 0)),
                    "high": float(row.get("high", 0)),
                    "low": float(row.get("low", 0)),
                    "close": float(row.get("close", 0)),
                    "volume": float(row.get("volume", 0) or 0),
                }
                for k in TECHNICAL_FIELDS:
                    v = row.get(k, "")
                    if v != "":
                        try:
                            c[k] = float(v)
                        except (TypeError, ValueError):
                            pass
                out.append(c)
            except (TypeError, ValueError):
                continue
    return sorted(out, key=lambda x: x["date"])


def get_stored_candle_paths() -> List[Path]:
    """All CSV paths in data/candles/ for training."""
    _ensure_candles_dir()
    return sorted(CANDLES_DIR.glob("*.csv"))


def get_insights() -> Dict[str, Any]:
    """
    Aggregate insights: overall accuracy, per-symbol accuracy, recent performance,
    and recommendation to retrain.
    """
    preds = _load_all_predictions()
    resolved = [p for p in preds if p.get("resolved_at") and p.get("actual_direction") is not None]
    total = len(resolved)
    correct = sum(1 for p in resolved if p.get("direction") == p.get("actual_direction"))
    overall_accuracy = (correct / total) if total else None

    by_symbol: Dict[str, Dict[str, Any]] = {}
    for p in resolved:
        sym = p.get("symbol") or "unknown"
        if sym not in by_symbol:
            by_symbol[sym] = {"total": 0, "correct": 0, "directions": {}}
        by_symbol[sym]["total"] += 1
        if p.get("direction") == p.get("actual_direction"):
            by_symbol[sym]["correct"] += 1
        actual = p.get("actual_direction") or "?"
        by_symbol[sym]["directions"][actual] = by_symbol[sym]["directions"].get(actual, 0) + 1

    symbol_accuracy = {
        sym: (d["correct"] / d["total"]) if d["total"] else None
        for sym, d in by_symbol.items()
    }
    symbol_accuracy = {k: round(v, 3) for k, v in symbol_accuracy.items() if v is not None}

    # Recent: last 30 resolved
    recent = sorted(resolved, key=lambda x: x.get("resolved_at") or "")[-30:]
    recent_correct = sum(1 for p in recent if p.get("direction") == p.get("actual_direction"))
    recent_accuracy = (recent_correct / len(recent)) if recent else None

    stored_paths = get_stored_candle_paths()
    total_rows = 0
    for p in stored_paths:
        with open(p, newline="", encoding="utf-8") as f:
            total_rows += sum(1 for _ in csv.DictReader(f))
    recommend_retrain = len(stored_paths) >= 1 and total_rows >= 300 and total >= 20
    # Suggest retrain when recent accuracy is low (model adapts to actual outcomes)
    adaptive_retrain_suggested = (
        recent_accuracy is not None
        and recent_accuracy < 0.50
        and total >= 15
        and len(stored_paths) >= 1
        and total_rows >= 100
    )

    return {
        "predictions_resolved": total,
        "overall_accuracy": round(overall_accuracy, 3) if overall_accuracy is not None else None,
        "recent_accuracy": round(recent_accuracy, 3) if recent_accuracy is not None else None,
        "by_symbol": {
            "accuracy": symbol_accuracy,
            "counts": {sym: d["total"] for sym, d in by_symbol.items()},
        },
        "stored_symbols": len(stored_paths),
        "stored_candle_rows": total_rows,
        "recommend_retrain": recommend_retrain,
        "adaptive_retrain_suggested": adaptive_retrain_suggested,
    }
