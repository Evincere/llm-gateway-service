from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class RequestLog(SQLModel, table=True):
    """
    Entity for logging every request made through the gateway.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    project_id: UUID = Field(foreign_key="project.id", index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    model: str = Field(index=True)  # Physical model name (e.g., llama3.3:70b)
    endpoint: str  # e.g., /v1/chat
    latency_ms: int
    status: int  # HTTP status code
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    
    def __repr__(self) -> str:
        return f"<RequestLog project={self.project_id} model={self.model} status={self.status}>"
