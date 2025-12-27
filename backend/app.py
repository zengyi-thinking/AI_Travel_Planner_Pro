#!/usr/bin/env python
"""
WanderFlow - AI Travel Planner Backend
Full backend entry point

Usage:
    python app.py
"""

import os
import sys
import logging
from pathlib import Path
import uvicorn

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load .env file before importing settings
env_file = project_root / ".env"
if env_file.exists():
    with env_file.open("r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    from app.main import app as main_app
except Exception as exc:
    logger.exception("Failed to import full backend app: %s", exc)
    raise

try:
    from app.core.config import settings
    default_port = settings.PORT
except Exception:
    default_port = 8000


if __name__ == "__main__":
    port = default_port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.warning("Invalid port arg, using default %s", default_port)

    logger.info("Starting full WanderFlow backend via app.main")
    uvicorn.run(
        main_app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
