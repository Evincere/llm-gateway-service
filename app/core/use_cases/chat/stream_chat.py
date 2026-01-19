from typing import List, Dict, Any, Generator
from app.core.ports.llm_service import LLMService
from app.core.ports.repositories import ModelExposureRepository, LogRepository
from app.core.domain.request_log import RequestLog
from uuid import UUID
import time
import json

class StreamChatWithModelUseCase:
    """
    Use case for handling streaming chat requests.
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
    ) -> Generator[str, None, None]:
        # 1. Resolve logical to physical model
        exposure = self.exposure_repo.get_by_logical_name(project_id, logical_model_name)
        
        if exposure:
            physical_model = exposure.backend_model
            params = {**exposure.config, **kwargs}
        else:
            physical_model = logical_model_name
            params = kwargs

        # 2. Call LLM Streaming
        start_time = time.time()
        
        def generate():
            try:
                for chunk in self.llm_service.stream_chat(model=physical_model, messages=messages, **params):
                    # Format as SSE
                    yield f"data: {json.dumps(chunk)}\n\n"
                
                status_code = 200
            except Exception as e:
                status_code = 500
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            finally:
                latency = int((time.time() - start_time) * 1000)
                # Log at the end of stream
                log = RequestLog(
                    project_id=project_id,
                    model=physical_model,
                    endpoint="/v1/chat/stream",
                    latency_ms=latency,
                    status=status_code if 'status_code' in locals() else 500
                )
                self.log_repo.save(log)
                yield "data: [DONE]\n\n"

        return generate()
