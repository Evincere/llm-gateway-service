from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, JSON, Column


class ModelExposure(SQLModel, table=True):
    """
    Defines how a backend model is exposed to a specific project.
    Maps a logical name (e.g., 'law-assistant') to a backend model.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    project_id: UUID = Field(foreign_key="project.id", index=True)
    logical_name: str = Field(index=True)
    backend_model: str
    
    # config: JSON field for default parameters (temperature, max_tokens, etc.)
    config: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    def __repr__(self) -> str:
        return f"<ModelExposure logical={self.logical_name} backend={self.backend_model}>"
