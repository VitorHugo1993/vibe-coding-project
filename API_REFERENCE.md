# Nezasa Connect API – Credential Management

## API Reference Documentation

Base URL: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/api/docs`

---

## Authentication

All API endpoints require authentication using an API key passed in the `X-API-Key` header.

### Available API Keys (Demo)

| API Key | Role | Permissions |
|---------|------|-------------|
| `admin_key_123` | admin | Full access (create, update, rotate, delete, view unmasked) |
| `devops_key_456` | devops | Update, view unmasked, view audit logs |
| `cs_key_789` | cs | View masked credentials only |
| `partner_key_012` | partner | View masked, rotate if allowed |

### Example Authentication Header

```bash
X-API-Key: admin_key_123
```

---

## Endpoints

### 1️⃣ POST /api/v1/credentials

**Create a new supplier credential**

**Required Role:** `admin`

#### Request

```bash
curl -X POST http://localhost:8000/api/v1/credentials \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "supplier": "Stripe",
    "environment": "production",
    "auth_type": "api_key",
    "data": {
      "api_key": "sk_live_xyz123456789"
    },
    "allow_self_rotation": false
  }'
```

#### Response (201 Created)

```json
{
  "id": 11,
  "supplier": "Stripe",
  "environment": "production",
  "auth_type": "api_key",
  "data": {
    "api_key": "sk_live_xyz123456789"
  },
  "created_by": "admin@demo.com",
  "created_at": "2024-10-12T10:30:00",
  "updated_at": "2024-10-12T10:30:00",
  "allow_self_rotation": false
}
```

---

### 2️⃣ GET /api/v1/credentials

**List all credentials**

**Required Role:** Any authenticated user

**Query Parameters:**
- `supplier` (optional): Filter by supplier name
- `environment` (optional): Filter by environment

#### Request

```bash
# List all credentials
curl -X GET http://localhost:8000/api/v1/credentials \
  -H "X-API-Key: admin_key_123"

# Filter by supplier
curl -X GET "http://localhost:8000/api/v1/credentials?supplier=Stripe" \
  -H "X-API-Key: admin_key_123"

# Filter by environment
curl -X GET "http://localhost:8000/api/v1/credentials?environment=production" \
  -H "X-API-Key: admin_key_123"
```

#### Response (200 OK)

```json
{
  "total": 10,
  "credentials": [
    {
      "id": 1,
      "supplier": "Sabre",
      "environment": "production",
      "auth_type": "api_key",
      "data": {
        "api_key": "sabre_prod_key_9x8y7z6"
      },
      "created_by": "alice@nezasa.com",
      "created_at": "2024-10-12T09:00:00",
      "updated_at": "2024-10-12T09:00:00",
      "allow_self_rotation": true
    },
    {
      "id": 2,
      "supplier": "Amadeus",
      "environment": "production",
      "auth_type": "api_key",
      "data": {
        "api_key": "amadeus_api_a1b2c3d4e5"
      },
      "created_by": "bob@nezasa.com",
      "created_at": "2024-10-12T09:00:00",
      "updated_at": "2024-10-12T09:00:00",
      "allow_self_rotation": false
    }
  ]
}
```

**Note:** Data is automatically masked for non-admin roles (cs, partner).

---

### 3️⃣ GET /api/v1/credentials/{credential_id}

**Get a specific credential by ID**

**Required Role:** Any authenticated user

#### Request

```bash
curl -X GET http://localhost:8000/api/v1/credentials/1 \
  -H "X-API-Key: admin_key_123"
```

#### Response (200 OK)

```json
{
  "id": 1,
  "supplier": "Sabre",
  "environment": "production",
  "auth_type": "api_key",
  "data": {
    "api_key": "sabre_prod_key_9x8y7z6"
  },
  "created_by": "alice@nezasa.com",
  "created_at": "2024-10-12T09:00:00",
  "updated_at": "2024-10-12T09:00:00",
  "allow_self_rotation": true
}
```

#### Response (404 Not Found)

```json
{
  "detail": "Credential not found"
}
```

---

### 4️⃣ PUT /api/v1/credentials/{credential_id}

**Update an existing credential**

**Required Role:** `admin` or `devops`

#### Request

```bash
curl -X PUT http://localhost:8000/api/v1/credentials/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "data": {
      "api_key": "sabre_new_updated_key_2024"
    },
    "environment": "production"
  }'
```

#### Response (200 OK)

```json
{
  "id": 1,
  "supplier": "Sabre",
  "environment": "production",
  "auth_type": "api_key",
  "data": {
    "api_key": "sabre_new_updated_key_2024"
  },
  "created_by": "alice@nezasa.com",
  "created_at": "2024-10-12T09:00:00",
  "updated_at": "2024-10-12T11:15:00",
  "allow_self_rotation": true
}
```

---

### 5️⃣ POST /api/v1/credentials/{credential_id}/rotate

**Rotate a credential (generate new key/password)**

**Required Role:** `admin` or `partner` (if `allow_self_rotation` is true)

#### Request

```bash
curl -X POST http://localhost:8000/api/v1/credentials/1/rotate \
  -H "X-API-Key: admin_key_123"
