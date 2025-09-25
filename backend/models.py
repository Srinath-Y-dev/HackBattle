from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    goals = relationship("Goal", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner") # Add this relationship

class Goal(Base):
    __tablename__ = "goals"
    # ... (no changes here)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float, default=0.0)
    timeframe = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="goals")

# --- NEW MODEL TO ADD ---
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    date = Column(Date)
    persona_name = Column(String)
    description = Column(String)
    category = Column(String)
    type = Column(String)
    amount = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")
