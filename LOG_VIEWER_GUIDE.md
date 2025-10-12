# 📊 API Log Viewer Guide

## Quick Start

### Step 1: Start the Log Viewer Server

```bash
python3 serve_logs.py
```

This will start a server on port 8080.

### Step 2: Open in Browser

The browser should open automatically, or go to:
```
http://localhost:8080/view_logs.html
```

### Step 3: Make API Requests

The log viewer will show all API requests in real-time!

---

## Features

### 🔄 Auto-Refresh
- Toggle "Auto-refresh" checkbox
- Updates every 2 seconds automatically
- Perfect for live demos

### 📊 Statistics
- **Total Requests**: Number of API calls made
- **Last Update**: When logs were last refreshed
- **Auto-refresh Status**: ON/OFF indicator

### 🎨 Color Coding
- **Green (➡️)**: Incoming requests
- **Orange (⬅️)**: Outgoing responses
- **Different colors** for methods, status codes, roles

### 🎯 Controls
- **🔄 Refresh Now**: Manual refresh
- **🗑️ Clear Display**: Clear the log display (doesn't delete file)
- **Auto-refresh toggle**: Enable/disable automatic updates

---

## Demo Setup

### Terminal Setup (4 terminals):

**Terminal 1: Streamlit UI**
```bash
streamlit run app.py
```
Access: http://localhost:8501

**Terminal 2: API Server**
```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```
Access: http://localhost:8000

**Terminal 3: Log Viewer Server**
```bash
python3 serve_logs.py
```
Access: http://localhost:8080/view_logs.html

**Terminal 4: Testing**
```bash
# Run test commands here
curl -X GET http://localhost:8000/api/v1/credentials \
  -H "X-API-Key: admin_key_123"
```

---

## Browser Setup (3 tabs):

1. **Streamlit UI** - http://localhost:8501
2. **API Docs (Swagger)** - http://localhost:8000/api/docs
3. **Log Viewer** - http://localhost:8080/view_logs.html

---

## Demo Flow

### 1. Show Log Viewer
- Open http://localhost:8080/view_logs.html
- Enable "Auto-refresh"
- Show existing logs

### 2. Make API Request via Swagger
- Go to http://localhost:8000/api/docs
- Expand "POST /api/v1/credentials"
- Click "Try it out"
- Add API key: `admin_key_123`
- Fill in example data:
```json
{
  "supplier": "Booking.com",
  "environment": "production",
  "auth_type": "api_key",
  "data": {
    "api_key": "booking_key_xyz123"
  },
  "allow_self_rotation": false
}
```
- Click "Execute"

### 3. Watch Logs Update
- **In Log Viewer**: See the POST request appear
- **In Streamlit**: Click "🔄 Refresh Data" to see new credential
- **In Swagger**: See the 201 response

### 4. Verify in Streamlit
- Go to Streamlit Dashboard tab
- Click "🔄 Refresh Data" button
- See the new "Booking.com" credential
- Expand it in Credential Actions
- Click "View Details"

---

## Troubleshooting

### Log Viewer Shows "Not Connected"
- Make sure API server is running
- Make sure `api_requests.log` file exists
- Try clicking "🔄 Refresh Now"

### No Logs Appearing
- Make sure you've made at least one API request
- Check that `api_requests.log` has content:
  ```bash
  cat api_requests.log
  ```

### Streamlit Not Showing New Credentials
- Click the "🔄 Refresh Data" button in Dashboard
- Streamlit doesn't auto-refresh - manual refresh needed

### Port Already in Use
If port 8080 is in use, edit `serve_logs.py` and change:
```python
PORT = 8080  # Change to another port like 8081
```

---

## Alternative: Terminal Log Viewer

If you prefer terminal, use:

```bash
python3 watch_logs.py
```

This shows colored, real-time logs in your terminal.

---

## Tips for Demo

1. **Split Screen**: 
   - Left: Streamlit UI
   - Right: Log Viewer

2. **Pre-open All Tabs**:
   - Streamlit, Swagger, Log Viewer
   - Switch between them during demo

3. **Use Auto-refresh**:
   - Enable it before making requests
   - Logs appear automatically

4. **Show The Flow**:
   - API Request (Swagger) →
   - Log Entry (Log Viewer) →
   - Database Update (Streamlit)

5. **Highlight Real-time**:
   - "Watch as I make this API call..."
   - *Make request*
   - "And here it is in the logs instantly!"

---

## Example Test Requests

```bash
# Create credential
curl -X POST http://localhost:8000/api/v1/credentials \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "supplier": "Expedia",
    "environment": "production",
    "auth_type": "api_key",
    "data": {"api_key": "expedia_key_123"},
    "allow_self_rotation": true
  }'

# List credentials
curl -X GET http://localhost:8000/api/v1/credentials \
  -H "X-API-Key: admin_key_123"

# Rotate credential
curl -X POST http://localhost:8000/api/v1/credentials/1/rotate \
  -H "X-API-Key: admin_key_123"

# Get audit logs
curl -X GET http://localhost:8000/api/v1/audit-logs?limit=10 \
  -H "X-API-Key: admin_key_123"
```

---

Good luck with your demo! 🚀

