from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Order Schemas ---
class OrderBase(BaseModel):
    user_id: int
    product_name: str
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None

class Order(OrderBase):
    id: int
    order_date: datetime

    class Config:
        from_attributes = True

class UserWithOrders(User):
    orders: list[Order] = []