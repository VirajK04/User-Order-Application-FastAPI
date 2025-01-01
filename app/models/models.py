from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint
from datetime import datetime
from sqlalchemy.orm import relationship


Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to orders
    orders = relationship("Order", back_populates="user", cascade="all, delete")

# Order Model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_name = Column(String(255), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)

    # Add a constraint to ensure quantity is greater than 0
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
    )

    # Relationship to user
    user = relationship("User", back_populates="orders")