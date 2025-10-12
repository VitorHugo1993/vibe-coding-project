#!/bin/bash
# Test script for Nezasa Connect API
# This script demonstrates common API operations for demo purposes

API_BASE="http://localhost:8000"
ADMIN_KEY="admin_key_123"
DEVOPS_KEY="devops_key_456"
PARTNER_KEY="partner_key_012"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Nezasa Connect API - Test Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to print section header
print_section() {
    echo ""
    echo -e "${YELLOW}>>> $1${NC}"
    echo ""
}

# Function to pause
pause() {
    echo ""
    read -p "Press Enter to continue..."
}

# Check if API is running
print_section "1. Health Check"
echo "GET /"
curl -s "${API_BASE}/" | python3 -m json.tool
pause

# List all credentials (as admin)
print_section "2. List All Credentials (Admin)"
echo "GET /api/v1/credentials"
curl -s -X GET "${API_BASE}/api/v1/credentials" \
  -H "X-API-Key: ${ADMIN_KEY}" | python3 -m json.tool
pause

# Get a specific credential
print_section "3. Get Specific Credential (ID: 1)"
echo "GET /api/v1/credentials/1"
curl -s -X GET "${API_BASE}/api/v1/credentials/1" \
  -H "X-API-Key: ${ADMIN_KEY}" | python3 -m json.tool
pause

# Create a new credential
print_section "4. Create New Credential (Admin)"
echo "POST /api/v1/credentials"
echo "Creating: Expedia API credential"
curl -s -X POST "${API_BASE}/api/v1/credentials" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${ADMIN_KEY}" \
  -d '{
    "supplier": "Expedia",
    "environment": "production",
    "auth_type": "api_key",
    "data": {
      "api_key": "expedia_prod_key_abc123xyz"
    },
    "allow_self_rotation": true
  }' | python3 -m json.tool
pause

# Update a credential
print_section "5. Update Credential (DevOps)"
echo "PUT /api/v1/credentials/1"
echo "Updating Sabre credential environment"
curl -s -X PUT "${API_BASE}/api/v1/credentials/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${DEVOPS_KEY}" \
  -d '{
    "environment": "production"
  }' | python3 -m json.tool
pause

# Rotate a credential
print_section "6. Rotate Credential (Admin)"
echo "POST /api/v1/credentials/1/rotate"
echo "Rotating Sabre credential"
curl -s -X POST "${API_BASE}/api/v1/credentials/1/rotate" \
  -H "X-API-Key: ${ADMIN_KEY}" | python3 -m json.tool
pause

# Get audit logs
print_section "7. Get Audit Logs (Admin)"
echo "GET /api/v1/audit-logs?limit=10"
curl -s -X GET "${API_BASE}/api/v1/audit-logs?limit=10" \
  -H "X-API-Key: ${ADMIN_KEY}" | python3 -m json.tool
pause

# Filter audit logs by action
print_section "8. Filter Audit Logs by Action (rotate)"
echo "GET /api/v1/audit-logs?action=rotate&limit=5"
curl -s -X GET "${API_BASE}/api/v1/audit-logs?action=rotate&limit=5" \
  -H "X-API-Key: ${ADMIN_KEY}" | python3 -m json.tool
pause

# Test permission error (partner trying to create)
print_section "9. Test Permission Denied (Partner tries to create)"
echo "POST /api/v1/credentials (with partner key)"
echo "This should fail with 403 Forbidden"
curl -s -X POST "${API_BASE}/api/v1/credentials" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${PARTNER_KEY}" \
  -d '{
    "supplier": "Test Supplier",
    "environment": "sandbox",
    "auth_type": "api_key",
    "data": {"api_key": "test_key"},
    "allow_self_rotation": false
  }' | python3 -m json.tool
pause

# List credentials (as partner - data should be masked)
print_section "10. List Credentials with Masked Data (Partner)"
echo "GET /api/v1/credentials (with partner key)"
echo "Data should be masked for non-admin roles"
curl -s -X GET "${API_BASE}/api/v1/credentials" \
  -H "X-API-Key: ${PARTNER_KEY}" | python3 -m json.tool
pause

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}API Test Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Check the Streamlit app's 'API Monitor' tab to see these requests logged!"
echo ""

