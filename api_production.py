# Production API with PostgreSQL support
import os
import sqlite3
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, Header, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import hashlib
import uuid

# Import the original API
from api import *

# Override database configuration for production
def get_production_db():
    """Get production database connection"""
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Use PostgreSQL in production
        import psycopg2
        return psycopg2.connect(database_url)
    else:
        # Fallback to SQLite
        return sqlite3.connect("credentials.db")

# Override the database connection in the original API
import api
api.get_db = get_production_db

# Create production app
app = FastAPI(
    title="Nezasa Connect API - Credential Management (Production)",
    description="Self-service API credential management system",
    version="1.0.0"
)

# Add CORS middleware for Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit Cloud domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Copy all routes from original API
from api import (
    VALID_API_KEYS, CredentialCreate, CredentialUpdate, 
    CredentialResponse, AuditLogResponse, get_api_key_role,
    create_credential, get_credentials, get_credential, 
    update_credential, delete_credential, rotate_credential, 
    get_audit_logs
)

# Add all the routes
app.get("/")(lambda: {"status": "online", "service": "Nezasa Connect API - Credential Management", "version": "1.0.0", "docs": "/api/docs"})
app.post("/api/v1/credentials", response_model=CredentialResponse)(create_credential)
app.get("/api/v1/credentials", response_model=List[CredentialResponse])(get_credentials)
app.get("/api/v1/credentials/{credential_id}", response_model=CredentialResponse)(get_credential)
app.put("/api/v1/credentials/{credential_id}", response_model=CredentialResponse)(update_credential)
app.delete("/api/v1/credentials/{credential_id}")(delete_credential)
app.post("/api/v1/credentials/{credential_id}/rotate", response_model=CredentialResponse)(rotate_credential)
app.get("/api/v1/audit-logs", response_model=List[AuditLogResponse])(get_audit_logs)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
