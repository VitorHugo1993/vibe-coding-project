# 🎬 Demo Guide - Nezasa Connect API Credential Management

## Complete Demo Setup and Flow

This guide will help you demonstrate the full capabilities of the Nezasa Connect Credential Management System during your product interview.

---

## 🚀 Quick Setup (Before Demo)

### 1. Terminal Setup (3 terminals needed)

**Terminal 1: Streamlit UI**
```bash
cd /Users/vitorhugooliveira/vibe-coding-project
streamlit run app.py
```
Access at: http://localhost:8501

**Terminal 2: API Server**
```bash
cd /Users/vitorhugooliveira/vibe-coding-project
python3 api.py
```
Access at: http://localhost:8000
API Docs: http://localhost:8000/api/docs

**Terminal 3: API Testing**
```bash
cd /Users/vitorhugooliveira/vibe-coding-project
# Ready to run test commands
```

---

## 📋 Demo Flow (15-20 minutes)

### Part 1: UI Overview (5 minutes)

#### 1.1 Role-Based Access Control
**What to show:**
- Open Streamlit UI
- Switch between different roles in sidebar:
  - **Admin** → Show full access
  - **DevOps** → Show update capabilities
  - **CS** → Show read-only with masked data
  - **Partner** → Show limited self-service

**Key Points:**
- Different roles see different UI elements
- Secrets are automatically masked for non-admin roles
- Partner role demonstrates self-service model

#### 1.2 Dashboard Tab
**What to show:**
- Navigate to **Dashboard** tab
- Show 10 real supplier credentials (Sabre, Amadeus, Stripe, etc.)
- Expand a credential in "Credential Actions"
- Click "View Details" to show credential data
- Point out masked vs unmasked data based on role

**Key Points:**
- Real-world supplier names
- Clean, professional UI
- Easy credential management

#### 1.3 Create Credential (Admin only)
**What to show:**
- Switch to **Admin** role
- Navigate to **Create Credential** tab
- Create a new credential:
  - Supplier: "Booking.com"
  - Environment: "production"
  - Auth Type: "api_key"
  - API Key: "booking_prod_key_123"
- Switch auth type to show dynamic form fields
- Click "Create Credential"
- Show success message

**Key Points:**
- Dynamic form based on auth type
- Validation and error handling
- Immediate feedback

#### 1.4 Audit Logs
**What to show:**
- Navigate to **Audit Logs** tab
- Show complete history of all operations
- Use filters to find specific actions
- Export audit trail as CSV

**Key Points:**
- Complete audit trail
- Compliance-ready logging
- Multiple action types (create, update, rotate, view)

---

### Part 2: API Demo (5 minutes)

#### 2.1 Interactive API Documentation
**What to show:**
- Open browser to: http://localhost:8000/api/docs
- Show Swagger UI with all endpoints
- Expand an endpoint (e.g., GET /api/v1/credentials)
- Click "Try it out"
- Add API key: `admin_key_123`
- Execute request
- Show response

**Key Points:**
- Production-ready REST API
- Interactive documentation
- Standard HTTP methods
- Role-based API keys

#### 2.2 Command Line API Testing
**Terminal 3 - Run these commands:**

```bash
# 1. List all credentials
curl -X GET http://localhost:8000/api/v1/credentials \
  -H "X-API-Key: admin_key_123" | python3 -m json.tool

# 2. Create a new credential
curl -X POST http://localhost:8000/api/v1/credentials \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "supplier": "Expedia",
    "environment": "production",
    "auth_type": "api_key",
    "data": {"api_key": "expedia_key_xyz"},
    "allow_self_rotation": true
  }'

# 3. Rotate a credential
curl -X POST http://localhost:8000/api/v1/credentials/1/rotate \
  -H "X-API-Key: admin_key_123"

# 4. Get audit logs
curl -X GET http://localhost:8000/api/v1/audit-logs?limit=10 \
  -H "X-API-Key: admin_key_123" | python3 -m json.tool
```

**Key Points:**
- RESTful API design
- JSON request/response
- Immediate database updates
- Audit logging for all operations

---

### Part 3: Live API Monitoring (5 minutes)

#### 3.1 API Monitor Tab
**What to show:**
- In Streamlit UI, navigate to **API Monitor** tab
- Enable "Auto-refresh" checkbox
- In Terminal 3, run API commands (see above)
- Watch requests appear in real-time in the log viewer

**Key Points:**
- Real-time request logging
- See API activity as it happens
- Great for debugging and monitoring

#### 3.2 Database View
**What to show:**
- Still in **API Monitor** tab
- Click on **Credentials Table** sub-tab
- Show raw database data
- Click on **Audit Logs Table** sub-tab
- Show audit trail from database perspective
- Click on **Database Stats** sub-tab
- Show statistics and metrics

**Key Points:**
- Direct database visibility
- Data persistence
- Complete transparency

#### 3.3 SQL Query Runner (Advanced)
**What to show:**
- Expand "Run Custom SQL Query" section
- Run a query:
  ```sql
  SELECT supplier, environment, created_by, created_at 
  FROM credentials 
  WHERE environment = 'production' 
  ORDER BY created_at DESC;
  ```
- Show results

