"""
Database Session Management

This module manages database connections and session creation.
It uses SQLAlchemy's async capabilities for high performance.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings
from app.core.db.base import Base
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """
    Initialize database connection and create tables.
    This function should be called on application startup.
    """
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully")


async def get_db() -> AsyncSession:
    """
    Dependency function to get database session.
    Should be used as FastAPI dependency.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def close_db():
    """
    Close database connections.
    This function should be called on application shutdown.
    """
    await engine.dispose()
    logger.info("Database connections closed")
