# models.py
from pydantic import BaseModel
from typing import List, Literal, Dict

class Income(BaseModel):
    amount: float
    frequency_days: int

class Expense(BaseModel):
    category: str
    amount: float
    frequency_days: int

class Transaction(BaseModel):
    date: str
    type: Literal['INCOME', 'EXPENSE', 'INVESTMENT']
    amount: float
    category: str
    description: str
    balance_after: float

class LifeEvent(BaseModel):
    date: str
    event_type: Literal['PROMOTION', 'MARKET_CRASH', 'UNEXPECTED_EXPENSE']
    description: str
    impact: Dict

class Persona(BaseModel):
    persona_id: str
    persona_name: str
    simulation_start_date: str
    initial_balance: float
    base_income: Income
    recurring_expenses: List[Expense]
    timeline: List[Transaction | LifeEvent]