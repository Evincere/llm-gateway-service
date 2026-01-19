from typing import List, Optional
from uuid import UUID
from app.core.ports.repositories import ProjectRepository
from app.core.domain.project import Project
import secrets

class ProjectManagementUseCase:
    """
    Use case for handling administrative CRUD operations on projects.
    """
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def list_projects(self) -> List[Project]:
        return self.project_repo.list_all()

    def create_project(self, name: str, description: Optional[str] = None, allowed_models: List[str] = []) -> Project:
        api_key = secrets.token_urlsafe(32)
        project = Project(
            name=name,
            description=description,
            api_key=api_key,
            allowed_models=allowed_models,
            is_active=True
        )
        return self.project_repo.save(project)

    def toggle_project_status(self, project_id: UUID) -> Optional[Project]:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            return None
        
        project.is_active = not project.is_active
        return self.project_repo.save(project)
