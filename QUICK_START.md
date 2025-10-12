# 🚀 Quick Start Guide

## Step-by-Step Setup

### 1️⃣ Start Services (Easy Way)

```bash
./START_DEMO.sh
```

This starts:
- ✅ API Server (port 8000)
- ✅ Log Viewer Server (port 8080)

Then in a **NEW terminal**, start Streamlit:
```bash
streamlit run app.py
```

---

### 2️⃣ Open Browser Tabs

1. **Streamlit UI**: http://localhost:8501
2. **API Docs (Swagger)**: http://localhost:8000/api/docs
3. **Log Viewer**: http://localhost:8080/view_logs.html

---

### 3️⃣ Verify Everything Works

#### Test API:
```bash
curl -X GET http://localhost:8000/api/v1/credentials \
  -H "X-API-Key: admin_key_123"
```

You should see:
- ✅ JSON response with 10+ credentials
- ✅ Log entry appears in **Log Viewer** (refresh if needed)
- ✅ Credentials visible in **Streamlit Dashboard**

---

### 4️⃣ Make a Test Request via Swagger

1. Go to: http://localhost:8000/api/docs
2. Click on **POST /api/v1/credentials**
3. Click "Try it out"
4. In the **X-API-Key** field, enter: `admin_key_123`
5. In the Request body, paste:
```json
{
  "supplier": "DemoSupplier",
  "environment": "production",
  "auth_type": "api_key",
  "data": {
    "api_key": "demo_key_xyz123"
  },
  "allow_self_rotation": false
}
```
6. Click **Execute**

#### What You Should See:

✅ **Swagger Response**: 201 Created with credential details

✅ **Log Viewer** (http://localhost:8080/view_logs.html):
   - Green "➡️ POST /api/v1/credentials" entry
   - Orange "⬅️ POST /api/v1/credentials | Status: 201" entry
   - (Click "🔄 Refresh Now" or enable "Auto-refresh")

✅ **Streamlit Dashboard** (http://localhost:8501):
   - Go to **Dashboard** tab
   - Click "🔄 Refresh Data" button
   - See "DemoSupplier" in the table
   - Expand it in "Credential Actions" section

---

### 5️⃣ Stop All Services

```bash
./STOP_DEMO.sh
```

---

## Troubleshooting

### Issue: "Log Viewer shows nothing"

**Solution 1**: Make sure you're accessing via HTTP, not file://
- ❌ Wrong: `file:///Users/.../view_logs.html`
- ✅ Correct: `http://localhost:8080/view_logs.html`

**Solution 2**: Click "🔄 Refresh Now" button in log viewer

**Solution 3**: Check logs exist:
```bash
cat api_requests.log
```

### Issue: "Streamlit not showing new credentials"

**Solution 1**: Click "🔄 Refresh Data" button in Dashboard tab

**Solution 2**: Check database:
```bash
sqlite3 credentials.db "SELECT id, supplier FROM credentials ORDER BY id DESC LIMIT 5;"
```

**Solution 3**: Refresh the entire Streamlit page (browser refresh)

### Issue: "API Server not responding"

**Check if running:**
```bash
curl http://localhost:8000/
```

**Restart services:**
```bash
./STOP_DEMO.sh
./START_DEMO.sh
```

### Issue: "Port already in use"

**Find and kill the process:**
```bash
# For API (port 8000)
lsof -ti:8000 | xargs kill -9

# For Log Viewer (port 8080)
lsof -ti:8080 | xargs kill -9

# For Streamlit (port 8501)
lsof -ti:8501 | xargs kill -9
```

---

## Checklist for Demo

- [ ] All services running (API, Log Viewer, Streamlit)
- [ ] 3 browser tabs open (Streamlit, Swagger, Log Viewer)
- [ ] Test API request works
- [ ] Logs appear in Log Viewer
- [ ] Credentials show in Streamlit after refresh
- [ ] Database has 10+ sample credentials

---

## Quick Commands

```bash
# Start everything
./START_DEMO.sh
streamlit run app.py  # In new terminal

# Test API
curl http://localhost:8000/api/v1/credentials -H "X-API-Key: admin_key_123"

# View logs (terminal)
tail -f api_requests.log

# Check database
sqlite3 credentials.db "SELECT * FROM credentials LIMIT 5;"

# Stop everything
./STOP_DEMO.sh
```

---

## URLs Reference

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| API Base | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/api/docs |
| Log Viewer | http://localhost:8080/view_logs.html |

---

## API Keys for Testing

| Role | API Key |
|------|---------|
| Admin | `admin_key_123` |
| DevOps | `devops_key_456` |
| CS | `cs_key_789` |
| Partner | `partner_key_012` |

---

Good luck with your demo! 🎉

For more detailed information, see:
- **API_REFERENCE.md** - Complete API documentation
- **DEMO_GUIDE.md** - Detailed demo walkthrough
- **LOG_VIEWER_GUIDE.md** - Log viewer setup guide

