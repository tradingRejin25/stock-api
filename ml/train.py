"""
Train the stock movement model on OHLCV data and save it for the predictor.

Usage:
  # From project root (stock_ai) or from stock_api_service:
  python -m stock_api_service.ml.train --csv path/to/candles.csv [--csv path/to/another.csv ...] --out ml/model.joblib
  # Or from stock_api_service directory:
  python -m ml.train --csv candles.csv --out ml/model.joblib

CSV format: date,open,high,low,close,volume  (header required). Optional column: symbol.
Multiple --csv files are merged (e.g. one CSV per symbol for multi-symbol training).

Labels: forward 5-day return -> up (ret > 0.01), down (ret < -0.01), sideways.
Train/validation: time-based split (last 20% of dates as test).
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import numpy as np


def _candle_row(row: Dict[str, str]) -> Dict[str, Any]:
    out = {
        "date": row["date"].strip(),
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": float(row.get("volume", 0) or 0),
    }
    for k in ("rsi", "sma5", "sma20", "sma50"):
        v = row.get(k, "")
        if v != "":
            try:
                out[k] = float(v)
            except (TypeError, ValueError):
                pass
    return out


def load_candles_from_csv(path: Path) -> List[Dict[str, Any]]:
    """Load candles from CSV: date, open, high, low, close, volume; optional: rsi, sma5, sma20, sma50."""
    candles = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "date" not in reader.fieldnames or "close" not in reader.fieldnames:
            raise ValueError(f"CSV must have header: date, open, high, low, close, volume. Got: {reader.fieldnames}")
        for row in reader:
            try:
                candles.append(_candle_row(row))
            except (KeyError, ValueError) as e:
                raise ValueError(f"Invalid row in {path}: {row}") from e
    return candles


def build_labels_and_features(
    candles: List[Dict[str, Any]],
    forward_days: int = 10,
    up_threshold: float = 0.01,
    down_threshold: float = -0.01,
    min_candles: int = 21,
):
    """
    For each date t where we have enough history and future, compute:
    - label: 0=up, 1=down, 2=sideways (based on forward_days return from t)
    - features: from build_features_from_candles using candles up to t
    """
    from .features import build_features_from_candles

    X_list = []
    y_list = []
    n = len(candles)
    for i in range(min_candles, n - forward_days):
        window = candles[: i + 1]
        features = build_features_from_candles(window, min_candles=min_candles)
        if features is None:
            continue
        close_t = candles[i]["close"]
        close_fwd = candles[i + forward_days]["close"]
        ret = (close_fwd - close_t) / (close_t + 1e-12)
        if ret > up_threshold:
            label = 0  # up
        elif ret < down_threshold:
            label = 1  # down
        else:
            label = 2  # sideways
        X_list.append(features)
        y_list.append(label)
    if not X_list:
        return None, None
    return np.stack(X_list), np.array(y_list)


def time_based_split(
    X: np.ndarray, y: np.ndarray, test_frac: float = 0.2
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split by last test_frac of samples (time order)."""
    n = len(X)
    split = int(n * (1 - test_frac))
    return X[:split], X[split:], y[:split], y[split:]


