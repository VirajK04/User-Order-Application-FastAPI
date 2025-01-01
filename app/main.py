from fastapi import FastAPI

from app.routes import user_routes, order_routes

from app.routes.tables import create_tables

from app.database.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    db_generator = get_db()  # Create the async generator
    db: AsyncSession = await anext(db_generator)  # Get the first value from the generator
    try:
        await create_tables(db)  # Pass the session to your function
    finally:
        await db.close()  # Ensure the session is closed

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

app.include_router(user_routes.router)
app.include_router(order_routes.router)