# backend/engine/velocity_engine.py
import pandas as pd
from datetime import datetime
from scipy.special import expit
from engine.transaction_classifier import classify_transaction # Make sure this import is here

# --- UTILITY: NORMALIZATION ---
def normalize_score(value, k=0.1):
    return expit(value * k)

# --- COMPONENT 1: INCOME MOMENTUM ---
def calculate_income_momentum(transactions_df):
    income_df = transactions_df[transactions_df['amount'] < 0].copy()
    if income_df.empty: return 0.3
    income_df['month'] = income_df['date'].dt.to_period('M')
    monthly_income = income_df.groupby('month')['amount'].sum().abs()
    if len(monthly_income) < 2: return 0.5
    last_month, prev_month = monthly_income.iloc[-1], monthly_income.iloc[-2]
    if prev_month == 0: return 0.9
    percent_change = ((last_month - prev_month) / prev_month) * 100
    return normalize_score(percent_change, k=0.05)

# --- COMPONENT 2: SPENDING HYGIENE (UPGRADED WITH AI) ---
def calculate_spending_hygiene(transactions_df):
    spending_df = transactions_df[transactions_df['amount'] > 0].copy()
    if spending_df.empty: return 0.5
    spending_df['smart_category'] = spending_df['description'].apply(classify_transaction)
    discretionary_spending = spending_df[spending_df['smart_category'] == 'Discretionary Spending']['amount'].sum()
    total_spending = spending_df['amount'].sum()
    if total_spending == 0: return 0.8
    discretionary_ratio = discretionary_spending / total_spending
    return 1.0 - discretionary_ratio

# --- MAIN ENGINE FUNCTION ---
def calculate_velocity_score(transactions: list) -> dict:
    if not transactions: return {"error": "No transactions provided"}
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])

    income_score = calculate_income_momentum(df)
    spending_score = calculate_spending_hygiene(df)
    
    asset_score = 0.7 
    debt_score = 0.4  

    velocity_score = (income_score * 0.4) + (spending_score * 0.3) + (asset_score * 0.2) - (debt_score * 0.1)
    velocity_score = max(0, min(1, velocity_score))

    return {
        "financial_velocity_score": round(velocity_score, 2),
        "breakdown": {
            "income_momentum": round(income_score, 2),
            "spending_hygiene": round(spending_score, 2),
            "asset_growth": asset_score,
            "debt_pressure": debt_score
        },
        "narrative": "Engine v1.0: Your financial vitals are looking stable."
    }