# Nezasa Connect API – Credential Management System

A comprehensive credential management system with both a **Streamlit UI** and a **REST API** for managing supplier API credentials with role-based access control (RBAC).

---

## 🚀 Quick Start

### ☁️ Production Deployment (Recommended)

The application is deployed and ready to use:

- **Streamlit UI:** Access via Streamlit Cloud (check your deployment)
- **REST API:** `https://vibe-coding-project-production.up.railway.app`
- **API Documentation:** `https://vibe-coding-project-production.up.railway.app/api/docs`

No local setup required! Just visit the URLs above.

---

### 💻 Local Development

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Run the Application

##### Option A: Streamlit UI (Recommended for Demo)

```bash
streamlit run app.py
```

Access the UI at: **http://localhost:8501**

##### Option B: REST API (Local)

```bash
python api.py
```

Or with uvicorn:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Access the API at: **http://localhost:8000**

Interactive API docs: **http://localhost:8000/api/docs**

##### Option C: Run Both Simultaneously

**Terminal 1:**
```bash
streamlit run app.py
```

**Terminal 2:**
```bash
python api.py
```

> **Note:** The Streamlit app is configured to use the Railway production API by default. To use your local API, update `API_BASE_URL` in `app.py` to `http://127.0.0.1:8000`

---

## 📋 Features

### Streamlit UI
- ✅ **Role-Based Access Control** - Admin, DevOps, CS, Partner roles
- ✅ **Credential Management** - Create, update, view, rotate, delete credentials
- ✅ **Credential Dashboard** - Visual overview of all credentials
- ✅ **Audit Trail** - Complete history of all credential operations
- ✅ **Secret Masking** - Automatic masking for non-admin roles
- ✅ **Real Suppliers** - Pre-loaded with Sabre, Amadeus, Google Maps, Stripe, etc.

### REST API
- ✅ **Full CRUD Operations** - Create, Read, Update, Delete credentials
- ✅ **Credential Rotation** - Automated key/password rotation
- ✅ **Audit Logging** - Track all API operations
- ✅ **Role-Based Permissions** - API key authentication with RBAC
- ✅ **OpenAPI/Swagger Docs** - Interactive API documentation
- ✅ **Filtering & Search** - Query credentials by supplier, environment

---

## 🔐 Demo Credentials

### Streamlit UI Roles
Select from the sidebar:
- `admin` - Full access
- `devops` - Update, view unmasked
- `cs` - View masked only
- `partner` - View masked, rotate if allowed

### API Keys
| API Key | Role | Use Case |
|---------|------|----------|
| `admin_key_123` | admin | Full API access |
| `devops_key_456` | devops | Update & view operations |
| `cs_key_789` | cs | Read-only access |
| `partner_key_012` | partner | Self-service rotation |

---

## 📖 Documentation

- **API Reference:** See [API_REFERENCE.md](./API_REFERENCE.md)
- **Database Setup:** See [DATABASE_SETUP.md](./DATABASE_SETUP.md)

---

## 📊 Viewing API Logs

The API server logs all requests to `api_requests.log`. You have several ways to view these logs:

### Option 1: HTML Log Viewer (Recommended for Demo)

Open in your browser:
```bash
open view_logs.html
```
Or just double-click `view_logs.html` in Finder.

**Features:**
- 🎨 Beautiful dark theme UI
- 🔄 Auto-refresh every 2 seconds
- 📊 Request statistics
- 🎯 Color-coded requests/responses
- 🖥️ Great for screen sharing

### Option 2: Terminal Log Watcher

Real-time colored terminal output:
```bash
python3 watch_logs.py
```

**Features:**
- 🌈 Color-coded output
- ⚡ Real-time updates
- 📜 Shows last 20 existing logs
- 💻 Perfect for technical demos

### Option 3: Simple Terminal Commands

```bash
# View all logs
cat api_requests.log

# Watch logs in real-time
tail -f api_requests.log

# View last 20 lines
tail -n 20 api_requests.log

# Filter by method
grep "GET" api_requests.log
grep "POST" api_requests.log

# Filter by status code
grep "Status: 200" api_requests.log
grep "Status: 4" api_requests.log  # Client errors
```

---

## 🧪 Testing the API

### Using Production API (Railway)

Replace `http://localhost:8000` with `https://vibe-coding-project-production.up.railway.app` in the examples below to test the production API.

### Example: Create a Credential

**Production:**
```bash
curl -X POST https://vibe-coding-project-production.up.railway.app/api/v1/credentials \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "supplier": "Stripe",
    "environment": "production",
    "auth_type": "api_key",
    "data": {"api_key": "sk_live_xyz123"},
    "allow_self_rotation": false
  }'
```

