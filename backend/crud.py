from sqlalchemy.orm import Session
from . import models, schemas

# For simplicity, we'll work with a single user (id=1)
def get_user(db: Session, user_id: int = 1):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user_goal(db: Session, goal: schemas.GoalCreate, user_id: int = 1):
    db_goal = models.Goal(**goal.dict(), owner_id=user_id, current_amount=0) # Start with 0 progress
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_dashboard_summary(db: Session, user_id: int = 1):
    user = get_user(db)
    # In a real app, these values would be calculated from transactions
    # For this prototype, we'll use impressive-looking static values
    summary_data = {
        "user_name": user.full_name,
        "financial_score": 750,
        "monthly_income": 8500.00,
        "total_assets": 285000.00,
        "total_savings": 45000.00,
        "outstanding_debts": 12000.00,
        "goals": user.goals
    }
    return summary_data