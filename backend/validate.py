# backend/validate.py
import pandas as pd
from engine.velocity_engine import calculate_velocity_score

def run_final_validation():
    """
    Dynamically loads the demo data, finds all unique personas,
    and runs the engine for each one.
    """
    try:
        df = pd.read_csv("utils/datasets.csv")
        print("✅ Demo dataset loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: datasets.csv not found. Make sure it's in the backend/utils folder.")
        return

    # Dynamically find all unique personas in the file
    personas = df['persona_name'].unique()
    print(f"Found {len(personas)} unique personas for validation: {', '.join(personas)}\n")

    # Loop through each persona and calculate their score
    for person_name in personas:
        print(f"--- 🚀 Running Validation for: {person_name} ---")
        
        # Filter the dataframe for the current person's transactions
        person_transactions = df[df['persona_name'] == person_name].to_dict('records')

        if person_transactions:
            score_card = calculate_velocity_score(person_transactions)
            
            # Check if the engine returned a valid score or an error
            if 'error' in score_card:
                print(f"Could not calculate score: {score_card['error']}\n")
            else:
                print(f"  Calculated Score: {score_card['financial_velocity_score']}")
                print(f"  Breakdown: {score_card['breakdown']}\n")
        else:
            print(f"No transaction data found for {person_name}.\n")

if __name__ == "__main__":
    # --- This block is executed when you run 'python validate.py' ---
    print("Initializing Final Validation...")
    print("="*40)
    run_final_validation()
    print("="*40)
    print("Validation Complete.")