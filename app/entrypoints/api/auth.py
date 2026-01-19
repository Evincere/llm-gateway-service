from fastapi import Security, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from app.infrastructure.adapters.database import get_session
from app.infrastructure.adapters.sql_repositories import SQLProjectRepository
from app.core.domain.project import Project
from sqlmodel import Session

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_project_by_api_key(
    api_key: str = Security(api_key_header),
    session: Session = Depends(get_session)
) -> Project:
    """
    Dependency to validate API Key and return the associated Project.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )
    
    repo = SQLProjectRepository(session)
    project = repo.get_by_api_key(api_key)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    
    if not project.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project is inactive",
        )
        
    return project
