# backend/validate.py
import pandas as pd
from engine.velocity_engine import calculate_velocity_score

# --- This is where we will add our classifier later for a deeper check ---
# from engine.transaction_classifier import classify_transaction

def run_validation():
    """
    Loads the demo data and runs it through our engine
    to validate the output for our two personas.
    """
    try:
        # We need to specify the correct path from the backend folder
        df = pd.read_csv("utils/demo_data.csv")
    except FileNotFoundError:
        print("Error: demo_data.csv not found. Make sure it's in the backend/utils folder.")
        return

    # Separate the data for each persona
    priya_transactions = df[df['persona_name'] == 'Priya Sharma'].to_dict('records')
    rohan_transactions = df[df['persona_name'] == 'Rohan Verma'].to_dict('records')

    print("--- Running Validation for Priya Sharma (Freelancer) ---")
    if priya_transactions:
        priya_score_card = calculate_velocity_score(priya_transactions)
        print(f"Calculated Score: {priya_score_card['financial_velocity_score']}")
        print(f"Breakdown: {priya_score_card['breakdown']}\n")
    else:
        print("No data found for Priya Sharma.\n")

    print("--- Running Validation for Rohan Verma (Salaried) ---")
    if rohan_transactions:
        rohan_score_card = calculate_velocity_score(rohan_transactions)
        print(f"Calculated Score: {rohan_score_card['financial_velocity_score']}")
        print(f"Breakdown: {rohan_score_card['breakdown']}\n")
    else:
        print("No data found for Rohan Verma.\n")

if __name__ == "__main__":
    run_validation()