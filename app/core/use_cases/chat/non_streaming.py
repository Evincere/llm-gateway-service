from typing import List, Dict, Any, Optional
from app.core.ports.llm_service import LLMService
from app.core.ports.repositories import ModelExposureRepository, LogRepository
from app.core.domain.request_log import RequestLog
from uuid import UUID
import time

class ChatWithModelUseCase:
    """
    Use case for handling non-streaming chat requests.
    """
    def __init__(
        self, 
        llm_service: LLMService, 
        exposure_repo: ModelExposureRepository,
        log_repo: LogRepository
    ):
        self.llm_service = llm_service
        self.exposure_repo = exposure_repo
        self.log_repo = log_repo

    def execute(
        self, 
        project_id: UUID, 
        logical_model_name: str, 
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        # 1. Resolve logical to physical model
        exposure = self.exposure_repo.get_by_logical_name(project_id, logical_model_name)
        
        if exposure:
            physical_model = exposure.backend_model
            # Merge default config with requested overrides
            params = {**exposure.config, **kwargs}
        else:
            # Fallback or error? Specs say logical name is mapped. 
            # If not found, we could try to use it as is if allowed, 
            # but for now let's assume strict mapping.
            physical_model = logical_model_name
            params = kwargs

        # 2. Call LLM
        start_time = time.time()
        try:
            response = self.llm_service.chat(model=physical_model, messages=messages, **params)
            status_code = 200
        except Exception as e:
            # Handle backend errors
            status_code = 500
            raise e
        finally:
            latency = int((time.time() - start_time) * 1000)
            
            # 3. Log the request (Omit token counts for now if not easily available)
            log = RequestLog(
                project_id=project_id,
                model=physical_model,
                endpoint="/v1/chat",
                latency_ms=latency,
                status=status_code
            )
            self.log_repo.save(log)

        return response
