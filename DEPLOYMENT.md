# Deployment Guide - Free Hosting Platforms

This guide covers deploying the Stock API Service to free hosting platforms.

## Recommended Free Platforms

### 1. **Render** (Recommended - Easiest)
- ✅ Free tier: 750 hours/month
- ✅ Automatic HTTPS
- ✅ Easy deployment from GitHub
- ✅ Auto-deploy on push
- ✅ Persistent storage

### 2. **Railway**
- ✅ Free tier: $5 credit/month
- ✅ Easy deployment
- ✅ Good performance

### 3. **Fly.io**
- ✅ Free tier: 3 shared VMs
- ✅ Global edge network
- ✅ Good for low traffic

### 4. **PythonAnywhere**
- ✅ Free tier available
- ✅ Simple setup
- ⚠️ Limited to 1 web app

## Quick Start: Render (Recommended)

### Step 1: Prepare Your Code

1. Make sure your code is in a Git repository (GitHub, GitLab, or Bitbucket)

2. Create a `render.yaml` file (already created in this project)

3. Ensure `requirements.txt` is up to date

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)

2. Click "New +" → "Web Service"

3. Connect your GitHub repository

4. Configure:
   - **Name**: `stock-api-service` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. Add Environment Variables (if needed):
   - `PORT`: (auto-set by Render)

6. Click "Create Web Service"

7. Wait for deployment (2-5 minutes)

8. Your API will be available at: `https://your-app-name.onrender.com`

### Step 3: Upload Your Data File

Since Render doesn't have persistent storage by default, you have options:

**Option A: Use GitHub (Recommended)**
- Place your Trendlyne data file in the repository
- Update `data_loader.py` to look for it in the repo

**Option B: Use External Storage**
- Upload to Google Drive/Dropbox and download on startup
- Use a cloud storage service

**Option C: Use Render Disk (Paid)**
- Upgrade to paid plan for persistent storage

## Alternative: Railway

### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
```

### Step 2: Login
```bash
railway login
```

### Step 3: Initialize Project
```bash
railway init
```

### Step 4: Deploy
```bash
railway up
```

Your app will be deployed and you'll get a URL.

## Alternative: Fly.io

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Login
```bash
fly auth login
```

### Step 3: Launch App
```bash
fly launch
```

Follow the prompts. Your app will be deployed.

## Production Considerations

### 1. Environment Variables
Create a `.env` file for local development (don't commit it):
```
PORT=8000
```

### 2. CORS Configuration
The current CORS allows all origins. For production, consider restricting:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Data File Management
- Store data file in repository (for small files)
- Use cloud storage for large files
- Consider database for production

### 4. Error Handling
Already implemented, but monitor logs in production.

### 5. Rate Limiting
Consider adding rate limiting for production:
```bash
pip install slowapi
```

## Monitoring

### Render
- Built-in logs dashboard
- Metrics available in dashboard

### Railway
- Logs in dashboard
- Metrics available

### Fly.io
```bash
fly logs
```

## Troubleshooting

### Common Issues

1. **App crashes on startup**
   - Check logs for errors
   - Verify all dependencies in `requirements.txt`
   - Check if data file is accessible

2. **Port binding error**
   - Use `$PORT` environment variable (Render)
   - Use `0.0.0.0` as host

3. **Data file not found**
   - Ensure file is in repository
   - Check file path in code
   - Verify file permissions

4. **Slow startup**
   - Normal for free tiers (cold starts)
   - Consider paid tier for better performance

## Cost Comparison

| Platform | Free Tier | Limitations |
|----------|-----------|-------------|
| Render | 750 hrs/month | Sleeps after 15 min inactivity |
| Railway | $5 credit/month | ~500 hours |
| Fly.io | 3 shared VMs | Limited resources |
| PythonAnywhere | Always-on | 1 web app only |

## Next Steps

1. Choose a platform (Render recommended)
2. Follow platform-specific guide below
3. Deploy your application
4. Test the API endpoints
5. Share the URL with your users

