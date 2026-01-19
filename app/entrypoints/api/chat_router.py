from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from app.core.domain.project import Project
from app.entrypoints.api.auth import get_project_by_api_key
from app.core.use_cases.chat import ChatWithModelUseCase
from app.infrastructure.adapters.ollama_adapter import OllamaFreeAPIAdapter
from app.infrastructure.adapters.sql_repositories import SQLModelExposureRepository, SQLLogRepository
from app.infrastructure.adapters.database import get_session
from pydantic import BaseModel
from sqlmodel import Session
from fastapi.responses import StreamingResponse
from app.core.use_cases.chat.stream_chat import StreamChatWithModelUseCase

router = APIRouter(prefix="/v1/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

@router.post("")
async def chat(
    request: ChatRequest,
    project: Project = Depends(get_project_by_api_key),
    session: Session = Depends(get_session)
):
    """
    Unified chat endpoint (non-streaming).
    """
    # Dependencies injection (manual for now, could use a container)
    llm_service = OllamaFreeAPIAdapter()
    exposure_repo = SQLModelExposureRepository(session)
    log_repo = SQLLogRepository(session)
    
    use_case = ChatWithModelUseCase(llm_service, exposure_repo, log_repo)
    
    # Prepare optional params
    params = {}
    if request.temperature is not None:
        params["temperature"] = request.temperature
    if request.max_tokens is not None:
        params["max_tokens"] = request.max_tokens

    try:
        response = use_case.execute(
            project_id=project.id,
            logical_model_name=request.model,
            messages=request.messages,
            **params
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    project: Project = Depends(get_project_by_api_key),
    session: Session = Depends(get_session)
):
    """
    Unified chat endpoint (streaming via SSE).
    """
    llm_service = OllamaFreeAPIAdapter()
    exposure_repo = SQLModelExposureRepository(session)
    log_repo = SQLLogRepository(session)
    
    use_case = StreamChatWithModelUseCase(llm_service, exposure_repo, log_repo)
    
    params = {}
    if request.temperature is not None:
        params["temperature"] = request.temperature
    if request.max_tokens is not None:
        params["max_tokens"] = request.max_tokens

    try:
        generator = use_case.execute(
            project_id=project.id,
            logical_model_name=request.model,
            messages=request.messages,
            **params
        )
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
