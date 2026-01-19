from app.infrastructure.adapters.database import engine, create_db_and_tables
from app.infrastructure.adapters.sql_repositories import SQLProjectRepository, SQLModelExposureRepository
from app.core.domain.project import Project
from app.core.domain.model_exposure import ModelExposure
from sqlmodel import Session
import secrets

def seed_data():
    """
    Seeds initial data: one project and one model exposure.
    """
    create_db_and_tables()
    
    with Session(engine) as session:
        project_repo = SQLProjectRepository(session)
        exposure_repo = SQLModelExposureRepository(session)
        
        # Check if we already have projects
        from sqlmodel import select
        existing = session.exec(select(Project)).first()
        if existing:
            print(f"Database already seeded. Project API Key: {existing.api_key}")
            return

        # Create a default project
        api_key = secrets.token_urlsafe(32)
        project = Project(
            name="Default Project",
            description="Initial project created during setup",
            api_key=api_key,
            allowed_models=["llama3"]
        )
        project_repo.save(project)
        
        # Create a default model mapping
        exposure = ModelExposure(
            project_id=project.id,
            logical_name="law-assistant",
            backend_model="llama3",
            config={"temperature": 0.2}
        )
        exposure_repo.save(exposure)
        
        print("Database seeded successfully!")
        print(f"Project ID: {project.id}")
        print(f"API Key: {api_key}")
        print(f"Mapped Model: 'law-assistant' -> 'llama3'")

if __name__ == "__main__":
    seed_data()
