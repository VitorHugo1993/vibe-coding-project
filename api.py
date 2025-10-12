"""
Nezasa Connect API - Credential Management REST API
FastAPI backend for credential management operations
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import sqlite3
import json
import hashlib
import uuid
import logging
import time

# Initialize FastAPI app
app = FastAPI(
    title="Nezasa Connect API - Credential Management",
    description="Self-service API credential management system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH = "credentials.db"

# Setup logging to file for demo purposes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_requests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests for demo purposes"""
    start_time = time.time()
    
    # Get API key from header
    api_key = request.headers.get("x-api-key", "none")
    role = VALID_API_KEYS.get(api_key, {}).get("role", "unknown")
    
    # Log request
    logger.info(f"➡️  {request.method} {request.url.path} | Role: {role}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(f"⬅️  {request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration:.3f}s")
    
    return response

# ==================== Models ====================

class CredentialCreate(BaseModel):
    supplier: str = Field(..., description="Name of the API supplier", example="Sabre")
    environment: str = Field(..., description="Target environment", example="production")
    auth_type: str = Field(..., description="Authentication type", example="api_key")
    data: Dict[str, Any] = Field(..., description="Authentication data (API key or username/password)", 
                                  example={"api_key": "sk_live_xyz123"})
    allow_self_rotation: bool = Field(default=False, description="Allow partner role to rotate this credential")

class CredentialUpdate(BaseModel):
    supplier: Optional[str] = Field(None, description="Updated supplier name")
    environment: Optional[str] = Field(None, description="Updated environment")
    auth_type: Optional[str] = Field(None, description="Updated authentication type")
    data: Optional[Dict[str, Any]] = Field(None, description="Updated authentication data")
    allow_self_rotation: Optional[bool] = Field(None, description="Updated self-rotation flag")

class CredentialResponse(BaseModel):
    id: int
    supplier: str
    environment: str
    auth_type: str
    data: Dict[str, Any]
    created_by: str
    created_at: str
    updated_at: str
    allow_self_rotation: bool

class CredentialListResponse(BaseModel):
    total: int
    credentials: List[CredentialResponse]

class RotateResponse(BaseModel):
    id: int
    supplier: str
    environment: str
    message: str
    new_data: Dict[str, Any]
    rotated_at: str

class AuditLogResponse(BaseModel):
    id: int
    cred_id: int
    action: str
    actor: str
    details: str
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: str

# ==================== Authentication & Authorization ====================

# Simple API key authentication for demo purposes
VALID_API_KEYS = {
    "admin_key_123": {"role": "admin", "email": "admin@demo.com"},
    "devops_key_456": {"role": "devops", "email": "devops@demo.com"},
    "cs_key_789": {"role": "cs", "email": "cs@demo.com"},
    "partner_key_012": {"role": "partner", "email": "partner@demo.com"}
}

ROLE_PERMISSIONS = {
    "admin": ["create", "update", "rotate", "view_unmasked", "view_audit"],
    "devops": ["update", "view_unmasked", "view_audit"],
    "cs": ["view_masked"],
    "partner": ["view_masked", "rotate_if_allowed"]
}

def verify_api_key(x_api_key: str = Header(..., description="API Key for authentication")):
    """Verify API key and return user info"""
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return VALID_API_KEYS[x_api_key]

def check_permission(user: dict, permission: str):
    """Check if user has required permission"""
    role = user["role"]
    if permission not in ROLE_PERMISSIONS.get(role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{role}' does not have permission: {permission}"
        )

# ==================== Database Functions ====================

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def mask_credential_data(data: dict, auth_type: str) -> dict:
    """Mask sensitive credential data"""
    masked_data = data.copy()
    if auth_type == "api_key" and "api_key" in masked_data:
        key = masked_data["api_key"]
        masked_data["api_key"] = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
    elif auth_type == "username_password":
        if "password" in masked_data:
            masked_data["password"] = "********"
    return masked_data

def simulate_credential_rotation(auth_type: str, old_data: dict) -> dict:
    """Simulate credential rotation by generating new values"""
    if auth_type == "api_key":
        new_key = hashlib.sha256(f"{uuid.uuid4()}{datetime.now()}".encode()).hexdigest()[:32]
        return {"api_key": f"sk_rotated_{new_key}"}
    elif auth_type == "username_password":
        new_password = hashlib.sha256(f"{uuid.uuid4()}{datetime.now()}".encode()).hexdigest()[:16]
        return {
            "username": old_data.get("username", "rotated_user"),
            "password": f"rotated_{new_password}"
        }
    return old_data

def log_audit(conn, cred_id: int, action: str, actor: str, details: str):
    """Log action to audit trail"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_logs (cred_id, action, actor, details, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (cred_id, action, actor, details, datetime.now().isoformat()))
    conn.commit()

# ==================== API Endpoints ====================

@app.get("/", tags=["Health"])
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "Nezasa Connect API - Credential Management",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.post(
    "/api/v1/credentials",
    response_model=CredentialResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Credentials"],
    summary="Create a new credential",
    description="Create a new supplier credential. Requires admin role."
)
async def create_credential(
    credential: CredentialCreate,
    user: dict = Depends(verify_api_key)
):
    """
    Create a new supplier credential.
    
    **Required Role:** admin
    
    **Example Request:**
    ```json
    {
        "supplier": "Stripe",
        "environment": "production",
        "auth_type": "api_key",
        "data": {
            "api_key": "sk_live_xyz123456789"
        },
        "allow_self_rotation": false
    }
    ```
    """
    check_permission(user, "create")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    try:
        cursor.execute("""
            INSERT INTO credentials (supplier, environment, auth_type, data, created_by, created_at, updated_at, allow_self_rotation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            credential.supplier,
            credential.environment,
            credential.auth_type,
            json.dumps(credential.data),
            user["email"],
            now,
            now,
            credential.allow_self_rotation
        ))
        
        cred_id = cursor.lastrowid
        
        # Log audit
        log_audit(
            conn,
            cred_id,
            "create",
            user["email"],
            f"Created credential for {credential.supplier} ({credential.environment}) via API"
        )
        
        conn.commit()
        
        # Return created credential
        return CredentialResponse(
            id=cred_id,
            supplier=credential.supplier,
            environment=credential.environment,
            auth_type=credential.auth_type,
            data=credential.data,
            created_by=user["email"],
            created_at=now,
            updated_at=now,
            allow_self_rotation=credential.allow_self_rotation
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.get(
    "/api/v1/credentials",
    response_model=CredentialListResponse,
    tags=["Credentials"],
    summary="List all credentials",
    description="Get a list of all credentials. Data is masked for non-admin roles."
)
async def list_credentials(
    supplier: Optional[str] = None,
    environment: Optional[str] = None,
    user: dict = Depends(verify_api_key)
):
    """
    List all credentials with optional filtering.
    
    **Permissions:**
    - admin/devops: View unmasked data
    - cs/partner: View masked data
    
    **Query Parameters:**
    - supplier: Filter by supplier name
    - environment: Filter by environment
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM credentials WHERE 1=1"
    params = []
    
    if supplier:
        query += " AND supplier = ?"
        params.append(supplier)
    
    if environment:
        query += " AND environment = ?"
        params.append(environment)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    # Check if user can view unmasked data
    can_view_unmasked = "view_unmasked" in ROLE_PERMISSIONS.get(user["role"], [])
    
    credentials = []
    for row in rows:
        data = json.loads(row["data"])
        
        # Mask data if user doesn't have permission
        if not can_view_unmasked:
            data = mask_credential_data(data, row["auth_type"])
        
        credentials.append(CredentialResponse(
            id=row["id"],
            supplier=row["supplier"],
            environment=row["environment"],
            auth_type=row["auth_type"],
            data=data,
            created_by=row["created_by"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            allow_self_rotation=bool(row["allow_self_rotation"])
        ))
    
    return CredentialListResponse(
        total=len(credentials),
        credentials=credentials
    )

@app.get(
    "/api/v1/credentials/{credential_id}",
    response_model=CredentialResponse,
    tags=["Credentials"],
    summary="Get credential by ID",
    description="Retrieve a specific credential by ID. Data is masked for non-admin roles."
)
async def get_credential(
    credential_id: int,
    user: dict = Depends(verify_api_key)
):
    """
    Get a specific credential by ID.
    
    **Permissions:**
    - admin/devops: View unmasked data
    - cs/partner: View masked data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (credential_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    # Check if user can view unmasked data
    can_view_unmasked = "view_unmasked" in ROLE_PERMISSIONS.get(user["role"], [])
    
    data = json.loads(row["data"])
    if not can_view_unmasked:
        data = mask_credential_data(data, row["auth_type"])
    
    return CredentialResponse(
        id=row["id"],
        supplier=row["supplier"],
        environment=row["environment"],
        auth_type=row["auth_type"],
        data=data,
        created_by=row["created_by"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        allow_self_rotation=bool(row["allow_self_rotation"])
    )

@app.put(
    "/api/v1/credentials/{credential_id}",
    response_model=CredentialResponse,
    tags=["Credentials"],
    summary="Update credential",
    description="Update an existing credential. Requires admin or devops role."
)
async def update_credential(
    credential_id: int,
    updates: CredentialUpdate,
    user: dict = Depends(verify_api_key)
):
    """
    Update an existing credential.
    
    **Required Role:** admin or devops
    
    **Example Request:**
    ```json
    {
        "data": {
            "api_key": "sk_live_new_key_abc"
        },
        "environment": "production"
    }
    ```
    """
    check_permission(user, "update")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if credential exists
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (credential_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Credential not found")
    
    # Build update query
    update_fields = []
    params = []
    
    if updates.supplier is not None:
        update_fields.append("supplier = ?")
        params.append(updates.supplier)
    
    if updates.environment is not None:
        update_fields.append("environment = ?")
        params.append(updates.environment)
    
    if updates.auth_type is not None:
        update_fields.append("auth_type = ?")
        params.append(updates.auth_type)
    
    if updates.data is not None:
        update_fields.append("data = ?")
        params.append(json.dumps(updates.data))
    
    if updates.allow_self_rotation is not None:
        update_fields.append("allow_self_rotation = ?")
        params.append(updates.allow_self_rotation)
    
    if not update_fields:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Add updated_at
    update_fields.append("updated_at = ?")
    now = datetime.now().isoformat()
    params.append(now)
    params.append(credential_id)
    
    query = f"UPDATE credentials SET {', '.join(update_fields)} WHERE id = ?"
    
    try:
        cursor.execute(query, params)
        
        # Log audit
        log_audit(
            conn,
            credential_id,
            "update",
            user["email"],
            f"Updated credential {credential_id} via API"
        )
        
        conn.commit()
        
        # Fetch updated credential
        cursor.execute("SELECT * FROM credentials WHERE id = ?", (credential_id,))
        row = cursor.fetchone()
        
        return CredentialResponse(
            id=row["id"],
            supplier=row["supplier"],
            environment=row["environment"],
            auth_type=row["auth_type"],
            data=json.loads(row["data"]),
            created_by=row["created_by"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            allow_self_rotation=bool(row["allow_self_rotation"])
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.post(
    "/api/v1/credentials/{credential_id}/rotate",
    response_model=RotateResponse,
    tags=["Credentials"],
    summary="Rotate credential",
    description="Rotate a credential (generate new API key or password). Requires admin role or partner role with allow_self_rotation enabled."
)
async def rotate_credential(
    credential_id: int,
    user: dict = Depends(verify_api_key)
):
    """
    Rotate a credential by generating new authentication data.
    
    **Required Role:** admin or partner (if allow_self_rotation is true)
    
    **Behavior:**
    - API keys: Generates a new API key
    - Username/Password: Generates a new password
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if credential exists
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (credential_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Credential not found")
    
    # Check permissions
    if user["role"] == "admin":
        pass  # Admin can always rotate
    elif user["role"] == "partner" and row["allow_self_rotation"]:
        pass  # Partner can rotate if allowed
    else:
        conn.close()
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to rotate this credential"
        )
    
    # Simulate rotation
    old_data = json.loads(row["data"])
    new_data = simulate_credential_rotation(row["auth_type"], old_data)
    
    now = datetime.now().isoformat()
    
    try:
        cursor.execute("""
            UPDATE credentials
            SET data = ?, updated_at = ?
            WHERE id = ?
        """, (json.dumps(new_data), now, credential_id))
        
        # Log audit
        log_audit(
            conn,
            credential_id,
            "rotate",
            user["email"],
            f"Rotated credential {credential_id} via API"
        )
        
        conn.commit()
        
        return RotateResponse(
            id=credential_id,
            supplier=row["supplier"],
            environment=row["environment"],
            message="Credential rotated successfully",
            new_data=new_data,
            rotated_at=now
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.delete(
    "/api/v1/credentials/{credential_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Credentials"],
    summary="Delete credential",
    description="Delete a credential. Requires admin role."
)
async def delete_credential(
    credential_id: int,
    user: dict = Depends(verify_api_key)
):
    """
    Delete a credential.
    
    **Required Role:** admin
    """
    check_permission(user, "create")  # Using create permission as proxy for delete
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if credential exists
    cursor.execute("SELECT * FROM credentials WHERE id = ?", (credential_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Credential not found")
    
    try:
        # Log audit before deletion
        log_audit(
            conn,
            credential_id,
            "delete",
            user["email"],
            f"Deleted credential {credential_id} ({row['supplier']}) via API"
        )
        
        cursor.execute("DELETE FROM credentials WHERE id = ?", (credential_id,))
        conn.commit()
        
        return None
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@app.get(
    "/api/v1/audit-logs",
    response_model=List[AuditLogResponse],
    tags=["Audit"],
    summary="Get audit logs",
    description="Retrieve audit logs for all credential operations. Requires admin or devops role."
)
async def get_audit_logs(
    credential_id: Optional[int] = None,
    action: Optional[str] = None,
    limit: int = 100,
    user: dict = Depends(verify_api_key)
):
    """
    Get audit logs with optional filtering.
    
    **Required Role:** admin or devops
    
    **Query Parameters:**
    - credential_id: Filter by specific credential
    - action: Filter by action type (create, update, rotate, delete, view)
    - limit: Maximum number of logs to return (default: 100)
    """
    check_permission(user, "view_audit")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM audit_logs WHERE 1=1"
    params = []
    
    if credential_id:
        query += " AND cred_id = ?"
        params.append(credential_id)
    
    if action:
        query += " AND action = ?"
        params.append(action)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        logs.append(AuditLogResponse(
            id=row["id"],
            cred_id=row["cred_id"],
            action=row["action"],
            actor=row["actor"],
            details=row["details"],
            timestamp=row["timestamp"]
        ))
    
    return logs

# ==================== Run Server ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

