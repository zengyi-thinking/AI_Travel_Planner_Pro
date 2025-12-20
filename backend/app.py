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

# Import settings
try:
    from app.core.config import settings
    HAS_SETTINGS = True
    print("[OK] Settings loaded successfully")
except ImportError as e:
    print(f"[WARN] Settings module not found: {e}")
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
    print("[OK] User authentication routes loaded")
    print(f"  - POST /api/v1/auth/register")
    print(f"  - POST /api/v1/auth/login")
    print(f"  - GET /api/v1/auth/me")
    print(f"  - PUT /api/v1/auth/me")
    print(f"  - POST /api/v1/auth/change-password")
except Exception as e:
    print(f"[ERROR] User auth routes failed: {e}")
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
    
    print("[OK] Itinerary planner routes loaded")
except Exception as e:
    print(f"[WARN] Planner routes failed: {e}")


# ===== QA Chat Routes =====

try:
    @app.post("/api/v1/qa/chat", tags=["qa"])
    async def chat():
        return {"message": "Chat endpoint - TODO"}
    
    @app.get("/api/v1/qa/sessions", tags=["qa"])
    async def get_sessions():
        return {"message": "Get chat sessions - TODO"}
    
    @app.post("/api/v1/qa/sessions", tags=["qa"])
    async def create_session():
        return {"message": "Create new session - TODO"}
    
    print("[OK] QA chat routes loaded")
except Exception as e:
    print(f"[WARN] QA routes failed: {e}")


# ===== Copywriting Routes =====

try:
    @app.post("/api/v1/copywriting/generate", tags=["copywriting"])
    async def generate_copywriting():
        return {"message": "Generate copywriting - TODO"}
    
    @app.get("/api/v1/copywriting/results", tags=["copywriting"])
    async def get_copywriting_results():
        return {"message": "Get copywriting history - TODO"}
    
    print("[OK] Copywriting routes loaded")
except Exception as e:
    print(f"[WARN] Copywriting routes failed: {e}")


# ===== Startup Event =====

@app.on_event("startup")
async def startup_event():
    """Execute on app startup"""
    print("\n" + "="*50)
    print("WanderFlow API Starting...")
    print("="*50)
    print(f"Server: http://localhost:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"ReDoc: http://localhost:8000/redoc")
    print(f"Health: http://localhost:8000/health")
    print("="*50 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on app shutdown"""
    print("\n" + "="*50)
    print("WanderFlow API Shutdown")
    print("="*50 + "\n")


# ===== Main Function =====

if __name__ == "__main__":
    # Get port
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port, using default 8000")
    
    # Start application
    print("\n" + "="*50)
    print("Starting WanderFlow Backend")
    print("="*50)
    print(f"Tip: Press Ctrl+C to stop")
    print(f"URL: http://localhost:{port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("="*50 + "\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
