"""LLM Gateway Service - Main Application Entry Point"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.adapters.database import create_db_and_tables
from app.infrastructure.adapters.logging import configure_logging
from app.infrastructure.adapters.middleware import RequestLoggingMiddleware

# Configure Logging
configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    create_db_and_tables()
    yield

# Create FastAPI app instance
app = FastAPI(
    title="LLM Gateway Service",
    description="Multi-tenant gateway for OllamaFreeAPI models",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add Middleware
app.add_middleware(RequestLoggingMiddleware)

from app.entrypoints.api import chat_router, models_router

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router.router)
app.include_router(models_router.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "LLM Gateway Service",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LLM Gateway Service",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
