import os
from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

# We'll use SQLite for development if DATABASE_URL is not provided
# But use psycopg2-binary for prod as per specs
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./llm_gateway.db")

# For SQLModel sync usage (common with FastAPI dependencies)
engine = create_engine(DATABASE_URL, echo=True)

import time
from loguru import logger

def create_db_and_tables():
    """Initializes the database schema with retry logic."""
    # Import all models to ensure they are registered with SQLModel.metadata
    from app.core.domain.project import Project
    from app.core.domain.request_log import RequestLog
    from app.core.domain.model_exposure import ModelExposure
    
    max_retries = 10
    retry_delay = 5  # seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt}/{max_retries})...")
            SQLModel.metadata.create_all(engine)
            logger.success("Database connection established and tables created.")
            break
        except Exception as e:
            if attempt == max_retries:
                logger.error(f"Failed to connect to database after {max_retries} attempts.")
                raise e
            logger.warning(f"Database connection failed: {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)

def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions."""
    with Session(engine) as session:
        yield session
