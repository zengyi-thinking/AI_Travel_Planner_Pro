"""
WanderFlow AI Travel Assistant - FastAPI Application Entry Point

This is the main entry point for WanderFlow backend application.
It sets up the FastAPI app, configures middleware, and registers all API routes.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os
import asyncio

from app.core.config import settings
from app.core.db.session import init_db
from app.modules.users.api.v1 import router as users_router
from app.modules.users.api.settings import router as users_settings_router
from app.modules.planner.api.v1 import router as planner_router
from app.modules.qa.api.v1 import router as qa_router
from app.modules.copywriter.api.v1 import router as copywriter_router
from app.modules.qa.rag.knowledge_base import get_knowledge_base

# 设置stdout和stderr的编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    force=True
)
logger = logging.getLogger(__name__)

# 配置SQLAlchemy的日志，避免编码问题
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.propagate = False
sqlalchemy_logger.addHandler(logging.StreamHandler(sys.stdout))

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered travel planning assistant",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered travel planning assistant",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting up WanderFlow backend...")
    
    # Import all models to register them with SQLAlchemy
    from app.core.db.base import import_all_models
    import_all_models()
    
    await init_db()
    logger.info("Database initialized successfully")

    prewarm_docs = [item.strip() for item in os.getenv("RAG_PREWARM_DOCS", "").split(",") if item.strip()]
    if prewarm_docs:
        kb = get_knowledge_base()
        asyncio.create_task(kb.prewarm_async(prewarm_docs))
        logger.info("RAG prewarm started for: %s", prewarm_docs)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to WanderFlow API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.APP_VERSION}


# Register API routers
app.include_router(
    users_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    users_settings_router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    planner_router,
    prefix="/api/v1/planner",
    tags=["Travel Planning"]
)

app.include_router(
    qa_router,
    prefix="/api/v1/qa",
    tags=["AI Assistant"]
)

app.include_router(
    copywriter_router,
    prefix="/api/v1/copywriter",
    tags=["Content Generation"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
