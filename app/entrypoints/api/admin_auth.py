import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

ADMIN_API_KEY_NAME = "X-Admin-Key"
admin_key_header = APIKeyHeader(name=ADMIN_API_KEY_NAME, auto_error=False)

def validate_admin_key(
    admin_key: str = Security(admin_key_header)
) -> bool:
    """
    Dependency to validate the master Admin API Key from environment variables.
    """
    master_key = os.getenv("ADMIN_MASTER_KEY", "admin-secret-key") # Default for dev
    
    if not admin_key or admin_key != master_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Admin API Key",
        )
    
    return True
