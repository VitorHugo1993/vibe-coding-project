# Deploy API to Render

## Setup Steps:

1. **Create render.yaml:**
   ```yaml
   services:
     - type: web
       name: nezasa-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: DATABASE_URL
           value: postgresql://user:pass@host:5432/db
   ```

2. **Connect GitHub repo to Render**
3. **Deploy automatically**

## Free Tier:
- ✅ 750 hours/month
- ✅ PostgreSQL database included
- ✅ Automatic HTTPS

## Your API will be at:
`https://nezasa-api.onrender.com`
