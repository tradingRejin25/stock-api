"""
Stock movement predictor: uses features from OHLCV to predict next direction.
Loads a saved model from ml/model.joblib if present; otherwise uses a small demo
model (synthetic data) or rule-based fallback.
"""
import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .features import build_features_from_candles

# Lazy load: saved model first, then demo model
_classifier = None


def _default_model_path() -> Path:
    """Path to model.joblib next to this file (stock_api_service/ml/model.joblib)."""
    return Path(__file__).resolve().parent / "model.joblib"


def _get_saved_model(path: Optional[Path] = None) -> Optional[Any]:
    """Load classifier from joblib if file exists."""
    p = path or _default_model_path()
    if not p.is_file():
        return None
    try:
        import joblib
        return joblib.load(p)
    except Exception:
        return None


def _get_demo_model():
    """Build a small Random Forest trained on synthetic data (demo only)."""
    global _classifier
    if _classifier is not None:
        return _classifier
    try:
        from sklearn.ensemble import RandomForestClassifier

        np.random.seed(42)
        n_samples = 500
        n_features = 12
        X = np.random.randn(n_samples, n_features).astype(np.float64) * 0.1
        # Synthetic target: "up" if sum of last 3 features > 0, else "down" or "sideways"
        raw = X[:, -3:].sum(axis=1)
        y = np.where(raw > 0.02, 0, np.where(raw < -0.02, 1, 2))  # 0=up, 1=down, 2=sideways
        _classifier = RandomForestClassifier(n_estimators=20, max_depth=4, random_state=42)
        _classifier.fit(X, y)
        return _classifier
    except Exception:
        return None


def _rule_based_direction(candles: List[Dict[str, Any]], forward_days: int = 10) -> Tuple[str, float, Dict[str, float]]:
    """Fallback: use forward_days return for direction and simple confidence; return class probs."""
    need = forward_days + 1
    if not candles or len(candles) < need:
        return "sideways", 0.5, {"up": 1/3, "down": 1/3, "sideways": 1/3}
    c = [float(x["close"]) for x in candles]
    ret = (c[-1] - c[-need]) / (c[-need] + 1e-12)
    conf = min(0.9, 0.5 + abs(ret) * 10)
    if ret > 0.01:
        return "up", conf, {"up": conf, "down": (1 - conf) / 2, "sideways": (1 - conf) / 2}
    if ret < -0.01:
        return "down", conf, {"up": (1 - conf) / 2, "down": conf, "sideways": (1 - conf) / 2}
    return "sideways", 0.5, {"up": 1/3, "down": 1/3, "sideways": 1/3}


class StockMovementPredictor:
    """Predict short-term stock direction from a list of OHLCV candles (oldest first)."""

    def __init__(self, use_demo_model: bool = True, model_path: Optional[os.PathLike] = None):
        self.use_demo_model = use_demo_model
        self._model_path = Path(model_path) if model_path else _default_model_path()
        # Prefer saved model, then demo if allowed
        self._model = _get_saved_model(self._model_path)
        if self._model is None and use_demo_model:
            self._model = _get_demo_model()

    def reload_model(self) -> bool:
        """Reload model from disk (e.g. after training). Returns True if a model was loaded."""
        self._model = _get_saved_model(self._model_path)
        if self._model is None and self.use_demo_model:
            self._model = _get_demo_model()
        return self._model is not None

    def predict(
        self,
        candles: List[Dict[str, Any]],
        min_candles: int = 21,
        forward_days: int = 10,
    ) -> Dict[str, Any]:
        """
        Predict direction over the next forward_days (default 10). Returns:
          - direction: "up" | "down" | "sideways"
          - confidence: float in [0, 1]
          - method: "model" | "rule"
          - prob_up, prob_down, prob_sideways: class probabilities
        """
        features = build_features_from_candles(candles, min_candles=min_candles)
        if features is not None and self._model is not None:
            try:
                # Use model's expected feature count (sklearn sets n_features_in_)
                n = getattr(self._model, "n_features_in_", None)
                if n is not None and len(features) > n:
                    features = features[:n]
                elif n is not None and len(features) < n:
                    pass  # will likely fail in predict; fall back to rule
                X = features.reshape(1, -1)
                pred = self._model.predict(X)[0]
                proba = self._model.predict_proba(X)[0]
                dir_map = {0: "up", 1: "down", 2: "sideways"}
                direction = dir_map.get(int(pred), "sideways")
                confidence = float(np.max(proba))
                probs = {"up": proba[0], "down": proba[1], "sideways": proba[2]}
                if len(proba) == 2:
                    probs = {"up": proba[0], "down": proba[1], "sideways": 0.0}
                return {
                    "direction": direction,
                    "confidence": round(confidence, 2),
                    "method": "model",
                    "forward_days": forward_days,
                    "prob_up": round(probs["up"], 3),
                    "prob_down": round(probs["down"], 3),
                    "prob_sideways": round(probs["sideways"], 3),
                }
            except Exception:
                pass
        direction, confidence, probs = _rule_based_direction(candles, forward_days=forward_days)
        return {
            "direction": direction,
            "confidence": round(confidence, 2),
            "method": "rule",
            "forward_days": forward_days,
            "prob_up": round(probs["up"], 3),
            "prob_down": round(probs["down"], 3),
            "prob_sideways": round(probs["sideways"], 3),
        }
