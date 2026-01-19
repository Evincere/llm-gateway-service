from fastapi import APIRouter, Depends
from app.core.domain.project import Project
from app.entrypoints.api.auth import get_project_by_api_key
from app.core.use_cases.models import ListAvailableModelsUseCase
from app.infrastructure.adapters.ollama_adapter import OllamaFreeAPIAdapter
from app.infrastructure.adapters.sql_repositories import SQLModelExposureRepository
from app.infrastructure.adapters.database import get_session
from sqlmodel import Session

router = APIRouter(prefix="/v1/models", tags=["Models"])

@router.get("")
async def list_models(
    project: Project = Depends(get_project_by_api_key),
    session: Session = Depends(get_session)
):
    """
    Returns models available to the project.
    """
    llm_service = OllamaFreeAPIAdapter()
    exposure_repo = SQLModelExposureRepository(session)
    
    use_case = ListAvailableModelsUseCase(llm_service, exposure_repo)
    
    models = use_case.execute(project.id)
    return {"data": models}
