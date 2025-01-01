from app.database.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

async def create_tables(db: AsyncSession = Depends(get_db)):
    await db.execute(
        text("""
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    )
    await db.execute(
        text("""
        CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        product_name VARCHAR(255) NOT NULL,
        quantity INT CHECK (quantity > 0),
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    )
    await db.commit()
    return {"Tables":"Created"}