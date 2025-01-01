from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/fastapi"

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an asynchronous sessionmaker
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get the DB session
async def get_db():
    async with AsyncSessionLocal() as db:  # Ensures session is closed automatically
        yield db  # Yield the session for use in the route