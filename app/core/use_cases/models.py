from typing import List, Dict, Any
from app.core.ports.llm_service import LLMService
from app.core.ports.repositories import ModelExposureRepository
from uuid import UUID

class ListAvailableModelsUseCase:
    """
    Use case for listing models available to a specific project.
    """
    def __init__(
        self, 
        llm_service: LLMService, 
        exposure_repo: ModelExposureRepository
    ):
        self.llm_service = llm_service
        self.exposure_repo = exposure_repo

    def execute(self, project_id: UUID) -> List[Dict[str, Any]]:
        # Get logical models defined for this project
        exposures = self.exposure_repo.get_by_project(project_id)
        
        # Optionally cross-reference with actual available models in backend
        # backend_models = self.llm_service.list_models()
        
        result = []
        for exp in exposures:
            result.append({
                "name": exp.logical_name,
                "backend_model": exp.backend_model,
                "config": exp.config
            })
            
        return result
