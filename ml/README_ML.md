# ML Stock Movement Prediction (10-day)

The ML module predicts stock **direction over the next 10 days** (up / down / sideways) using past OHLCV and optional technicals (RSI, moving averages). Data is provided by the Flutter app, stored in CSV on Render, and the model **adapts** when prediction accuracy vs actual movement is low.

**Training** uses **all past available candle details**: every stored CSV (per symbol) is loaded in full; for each symbol every valid window is used to build samples (no sampling or mixing across symbols).

**Render / processing delay**: Each response includes `process_time_ms` and the server adds an `X-Process-Time` (seconds) header. Use these to handle cold starts and slow requests (e.g. show a loading state, or retry with backoff if the first request times out).

## Flow

1. **Flutter** sends past candles (and optionally RSI, sma5, sma20, sma50 per candle) to the API.
2. **Storage**: Candles are merged into `data/candles/<symbol>.csv` on the server (Render).
3. **Predict**: `POST /api/ml/predict` returns direction, **confidence**, and **prob_up / prob_down / prob_sideways** for the next 10 days.
4. **Training**: When enough data is stored, `POST /api/ml/train` trains a model on 10-day forward returns. Optional `?auto=1` trains only when insights recommend it (adaptive).
5. **Adaptation**: Resolved predictions (actual vs predicted) feed `GET /api/ml/insights`. When recent accuracy is low, `adaptive_retrain_suggested` is true; calling train then updates the model.

## API (summary)

All ML responses include **process_time_ms** in the body; all responses get an **X-Process-Time** (seconds) header for Render/processing delay.

| Endpoint | Description |
|----------|-------------|
| `GET /api/ml/health` | Check ML module is up; `process_time_ms` in body. |
| `POST /api/ml/predict` | Body: `symbol`, `candles[]` (date, open, high, low, close, volume; optional rsi, sma5, sma20, sma50), `store_for_training`, `forward_days` (default 10). Returns direction, confidence, prob_*, **process_time_ms**. |
| `POST /api/ml/candles` | Body: `symbol`, `candles[]`. Merge into CSV; returns **process_time_ms**. |
| `POST /api/ml/train` | Train from **all** stored candles (every CSV, every valid window per symbol). 10-day labels. Returns **process_time_ms** (training can be slow). `?auto=1`: train only when recommended. |
| `GET /api/ml/insights` | Accuracy, recommend_retrain, adaptive_retrain_suggested; **process_time_ms**. |

## Features used

- Returns (1d, 3d, 5d, 10d, 20d), volume ratio, range, momentum (vs SMA5/20/50), volatility, **RSI** (from Flutter or computed), and extra momentum/volatility. Model expects 16 features (or 12 for older models).

## Confidence and adaptation

- **Confidence** is the model’s max class probability (or rule-based strength). Shown in the predict response.
- **Adaptation**: When actual outcomes are available (after 10 days), predictions are resolved. If recent accuracy drops below 50% and there’s enough data, `adaptive_retrain_suggested` is set; call `POST /api/ml/train?auto=1` (or full train) to update the model.
