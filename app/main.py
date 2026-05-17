from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.db import engine

from app.models.models import Base

from app.routes import user_routes, order_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting: Initializing database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield 
    
    print("Application shutting down: Disposing database engine...")
    await engine.dispose()

app = FastAPI(
    title="User-Order Async API",
    description="High-performance async backend for users and orders",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_routes.router, prefix="/api", tags=["Users"])
app.include_router(order_routes.router, prefix="/api", tags=["Orders"])

# Optional root endpoint for a quick health check
@app.get("/")
async def root():
    return {"message": "API is online and running asynchronously!"}