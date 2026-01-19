from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, JSON, Column


class Project(SQLModel, table=True):
    """
    Project entity representing a client/tenant of the LLM Gateway.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    api_key: str = Field(index=True, unique=True)
    is_active: bool = Field(default=True)
    rate_limit_per_minute: Optional[int] = None
    
    # allowed_models: List of model names or logical identifiers
    allowed_models: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    def __repr__(self) -> str:
        return f"<Project name={self.name} active={self.is_active}>"
