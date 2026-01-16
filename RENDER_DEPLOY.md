# Deploy to Render - Step by Step Guide

## Prerequisites
- GitHub account
- Your code pushed to GitHub
- Render account (free signup at render.com)

## Step 1: Prepare Your Repository

1. **Ensure your code is on GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/stock-api-service.git
   git push -u origin main
   ```

2. **Verify these files exist:**
   - `requirements.txt`
   - `main.py`
   - `render.yaml` (optional, but helpful)
   - Your Trendlyne data file (or update code to fetch it)

## Step 2: Sign Up on Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email

## Step 3: Create Web Service

1. **Click "New +" → "Web Service"**

2. **Connect Repository:**
   - Click "Connect account" if not connected
   - Select your repository
   - Click "Connect"

3. **Configure Service:**
   - **Name**: `stock-api-service` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `./` if needed)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free**

4. **Advanced Settings (Optional):**
   - **Auto-Deploy**: Yes (deploys on every push)
   - **Health Check Path**: `/health`

5. **Click "Create Web Service"**

## Step 4: Wait for Deployment

- First deployment takes 2-5 minutes
- Watch the logs in real-time
- You'll see build progress

## Step 5: Access Your API

Once deployed, you'll get a URL like:
```
https://stock-api-service.onrender.com
```

Test it:
```bash
curl https://stock-api-service.onrender.com/health
```

## Step 6: Handle Data File

### Option A: Store in Repository (Recommended for small files)

1. Place your Trendlyne file in the `data/` folder
2. Commit and push:
   ```bash
   git add data/trendlyne_data.csv
   git commit -m "Add data file"
   git push
   ```
3. Render will auto-deploy with the new file

### Option B: Download on Startup

Modify `main.py` to download from cloud storage:

```python
import requests
import os

def download_data_file():
    if not os.path.exists("data/trendlyne_data.csv"):
        # Download from URL
        url = os.environ.get("DATA_FILE_URL")
        if url:
            response = requests.get(url)
            os.makedirs("data", exist_ok=True)
            with open("data/trendlyne_data.csv", "wb") as f:
                f.write(response.content)
```

## Step 7: Environment Variables (If Needed)

1. Go to your service on Render
2. Click "Environment"
3. Add variables:
   - `DATA_FILE_URL`: (if using Option B above)
   - Any other config you need

## Step 8: Monitor Your Service

1. **Logs**: Click "Logs" tab to see real-time logs
2. **Metrics**: View CPU, Memory usage
3. **Events**: See deployment history

## Important Notes

### Free Tier Limitations:
- **Sleeps after 15 minutes** of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month free
- Auto-wakes on request

### To Keep Service Awake:
1. Use a cron job service (like cron-job.org)
2. Ping your health endpoint every 10 minutes:
   ```
   https://stock-api-service.onrender.com/health
   ```

### Upgrading (Optional):
- Paid plans start at $7/month
- No sleep on paid plans
- Better performance
- More resources

## Troubleshooting

### Service Won't Start
- Check logs for errors
- Verify `requirements.txt` is correct
- Ensure `main.py` exists
- Check start command is correct

### Data File Not Found
- Verify file is in repository
- Check file path in code
- Look at logs for file path errors

### Slow Response
- Normal for free tier (cold starts)
- First request after sleep is slow
- Consider paid tier for better performance

## Next Steps

1. ✅ Your API is now live!
2. Test all endpoints
3. Share the URL with users
4. Set up monitoring (optional)
5. Consider upgrading if needed

## Example API Calls

```bash
# Health check
curl https://stock-api-service.onrender.com/health

# Get all stocks
curl https://stock-api-service.onrender.com/stocks?limit=10

# Get quality stocks
curl "https://stock-api-service.onrender.com/stocks/quality?limit=20"

# Get stock by symbol
curl https://stock-api-service.onrender.com/stocks/RELIANCE
```

Your API is now accessible from anywhere! 🌍

