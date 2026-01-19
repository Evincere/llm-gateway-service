import pytest
from sqlmodel import Session
from uuid import uuid4
from app.infrastructure.adapters.sql_repositories import SQLProjectRepository, SQLModelExposureRepository
from app.core.domain.project import Project
from app.core.domain.model_exposure import ModelExposure

def test_project_repository_save_and_get(session: Session):
    repo = SQLProjectRepository(session)
    project = Project(
        name="Internal App",
        api_key="secret-key",
        allowed_models=["gpt-4"]
    )
    
    saved = repo.save(project)
    retrieved = repo.get_by_id(saved.id)
    retrieved_by_key = repo.get_by_api_key("secret-key")
    
    assert retrieved.name == "Internal App"
    assert retrieved_by_key.id == saved.id

def test_model_exposure_repository(session: Session, mock_project: Project):
    repo = SQLModelExposureRepository(session)
    exposure = ModelExposure(
        project_id=mock_project.id,
        logical_name="assistant",
        backend_model="llama2",
        config={"temp": 0.5}
    )
    
    repo.save(exposure)
    all_exp = repo.get_by_project(mock_project.id)
    one_exp = repo.get_by_logical_name(mock_project.id, "assistant")
    
    assert len(all_exp) == 1
    assert one_exp.backend_model == "llama2"
