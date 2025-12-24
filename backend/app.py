#!/usr/bin/env python
"""
WanderFlow - AI Travel Planner Backend
Main application entry point

Usage:
    python app.py

Author: WanderFlow Team
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load .env file before importing settings
env_file = project_root / '.env'
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime
from app.core.db.session import init_db

# Setup logging
logs_dir = Path(__file__).parent / "logs"
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import settings
try:
    from app.core.config.settings import settings
    HAS_SETTINGS = True
    logger.info("[OK] Settings loaded successfully")
except ImportError as e:
    logger.warning(f"[WARN] Settings module not found: {e}")
    HAS_SETTINGS = False
    settings = None

# Create FastAPI application
app = FastAPI(
    title="WanderFlow API",
    description="AI Travel Planner Backend API Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
allowed_origins = ["*"]
if HAS_SETTINGS and hasattr(settings, "ALLOWED_ORIGINS") and settings.ALLOWED_ORIGINS:
    allowed_origins = settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS != ["*"] else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal server error",
            "detail": str(exc) if not HAS_SETTINGS or (settings and settings.DEBUG) else "Contact administrator"
        }
    )


# ===== Root and Health Routes =====

@app.get("/")
async def root():
    """Root path returns app info"""
    return {
        "name": "WanderFlow API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WanderFlow API",
        "version": "1.0.0"
    }


# ===== User Authentication Routes =====

try:
    from app.modules.users.api.v1 import router as users_router
    app.include_router(users_router, prefix="/api/v1/auth", tags=["auth"])
    logger.info("[OK] User authentication routes loaded")
    logger.info("  - POST /api/v1/auth/register")
    logger.info("  - POST /api/v1/auth/login")
    logger.info("  - GET /api/v1/auth/me")
    logger.info("  - PUT /api/v1/auth/me")
    logger.info("  - POST /api/v1/auth/change-password")
except Exception as e:
    logger.error(f"[ERROR] User auth routes failed: {e}")
    import traceback
    traceback.print_exc()


# ===== Planner Routes =====

try:
    @app.get("/api/v1/itineraries", tags=["planner"])
    async def get_itineraries():
        return {"message": "Get itineraries list - TODO"}

    @app.post("/api/v1/itineraries", tags=["planner"])
    async def create_itinerary():
        return {"message": "Create itinerary - TODO"}

    @app.get("/api/v1/itineraries/{itinerary_id}", tags=["planner"])
    async def get_itinerary(itinerary_id: int):
        return {"message": f"Get itinerary {itinerary_id} - TODO"}

    @app.post("/api/v1/itineraries/{itinerary_id}/generate", tags=["planner"])
    async def generate_itinerary(itinerary_id: int):
        return {"message": f"AI generate itinerary {itinerary_id} - TODO"}

    logger.info("[OK] Itinerary planner routes loaded")
except Exception as e:
    logger.warning(f"[WARN] Planner routes failed: {e}")


# ===== QA Chat Routes =====

try:
    # Test route without body
    @app.post("/api/v1/qa/test", tags=["qa"])
    async def test_qa():
        logger.info("Test QA endpoint called")
        return {"message": "Test successful"}

    # Simplified QA routes for testing
    @app.post("/api/v1/qa/sessions", tags=["qa"])
    async def create_session():
        logger.info("Create session called")
        return {"message": "Session created", "id": 1}

    @app.get("/api/v1/qa/sessions", tags=["qa"])
    async def get_sessions():
        return {"items": [], "total": 0}

    @app.post("/api/v1/qa/messages", tags=["qa"])
    async def send_message():
        logger.info("Send message called")
        return {"message": "Message received", "response": "Hello from QA!"}

    logger.info("[OK] QA chat routes loaded (simplified)")
    logger.info("  - POST /api/v1/qa/test")
    logger.info("  - POST /api/v1/qa/sessions")
    logger.info("  - GET /api/v1/qa/sessions")
    logger.info("  - POST /api/v1/qa/messages")
except Exception as e:
    logger.error(f"[WARN] QA routes failed: {e}")
    import traceback
    traceback.print_exc()


# ===== Copywriting Routes =====

try:
    @app.post("/api/v1/copywriting/generate", tags=["copywriting"])
    async def generate_copywriting():
        return {"message": "Generate copywriting - TODO"}

    @app.get("/api/v1/copywriting/results", tags=["copywriting"])
    async def get_copywriting_results():
        return {"message": "Get copywriting history - TODO"}

    logger.info("[OK] Copywriting routes loaded")
except Exception as e:
    logger.warning(f"[WARN] Copywriting routes failed: {e}")


# ===== Startup Event =====

@app.on_event("startup")
async def startup_event():
    """Execute on app startup"""
    logger.info("="*50)
    logger.info("WanderFlow API Starting...")
    logger.info("="*50)

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        import traceback
        traceback.print_exc()

    logger.info(f"Server: http://localhost:8000")
    logger.info(f"API Docs: http://localhost:8000/docs")
    logger.info(f"ReDoc: http://localhost:8000/redoc")
    logger.info(f"Health: http://localhost:8000/health")
    logger.info("="*50)


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on app shutdown"""
    logger.info("="*50)
    logger.info("WanderFlow API Shutdown")
    logger.info("="*50)


# ===== Main Function =====

if __name__ == "__main__":
    # Get port
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.warning("Invalid port, using default 8000")

    # Start application
    logger.info("="*50)
    logger.info("Starting WanderFlow Backend")
    logger.info("="*50)
    logger.info(f"Tip: Press Ctrl+C to stop")
    logger.info(f"URL: http://localhost:{port}")
    logger.info(f"Docs: http://localhost:{port}/docs")
    logger.info("="*50)

    # Run uvicorn - pass app instance directly without reload for stability
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload to avoid import string issues
        log_level="info"
    )
