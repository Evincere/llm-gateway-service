from typing import Protocol, List, Optional
from uuid import UUID
from app.core.domain.project import Project
from app.core.domain.request_log import RequestLog
from app.core.domain.model_exposure import ModelExposure

class ProjectRepository(Protocol):
    """Interface for Project persistence."""
    
    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        ...
        
    def get_by_api_key(self, api_key: str) -> Optional[Project]:
        ...
        
    def save(self, project: Project) -> Project:
        ...

class LogRepository(Protocol):
    """Interface for RequestLog persistence."""
    
    def save(self, log: RequestLog) -> RequestLog:
        ...
        
    def get_by_project(self, project_id: UUID, limit: int = 100) -> List[RequestLog]:
        ...

class ModelExposureRepository(Protocol):
    """Interface for ModelExposure persistence."""
    
    def get_by_project(self, project_id: UUID) -> List[ModelExposure]:
        ...
        
    def get_by_logical_name(self, project_id: UUID, logical_name: str) -> Optional[ModelExposure]:
        ...
        
    def save(self, model_exposure: ModelExposure) -> ModelExposure:
        ...
