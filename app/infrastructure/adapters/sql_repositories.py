from typing import List, Optional, Dict, Any
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

    def list_all(self) -> List[Project]:
        statement = select(Project)
        return list(self.session.exec(statement).all())

    def delete(self, project_id: UUID) -> bool:
        project = self.session.get(Project, project_id)
        if not project:
            return False
        self.session.delete(project)
        self.session.commit()
        return True

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

    def get_global_stats(self) -> Dict[str, Any]:
        from sqlalchemy import func
        
        # Total requests
        total_stmt = select(func.count(RequestLog.id))
        total = self.session.exec(total_stmt).one()
        
        # Avg latency
        avg_lat_stmt = select(func.avg(RequestLog.latency_ms))
        avg_latency = self.session.exec(avg_lat_stmt).one() or 0
        
        # Top models
        top_models_stmt = select(RequestLog.model, func.count(RequestLog.id)).group_by(RequestLog.model).order_by(func.count(RequestLog.id).desc()).limit(5)
        top_models = self.session.exec(top_models_stmt).all()
        
        # Projects activity
        top_projects_stmt = select(RequestLog.project_id, func.count(RequestLog.id)).group_by(RequestLog.project_id).order_by(func.count(RequestLog.id).desc()).limit(5)
        top_projects = self.session.exec(top_projects_stmt).all()
        
        return {
            "total_requests": total,
            "avg_latency_ms": round(float(avg_latency), 2),
            "top_models": [{"name": m, "count": c} for m, c in top_models],
            "top_projects": [{"id": str(p), "count": c} for p, c in top_projects]
        }

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
