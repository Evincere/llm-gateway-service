import pytest
import os
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.adapters.database import get_session
from app.core.domain.project import Project

# Use in-memory SQLite for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="mock_project")
def mock_project_fixture(session: Session):
    project = Project(
        name="Test Project",
        api_key="test-api-key",
        is_active=True,
        allowed_models=["llama3"]
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