def train_and_save(
    csv_paths: List[Path],
    out_path: Path,
    test_frac: float = 0.2,
    forward_days: int = 10,
    up_threshold: float = 0.01,
    down_threshold: float = -0.01,
    min_candles: int = 21,
    n_estimators: int = 50,
    max_depth: int = 6,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Train on all past available candle data: every stored CSV (symbol) is loaded
    in full; for each symbol we build samples from every valid window (no sampling).
    Symbols are kept separate so time series are not mixed.
    """
    from sklearn.ensemble import RandomForestClassifier
    import joblib

    X_list: List[np.ndarray] = []
    y_list: List[np.ndarray] = []
    for p in csv_paths:
        candles = load_candles_from_csv(p)
        candles.sort(key=lambda c: c["date"])
        if len(candles) < min_candles + forward_days:
            continue
        X_sym, y_sym = build_labels_and_features(
            candles,
            forward_days=forward_days,
            up_threshold=up_threshold,
            down_threshold=down_threshold,
            min_candles=min_candles,
        )
        if X_sym is not None and len(X_sym) > 0:
            X_list.append(X_sym)
            y_list.append(y_sym)

    if not X_list:
        raise ValueError(
            "No samples from any CSV. Need at least min_candles + forward_days rows per symbol."
        )

    X = np.vstack(X_list)
    y = np.concatenate(y_list)

    X_train, X_test, y_train, y_test = time_based_split(X, y, test_frac=test_frac)

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
    )
    model.fit(X_train, y_train)

    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)

    return {
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "total_samples": len(X),
        "symbols_used": len(X_list),
        "train_accuracy": round(train_acc, 3),
        "test_accuracy": round(test_acc, 3),
        "model_path": str(out_path.absolute()),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Train stock movement model from OHLCV CSV(s) and save joblib."
    )
    parser.add_argument(
        "--from-stored",
        action="store_true",
        help="Use all CSVs in data/candles/ (from app-sent data) instead of --csv.",
    )
    parser.add_argument(
        "--csv",
        action="append",
        dest="csv_paths",
        help="Path to CSV (date,open,high,low,close,volume). Can be repeated. Not used if --from-stored.",
    )
    parser.add_argument(
        "--out",
        default="ml/model.joblib",
        help="Output path for joblib model (default: ml/model.joblib)",
    )
    parser.add_argument("--test-frac", type=float, default=0.2, help="Fraction for time-based test set")
    parser.add_argument("--forward-days", type=int, default=10, help="Forward return window for labels (default 10)")
    parser.add_argument("--up", type=float, default=0.01, help="Return threshold for 'up' label")
    parser.add_argument("--down", type=float, default=-0.01, help="Return threshold for 'down' label")
    parser.add_argument("--min-candles", type=int, default=21, help="Min candles for feature window")
    parser.add_argument("--n-estimators", type=int, default=50, help="RandomForest n_estimators")
    parser.add_argument("--max-depth", type=int, default=6, help="RandomForest max_depth")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.from_stored:
        try:
            metrics = train_from_stored(
                out_path=Path(args.out),
                test_frac=args.test_frac,
                forward_days=args.forward_days,
                up_threshold=args.up,
                down_threshold=args.down,
                min_candles=args.min_candles,
                n_estimators=args.n_estimators,
                max_depth=args.max_depth,
                random_state=args.seed,
            )
            print("Train from stored:", metrics)
        except ValueError as e:
            raise SystemExit(str(e))
        return

    if not args.csv_paths:
        raise SystemExit("Provide --csv path(s) or --from-stored.")
    paths = [Path(p) for p in args.csv_paths]
    for p in paths:
        if not p.exists():
            raise SystemExit(f"File not found: {p}")
    try:
        metrics = train_and_save(
            csv_paths=paths,
            out_path=Path(args.out),
            test_frac=args.test_frac,
            forward_days=args.forward_days,
            up_threshold=args.up,
            down_threshold=args.down,
            min_candles=args.min_candles,
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=args.seed,
        )
        print(f"Train samples: {metrics['train_samples']}, test: {metrics['test_samples']}; "
              f"train acc: {metrics['train_accuracy']}, test acc: {metrics['test_accuracy']}; "
              f"saved to {metrics['model_path']}")
    except ValueError as e:
        raise SystemExit(str(e))


def train_from_stored(
    out_path: Optional[Path] = None,
    test_frac: float = 0.2,
    forward_days: int = 10,
    up_threshold: float = 0.01,
    down_threshold: float = -0.01,
    min_candles: int = 21,
    n_estimators: int = 50,
    max_depth: int = 6,
    random_state: int = 42,
) -> Dict[str, Any]:
    """Train from all CSVs in data/candles/ (created from app-sent data). Returns metrics."""
    from .storage import get_stored_candle_paths

    paths = get_stored_candle_paths()
    if not paths:
        raise ValueError("No stored candle CSVs found. Send candles from the app (store_for_training or POST /api/ml/candles) first.")
    default_out = Path(__file__).resolve().parent / "model.joblib"
    return train_and_save(
        csv_paths=paths,
        out_path=out_path or default_out,
        test_frac=test_frac,
        forward_days=forward_days,
        up_threshold=up_threshold,
        down_threshold=down_threshold,
        min_candles=min_candles,
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
    )


if __name__ == "__main__":
    main()
