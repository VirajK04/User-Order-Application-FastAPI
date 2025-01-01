from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from app.models.models import User
from app.schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    result =await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email

    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}