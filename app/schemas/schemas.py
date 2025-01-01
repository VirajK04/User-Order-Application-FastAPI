from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    user_id: int
    product_name: str
    quantity: int
    order_date: datetime

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int

    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None

    class Config:
        orm_mode = True