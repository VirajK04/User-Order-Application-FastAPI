# app/database/db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/fastapi"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing!")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,                  # Set to True for debugging SQL queries, False for production speed
    pool_size=20,                # Number of connections kept open persistently
    max_overflow=10,             # Max extra connections allowed during traffic spikes
    pool_timeout=30,             # Seconds to wait for an available connection before failing
    pool_recycle=1800,           # Recycle connections after 30 minutes to prevent stale DB drops
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False
)

async def get_db():
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()