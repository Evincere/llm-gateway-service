from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.core.domain.project import Project
from app.core.domain.request_log import RequestLog
from app.core.domain.model_exposure import ModelExposure
from app.core.ports.repositories import ProjectRepository, LogRepository, ModelExposureRepository

class SQLProjectRepository(ProjectRepository):
    def __init__(self, session: Session):
        self.session = session
        
    def get_by_id(self, project_id: UUID) -> Optional[Project]:
        return self.session.get(Project, project_id)
        
    def get_by_api_key(self, api_key: str) -> Optional[Project]:
        statement = select(Project).where(Project.api_key == api_key)
        return self.session.exec(statement).first()
        
    def save(self, project: Project) -> Project:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

class SQLLogRepository(LogRepository):
    def __init__(self, session: Session):
        self.session = session
        
    def save(self, log: RequestLog) -> RequestLog:
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log
        
    def get_by_project(self, project_id: UUID, limit: int = 100) -> List[RequestLog]:
        statement = select(RequestLog).where(RequestLog.project_id == project_id).limit(limit)
        return list(self.session.exec(statement).all())

class SQLModelExposureRepository(ModelExposureRepository):
    def __init__(self, session: Session):
        self.session = session
        
    def get_by_project(self, project_id: UUID) -> List[ModelExposure]:
        statement = select(ModelExposure).where(ModelExposure.project_id == project_id)
        return list(self.session.exec(statement).all())
        
    def get_by_logical_name(self, project_id: UUID, logical_name: str) -> Optional[ModelExposure]:
        statement = select(ModelExposure).where(
            ModelExposure.project_id == project_id,
            ModelExposure.logical_name == logical_name
        )
        return self.session.exec(statement).first()
        
    def save(self, model_exposure: ModelExposure) -> ModelExposure:
        self.session.add(model_exposure)
        self.session.commit()
        self.session.refresh(model_exposure)
        return model_exposure
