"""
WanderFlow AI Travel Assistant - FastAPI Application Entry Point

This is the main entry point for the WanderFlow backend application.
It sets up the FastAPI app, configures middleware, and registers all API routes.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.db.session import init_db
from app.modules.users.api.v1 import router as users_router
from app.modules.planner.api.v1 import router as planner_router
from app.modules.qa.api.v1 import router as qa_router
from app.modules.copywriter.api.v1 import router as copywriter_router

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
app.add_middleware(GZipMiddleware, minimum_size=1000)

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
    await init_db()
    logger.info("Database initialized successfully")


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
