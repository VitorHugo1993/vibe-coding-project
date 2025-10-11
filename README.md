# 🔐 Nezasa Connect API Credential Management System (POC)

A comprehensive Streamlit application that simulates the Nezasa Connect API Credential Management System for product demonstration during interviews.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the app:**
   - Open your browser to `http://localhost:8501`
   - The app will automatically initialize the SQLite database with sample data

## 🎯 Demo Features

### ✅ Core Functionality
- **Role-Based Access Control (RBAC)**: 4 distinct roles with different permissions
- **Credential Management**: Full CRUD operations for API credentials
- **Credential Rotation**: Automatic secret regeneration with audit logging
- **Audit Trail**: Complete action logging with filtering and export capabilities
- **Security Simulation**: Credential masking based on user roles
- **Professional UI**: Clean, modern interface optimized for demos

### 🔑 Supported Roles

| Role | Create | Update | Rotate | View Unmasked | View Audit |
|------|--------|--------|--------|---------------|------------|
| **Admin** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DevOps** | ❌ | ✅ | ❌ | ✅ | ✅ |
| **CS** | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Partner** | ❌ | ❌ | Conditional* | ❌ | ❌ |

*Partners can rotate credentials only if `allow_self_rotation` is enabled

### 📊 Sample Data
The app comes pre-loaded with 3 example credentials:
- **SupplierA** (production, API key) - Created by alice@nezasa.com
- **SupplierB** (sandbox, username/password) - Created by bob@devops.nezasa.com  
- **SupplierC** (production, API key) - Created by carol@cs.nezasa.com

## 🎬 Demo Flow (10-minute presentation)

### 1. **Introduction (2 minutes)**
- Show the clean, professional UI
- Explain the role selector and RBAC system
- Demonstrate the 3 main tabs: Dashboard, Create Credential, Audit Logs

### 2. **Admin Demo (3 minutes)**
- Switch to **Admin** role
- Create a new credential for "Expedia" (production, API key)
- Show the credential appears in the dashboard
- Demonstrate credential rotation
- View audit logs to show the actions were logged

### 3. **Role-Based Access Demo (3 minutes)**
- Switch to **Partner** role
- Show masked credential data (`*****1234`)
- Attempt to rotate a credential (success if allowed, failure if not)
- Switch to **CS** role
- Show read-only access with masked data
- Switch to **DevOps** role
- Demonstrate update functionality

### 4. **Audit & Compliance Demo (2 minutes)**
- Switch back to **Admin**
- Open Audit Logs tab
- Show filtering by supplier, action, actor
- Demonstrate CSV export functionality
- Highlight compliance and audit trail benefits

## 🏗️ Technical Architecture

### Database Schema
```sql
-- Credentials table
credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier TEXT NOT NULL,
    environment TEXT NOT NULL,
    auth_type TEXT NOT NULL,
    data TEXT NOT NULL,  -- JSON format
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    allow_self_rotation BOOLEAN DEFAULT FALSE
)

-- Audit logs table
audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cred_id INTEGER,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    details TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (cred_id) REFERENCES credentials (id)
)
```

### Key Classes
- **DatabaseManager**: SQLite database operations and initialization
- **RBACManager**: Role-based access control logic
- **CredentialManager**: CRUD operations and business logic

### Security Features
- Credential masking for non-admin roles
- Audit logging for all actions
- Permission validation before operations
- Simulated encryption (shows `encrypted(...)` format)

## 🔧 Customization Options

### Adding New Roles
Edit the `RBACManager.ROLES` dictionary in `app.py`:
```python
"new_role": {
    "can_create": True,
    "can_update": False,
    "can_rotate": True,
    "can_view_unmasked": False,
    "can_view_audit": True,
    "description": "Custom role description"
}
```

### Adding New Auth Types
1. Update the `auth_type` selectbox options
2. Add handling in the credential creation/update forms
3. Update the `mask_secret_data()` function for proper masking

### Styling Customization
Modify the CSS in the `st.markdown()` call at the top of `main()` function.

## 🚀 Production Considerations

This is a **Proof of Concept** application. For production use, consider:

### Security
- Replace SQLite with PostgreSQL/MySQL
- Implement proper encryption (not simulated)
- Add HTTPS and proper authentication
- Use environment variables for sensitive configuration
- Implement rate limiting and input validation

### Scalability
- Add database connection pooling
- Implement caching (Redis)
- Add API endpoints for external integrations
- Consider microservices architecture

### Integration
- Connect to actual supplier APIs for validation
- Integrate with HashiCorp Vault or similar secret management
- Add LDAP/Active Directory integration
- Implement webhook notifications

## 📁 File Structure

```
vibe-coding-project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── credentials.db        # SQLite database (auto-created)
└── .gitignore           # Git ignore rules
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Database permissions:**
   - Ensure write permissions in the project directory
   - Delete `credentials.db` to reset sample data

3. **Missing dependencies:**
   ```bash
   pip install --upgrade streamlit pandas
   ```

## 📞 Support

This is a demonstration application created for product interviews. For questions about the implementation or customization, refer to the inline code comments in `app.py`.

---

**Built with ❤️ using Streamlit**
