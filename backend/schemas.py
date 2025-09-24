from pydantic import BaseModel
from typing import List

# --- Goal Schemas ---
class GoalBase(BaseModel):
    name: str
    category: str
    target_amount: float
    timeframe: str

class GoalCreate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: int
    current_amount: float
    owner_id: int

    class Config:
        orm_mode = True

# --- Dashboard Schemas ---
class DashboardSummary(BaseModel):
    user_name: str
    financial_score: int
    monthly_income: float
    total_assets: float
    total_savings: float
    outstanding_debts: float
    goals: List[GoalResponse]