**Local:**
```bash
curl -X POST http://localhost:8000/api/v1/credentials \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "supplier": "Stripe",
    "environment": "production",
    "auth_type": "api_key",
    "data": {"api_key": "sk_live_xyz123"},
    "allow_self_rotation": false
  }'
```

### Example: List All Credentials

**Production:**
```bash
curl -X GET https://vibe-coding-project-production.up.railway.app/api/v1/credentials \
  -H "X-API-Key: admin_key_123"
```

**Local:**
```bash
curl -X GET http://localhost:8000/api/v1/credentials \
  -H "X-API-Key: admin_key_123"
```

### Example: Rotate a Credential

**Production:**
```bash
curl -X POST https://vibe-coding-project-production.up.railway.app/api/v1/credentials/1/rotate \
  -H "X-API-Key: admin_key_123"
```

**Local:**
```bash
curl -X POST http://localhost:8000/api/v1/credentials/1/rotate \
  -H "X-API-Key: admin_key_123"
```

### Interactive API Documentation

Visit the Swagger UI to test the API interactively:
- **Production:** `https://vibe-coding-project-production.up.railway.app/api/docs`
- **Local:** `http://localhost:8000/api/docs`

---

## 🗂️ Project Structure

```
vibe-coding-project/
├── app.py                  # Streamlit UI application
├── api.py                  # FastAPI REST API
├── credentials.db          # SQLite database (auto-created)
├── database_config.py      # Database configuration
├── requirements.txt        # Python dependencies
├── API_REFERENCE.md        # Complete API documentation
├── DATABASE_SETUP.md       # Database setup guide
└── README.md              # This file
```

---

## 🏢 Pre-loaded Suppliers

The system comes with 10 real supplier credentials:

1. **Sabre** - GDS/Travel API
2. **Amadeus** - GDS/Travel API
3. **Google Maps** - Mapping API
4. **Stripe** - Payment Processing
5. **Payyo** - Payment Gateway
6. **Viator** - Tours & Activities
7. **Musement** - Tours & Activities
8. **G Adventures** - Travel Tours
9. **OTS Globe** - Travel Technology
10. **TUI** - Travel & Tourism

---

## 🎯 Use Cases

### 1. Self-Service Partner Portal
Partners can view and rotate their own credentials without contacting support.

### 2. DevOps Automation
DevOps team can integrate the API into CI/CD pipelines for automated credential rotation.

### 3. Customer Support
CS team can safely view credential information (masked) to assist customers.

### 4. Audit & Compliance
Admin can review complete audit trails for security and compliance requirements.

---

## ☁️ Deployment

### Current Production Setup

- **API Backend:** Deployed on [Railway](https://railway.app)
  - URL: `https://vibe-coding-project-production.up.railway.app`
  - Database: SQLite (auto-deployed with the app)
  - Free tier: 500 hours/month
  
- **Streamlit UI:** Deployed on [Streamlit Cloud](https://streamlit.io/cloud)
  - Connects to Railway API
  - Auto-deploys on Git push

### Deploy Your Own

#### Deploy API to Railway:
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects and deploys
6. Copy your Railway URL
7. Update `API_BASE_URL` in `app.py`

#### Deploy UI to Streamlit Cloud:
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign up with GitHub
3. Click "New app"
4. Select your repository and `app.py`
5. Deploy!

See deployment guides:
- [railway-deploy.md](./railway-deploy.md)
- [render-deploy.md](./render-deploy.md)
- [heroku-deploy.md](./heroku-deploy.md)

---

## 🔧 Configuration

### Switch to PostgreSQL

Edit `database_config.py`:

```python
return {
    "use_postgres": True,
    "postgres_url": "postgresql://user:pass@host:5432/dbname",
    "sqlite_path": "credentials.db"
}
```

See [DATABASE_SETUP.md](./DATABASE_SETUP.md) for details.

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend API:** FastAPI
- **Database:** SQLite (default) / PostgreSQL (optional)
- **ORM:** SQLAlchemy
- **API Docs:** OpenAPI/Swagger
- **Authentication:** API Key (demo) / JWT (production-ready)

---

## 📝 Notes

- This is a **demo/POC system** for product interviews
- For production use, implement:
  - JWT/OAuth2 authentication
  - HTTPS/TLS encryption
  - Proper secrets management (Vault, AWS Secrets Manager)
  - Rate limiting
  - Enhanced audit logging
  - IP whitelisting

---

## 🤝 Support

For questions or issues:
- Email: engineering@nezasa.com
- Documentation: See API_REFERENCE.md

---

## 📄 License

Demo/POC for Nezasa product interview purposes.
