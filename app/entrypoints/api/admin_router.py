from fastapi import APIRouter, Depends
from app.entrypoints.api.admin_auth import validate_admin_key
from app.core.use_cases.admin.get_stats import GetSystemStatsUseCase
from app.infrastructure.adapters.sql_repositories import SQLLogRepository
from app.infrastructure.adapters.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(validate_admin_key)])

@router.get("/stats")
async def get_stats(session: Session = Depends(get_session)):
    """
    Global usage statistics for the LLM Gateway.
    """
    log_repo = SQLLogRepository(session)
    use_case = GetSystemStatsUseCase(log_repo)
    
    return use_case.execute()

from app.core.use_cases.admin.manage_projects import ProjectManagementUseCase
from app.infrastructure.adapters.sql_repositories import SQLProjectRepository
from pydantic import BaseModel
from typing import List, Optional

class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    allowed_models: List[str] = []

@router.get("/projects")
async def list_projects(session: Session = Depends(get_session)):
    repo = SQLProjectRepository(session)
    use_case = ProjectManagementUseCase(repo)
    return use_case.list_projects()

@router.post("/projects")
async def create_project(request: CreateProjectRequest, session: Session = Depends(get_session)):
    repo = SQLProjectRepository(session)
    use_case = ProjectManagementUseCase(repo)
    return use_case.create_project(
        name=request.name,
        description=request.description,
        allowed_models=request.allowed_models
    )

@router.patch("/projects/{project_id}/toggle")
async def toggle_project(project_id: str, session: Session = Depends(get_session)):
    from uuid import UUID
    repo = SQLProjectRepository(session)
    use_case = ProjectManagementUseCase(repo)
    project = use_case.toggle_project_status(UUID(project_id))
    if not project:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Project not found")
    return project