**Key Points:**
- Technical flexibility
- Database queries for advanced users
- Read-only for safety

---

### Part 4: Integration Use Cases (3 minutes)

#### 4.1 Self-Service Partner Portal
**Scenario:** Travel partner needs to rotate their API key

**What to show:**
1. Switch to **Partner** role in UI
2. Go to **Dashboard**
3. Find a credential with "Allow Self Rotation"
4. Click "Rotate"
5. Show new key generated
6. Check audit log for rotation entry

**Key Points:**
- Partners can manage their own credentials
- Reduces support tickets
- Maintains security with audit trail

#### 4.2 DevOps Automation
**Scenario:** DevOps needs to update credentials programmatically

**What to show:**
- In Terminal 3, run:
```bash
curl -X PUT http://localhost:8000/api/v1/credentials/2 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: devops_key_456" \
  -d '{"data": {"api_key": "new_updated_key_2024"}}'
```
- Go back to Streamlit Dashboard
- Click "Refresh Now" in API Monitor
- Show credential was updated
- Show audit log entry

**Key Points:**
- CI/CD integration ready
- Automated credential rotation
- API-first design

#### 4.3 Customer Support
**Scenario:** CS agent needs to verify customer's credential

**What to show:**
1. Switch to **CS** role
2. Go to **Dashboard**
3. View credential details
4. Note that secrets are masked
5. Can confirm credential exists without seeing sensitive data

**Key Points:**
- Secure customer support
- View without compromise
- Compliance-friendly

---

## 🎯 Key Talking Points

### Business Value
- **Reduces support tickets** - Self-service for partners
- **Improves security** - Audit trail, role-based access
- **Increases efficiency** - Automated credential rotation
- **Enhances compliance** - Complete audit logs, masked data

### Technical Excellence
- **Modern stack** - Streamlit UI, FastAPI backend
- **Database flexibility** - SQLite (demo) or PostgreSQL (production)
- **API-first design** - RESTful endpoints with OpenAPI docs
- **Role-based security** - RBAC for UI and API

### Scalability
- **Multi-supplier support** - 10+ suppliers pre-configured
- **Environment separation** - Production, sandbox, staging, dev
- **Audit logging** - All operations tracked
- **Export capabilities** - CSV export for analysis

---

## 🔧 Quick Test Script

For a rapid demo, run the automated test script:

```bash
./test_api.sh
```

This will:
- Run through all major API endpoints
- Show successful operations
- Demonstrate permission errors
- Display data masking
- All while logging to the API Monitor tab!

---

## 💡 Demo Tips

1. **Start with the UI** - It's more visual and easier to understand
2. **Show role switching** - Demonstrates RBAC clearly
3. **Use real-world scenarios** - Partner self-service, DevOps automation
4. **Keep API Monitor tab open** - Shows live activity
5. **Mention production considerations** - JWT auth, secrets management, rate limiting
6. **Show both UI and API** - Demonstrates flexibility
7. **Highlight audit trail** - Important for compliance
8. **Use the test script** - Quick way to generate activity

---

## 📊 Demo Metrics to Highlight

- **10 real suppliers** pre-configured
- **4 role types** (admin, devops, cs, partner)
- **7 API endpoints** fully functional
- **4 action types** logged (create, update, rotate, view)
- **Auto-refresh** monitoring (2-second intervals)
- **Complete audit trail** for compliance
- **Real-time synchronization** between UI and API

---

## 🚨 Troubleshooting

**API not responding?**
```bash
# Check if API is running
curl http://localhost:8000/
```

**Streamlit not showing new data?**
- Click "🔄 Refresh Now" in API Monitor tab
- Or toggle auto-refresh on

**Database empty?**
```bash
# Delete and restart to reload sample data
rm credentials.db
streamlit run app.py
```

**API logs not showing?**
- Make sure API server has been started at least once
- Run a test request to generate logs

---

## 📞 Questions to Anticipate

**Q: How would this work in production?**
A: Replace demo API keys with JWT/OAuth2, use PostgreSQL, add rate limiting, enable HTTPS, integrate with secrets management (Vault/AWS Secrets Manager).

**Q: Can this scale to hundreds of suppliers?**
A: Yes, database-backed design scales well. Can add pagination, caching, and search functionality.

**Q: How do you handle credential expiration?**
A: Can add expiration dates, automated rotation schedules, and expiry notifications.

**Q: What about multi-region support?**
A: Can add region field to credentials, deploy API to multiple regions, use geo-distributed database.

**Q: How do you ensure security?**
A: RBAC, audit logging, secret masking, encryption at rest (can be added), HTTPS, API key rotation.

---

## ✅ Demo Checklist

Before the demo:
- [ ] All 3 terminals running (Streamlit, API, Testing)
- [ ] Browser tabs open (Streamlit UI, API Docs)
- [ ] Database has sample data (10 suppliers)
- [ ] Test one API request to verify everything works
- [ ] Have API keys handy for reference

During the demo:
- [ ] Show all 4 roles in UI
- [ ] Demonstrate CRUD operations
- [ ] Run live API requests
- [ ] Show real-time monitoring
- [ ] Highlight audit trail
- [ ] Discuss production considerations

---

Good luck with your demo! 🚀

