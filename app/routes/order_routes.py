from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from app.models.models import Order
from app.schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

@router.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    db_order = Order(user_id=order.user_id, product_name=order.product_name, quantity=order.quantity)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.put("/orders/{order_id}", response_model=schemas.Order)
async def update_order(order_id: int, order: schemas.OrderUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalar_one_or_none()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id:
        db_order.user_id = order.user_id
    if order.product_name:
        db_order.product_name = order.product_name
    if order.quantity:
        db_order.quantity = order.quantity
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.delete(order)
    await db.commit()
    return {"message": "Order deleted successfully"}