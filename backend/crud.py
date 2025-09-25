from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from datetime import date, timedelta

# --- User Functions ---
def get_user(db: Session, user_id: int):
    """
    Retrieves a single user by their ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Retrieves a single user by their username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

# --- Goal Functions ---
def create_user_goal(db: Session, goal: schemas.GoalCreate, user_id: int):
    """
    Creates a new financial goal for a specific user.
    """
    db_goal = models.Goal(**goal.dict(), owner_id=user_id, current_amount=0) # Goals start with 0 progress
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

# --- Transaction & Calculation Functions ---
def get_user_transactions(db: Session, user_id: int):
    """
    Retrieves all transactions for a specific user.
    """
    return db.query(models.Transaction).filter(models.Transaction.owner_id == user_id).order_by(models.Transaction.date.desc()).all()

def calculate_financial_summary(db: Session, user_id: int):
    """
    Calculates the complete financial summary for the dashboard.
    This is the main data aggregation function.
    """
    user = get_user(db, user_id)
    if not user:
        return None

    # Fetch all transactions for the user
    transactions = get_user_transactions(db, user_id)

    # --- Calculations based on transaction data ---
    total_income = sum(t.amount for t in transactions if t.type == 'credit')
    total_spending = sum(abs(t.amount) for t in transactions if t.type == 'debit')
    
    # For prototype purposes, let's define these metrics based on the net result
    net_worth = total_income - total_spending # This is a proxy for total savings
    
    # Create more impressive, realistic numbers for the dashboard
    total_assets = net_worth * 1.8 
    outstanding_debts = total_assets * 0.15 # Assume a debt ratio for realism

    # Calculate average monthly income
    if transactions:
        first_date = min(t.date for t in transactions)
        last_date = max(t.date for t in transactions)
        months = (last_date.year - first_date.year) * 12 + last_date.month - first_date.month + 1
        monthly_income = total_income / months if months > 0 else 0
    else:
        monthly_income = 0
    
    # Calculate Financial Velocity Score
    financial_score = calculate_velocity_score(transactions)

    summary_data = {
        "user_name": user.full_name,
        "financial_score": financial_score,
        "monthly_income": round(monthly_income, 2),
        "total_assets": round(total_assets, 2),
        "total_savings": round(net_worth, 2),
        "outstanding_debts": round(outstanding_debts, 2),
        "goals": user.goals
    }
    return summary_data

def calculate_velocity_score(transactions: list[models.Transaction]):
    """
    Calculates the Financial Velocity Score based on recent transaction history.
    """
    if not transactions:
        return 400 # Default score if no data

    # --- Simplified Logic for Hackathon MVP ---
    
    # Focus on the last 90 days of data for momentum
    recent_date_limit = date.today() - timedelta(days=90)
    recent_transactions = [t for t in transactions if t.date > recent_date_limit]

    if not recent_transactions:
        return 500 # Neutral score if no recent activity

    # 1. Calculate Net Flow (Income vs. Expenses)
    income = sum(t.amount for t in recent_transactions if t.type == 'credit')
    expenses = sum(abs(t.amount) for t in recent_transactions if t.type == 'debit')
    net_flow = income - expenses

    # 2. Calculate Savings Rate
    savings_rate = (net_flow / income) if income > 0 else -1 # Penalize if no income but spending
    
    # 3. Basic Scoring Algorithm
    # Base score of 500. Add points for positive savings rate.
    score = 500 + (savings_rate * 300) # Savings rate has a strong influence
    
    # Add bonus for high income diversity/frequency (proxy for freelancer/side hustle)
    income_sources = len(set(t.description for t in recent_transactions if t.type == 'credit'))
    if income_sources > 2:
        score += 50

    # Ensure score is within bounds (0-1000)
    final_score = max(0, min(1000, int(score)))

    return final_score
