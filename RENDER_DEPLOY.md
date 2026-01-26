# Render Deployment Guide

## Issue: Python 3.13.4 Build Errors

The error you're seeing is because Python 3.13.4 is too new and some packages don't have pre-built wheels yet. The `uvicorn[standard]` package requires Rust compilation which is failing.

## Solution

### Step 1: Update Render Settings

In your Render dashboard, go to your service settings and:

1. **Set Python Version**: Change from `3.13.4` to `3.11.7`
   - Go to: Settings → Environment → Python Version
   - Select: `3.11.7`

2. **Update Build Command**:
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```

3. **Update Start Command**:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### Step 2: Files Already Updated

The following files have been updated:
- ✅ `requirements.txt` - Removed `[standard]` extras to avoid Rust compilation
- ✅ `runtime.txt` - Specifies Python 3.11.7
- ✅ `.python-version` - Specifies Python 3.11.7

### Step 3: Commit and Push

```bash
cd ../stock_api_service
git add requirements.txt runtime.txt .python-version
git commit -m "Fix Render deployment: Use Python 3.11.7 and simplify dependencies"
git push
```

### Step 4: Manual Render Configuration (Alternative)

If the render.yaml doesn't work, manually configure in Render dashboard:

1. **Environment**: Python 3
2. **Python Version**: `3.11.7` (specify in runtime.txt or environment settings)
3. **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Why This Fixes It

1. **Python 3.11.7** has better package support and pre-built wheels
2. **Removed `[standard]` extras** from uvicorn avoids Rust compilation
3. **Upgraded pip** ensures latest package resolution

## Alternative: Use Simpler Requirements

If issues persist, you can use even simpler versions:

```txt
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
```

This allows pip to choose compatible versions automatically.