```

#### Response (200 OK)

```json
{
  "id": 1,
  "supplier": "Sabre",
  "environment": "production",
  "message": "Credential rotated successfully",
  "new_data": {
    "api_key": "sk_rotated_a8f3d2e1b7c4f9e2d1a5b3c7"
  },
  "rotated_at": "2024-10-12T11:30:00"
}
```

#### Response (403 Forbidden)

```json
{
  "detail": "Insufficient permissions to rotate this credential"
}
```

---

### 6️⃣ DELETE /api/v1/credentials/{credential_id}

**Delete a credential**

**Required Role:** `admin`

#### Request

```bash
curl -X DELETE http://localhost:8000/api/v1/credentials/1 \
  -H "X-API-Key: admin_key_123"
```

#### Response (204 No Content)

No response body.

---

### 7️⃣ GET /api/v1/audit-logs

**Get audit logs for credential operations**

**Required Role:** `admin` or `devops`

**Query Parameters:**
- `credential_id` (optional): Filter by specific credential
- `action` (optional): Filter by action type (create, update, rotate, delete, view)
- `limit` (optional): Maximum number of logs (default: 100)

#### Request

```bash
# Get all audit logs
curl -X GET http://localhost:8000/api/v1/audit-logs \
  -H "X-API-Key: admin_key_123"

# Filter by credential
curl -X GET "http://localhost:8000/api/v1/audit-logs?credential_id=1" \
  -H "X-API-Key: admin_key_123"

# Filter by action
curl -X GET "http://localhost:8000/api/v1/audit-logs?action=rotate&limit=50" \
  -H "X-API-Key: admin_key_123"
```

#### Response (200 OK)

```json
[
  {
    "id": 15,
    "cred_id": 1,
    "action": "rotate",
    "actor": "admin@demo.com",
    "details": "Rotated credential 1 via API",
    "timestamp": "2024-10-12T11:30:00"
  },
  {
    "id": 14,
    "cred_id": 1,
    "action": "update",
    "actor": "admin@demo.com",
    "details": "Updated credential 1 via API",
    "timestamp": "2024-10-12T11:15:00"
  },
  {
    "id": 1,
    "cred_id": 1,
    "action": "create",
    "actor": "alice@nezasa.com",
    "details": "Created credential for Sabre (production)",
    "timestamp": "2024-10-12T09:00:00"
  }
]
```

---

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Invalid API key"
}
```

### 403 Forbidden

```json
{
  "detail": "Role 'cs' does not have permission: create"
}
```

### 404 Not Found

```json
{
  "detail": "Credential not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Database error: ..."
}
```

---

## Running the API

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
python api.py
```

Or using uvicorn directly:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access Interactive Documentation

Open your browser:
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## Example Use Cases

### Use Case 1: Create and Rotate a Credential

```bash
# 1. Create a new credential
curl -X POST http://localhost:8000/api/v1/credentials \
  -H "Content-Type: application/json" \
  -H "X-API-Key: admin_key_123" \
  -d '{
    "supplier": "New Supplier",
    "environment": "production",
    "auth_type": "api_key",
    "data": {"api_key": "initial_key_123"},
    "allow_self_rotation": true
  }'

# Response: {"id": 11, ...}

# 2. Rotate the credential
curl -X POST http://localhost:8000/api/v1/credentials/11/rotate \
  -H "X-API-Key: admin_key_123"

# Response: {"new_data": {"api_key": "sk_rotated_..."}, ...}
```

### Use Case 2: Partner Self-Service Rotation

```bash
# Partner can rotate their own credential (if allowed)
curl -X POST http://localhost:8000/api/v1/credentials/6/rotate \
  -H "X-API-Key: partner_key_012"
```

### Use Case 3: DevOps Updates Production Key

```bash
# DevOps updates a production credential
curl -X PUT http://localhost:8000/api/v1/credentials/3 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: devops_key_456" \
  -d '{
    "data": {"api_key": "updated_production_key"}
  }'
```

### Use Case 4: Audit Trail Review

```bash
# Admin reviews all rotation actions
curl -X GET "http://localhost:8000/api/v1/audit-logs?action=rotate" \
  -H "X-API-Key: admin_key_123"
```

---

## Integration Example (Python)

```python
import requests

API_BASE = "http://localhost:8000"
API_KEY = "admin_key_123"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Create a credential
response = requests.post(
    f"{API_BASE}/api/v1/credentials",
    headers=headers,
    json={
        "supplier": "Booking.com",
        "environment": "production",
        "auth_type": "api_key",
        "data": {"api_key": "booking_api_key_123"},
        "allow_self_rotation": False
    }
)

if response.status_code == 201:
    credential = response.json()
    print(f"Created credential ID: {credential['id']}")
    
    # List all credentials
    response = requests.get(
        f"{API_BASE}/api/v1/credentials",
        headers=headers
    )
    
    credentials = response.json()
    print(f"Total credentials: {credentials['total']}")
```

---

## Security Notes

🔒 **For Production Use:**
1. Replace demo API keys with secure token-based authentication (JWT, OAuth2)
2. Enable HTTPS/TLS encryption
3. Implement rate limiting
4. Add request validation and sanitization
5. Use proper secrets management (HashiCorp Vault, AWS Secrets Manager)
6. Enable audit logging to external systems
7. Implement IP whitelisting for API access
8. Add CORS restrictions for specific origins

---

## Support

For questions or issues, contact: **engineering@nezasa.com**

