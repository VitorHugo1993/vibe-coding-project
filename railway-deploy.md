# Deploy API to Railway

## Quick Setup (5 minutes):

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Deploy your API:**
   ```bash
   railway init
   railway up
   ```

4. **Get your public URL:**
   ```bash
   railway domain
   ```

## What Railway Does:
- ✅ Automatically detects Python/FastAPI
- ✅ Installs dependencies from requirements.txt
- ✅ Provides public HTTPS URL
- ✅ Handles database (PostgreSQL)
- ✅ Free tier: 500 hours/month

## Your API will be available at:
`https://your-app-name.railway.app`

## Update Streamlit Config:
Change in app.py:
```python
API_BASE_URL = "https://your-app-name.railway.app"
```
