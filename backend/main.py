from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create database tables if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",  # Replace with your frontend URL
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "FinCargo Backend is operational"}

@app.get("/api/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    summary = crud.get_dashboard_summary(db, user_id=1)
    return summary

@app.post("/api/goals", response_model=schemas.GoalResponse)
def create_goal_for_user(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    return crud.create_user_goal(db=db, goal=goal, user_id=1)

@app.post("/api/chat")
def handle_chat(message: dict):
    user_message = message.get("message", "").lower()
    if "score" in user_message:
        response = "You can improve your score by paying debts on time and increasing your savings rate."
    elif "save" in user_message:
        response = "A great way to save more is by setting clear goals and tracking your spending. Try adding a new goal!"
    else:
        response = "I am a prototype assistant. For more complex queries, please contact a financial advisor."
    return {"response": response}

@app.get("/api/report")
def generate_report(db: Session = Depends(get_db)):
    summary = crud.get_dashboard_summary(db, user_id=1)
    report_data = {
        "user_name": summary['user_name'],
        "financial_score": summary['financial_score'],
        "monthly_income": summary['monthly_income'],
        "total_assets": summary['total_assets'],
        "total_savings": summary['total_savings'],
        "outstanding_debts": summary['outstanding_debts'],
        "goals": summary['goals'],
        "net_worth": summary['total_assets'] - summary['outstanding_debts'],
        "debt_to_income_ratio": (summary['outstanding_debts'] / (summary['monthly_income'] * 12)) * 100 if summary['monthly_income'] > 0 else 0,
    }
    return report_data
