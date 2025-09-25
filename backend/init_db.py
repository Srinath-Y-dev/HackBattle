import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime

# This creates all tables (User, Goal, and now Transaction)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Create Personas as Users if they don't exist ---
personas = ["Priya Sharma", "Rohan Verma", "Anjali Mehta", "Vikram Singh", "Sunita Patel"]
user_map = {} # To hold the user IDs for each persona name

for idx, name in enumerate(personas, 1):
    user = db.query(models.User).filter(models.User.full_name == name).first()
    if not user:
        user = models.User(id=idx, username=name.lower().split()[0], full_name=name)
        db.add(user)
        print(f"User '{user.full_name}' created.")
    user_map[name] = user.id

db.commit()

# --- Import CSV Data ---
# Check if we have already imported transactions to avoid duplicates
transaction_count = db.query(models.Transaction).count()
if transaction_count == 0:
    print("No transactions found. Importing from datasets.csv...")
    try:
        # Assumes datasets.csv is in the same directory as this script for simplicity
        df = pd.read_csv("datasets.csv")

        for index, row in df.iterrows():
            transaction_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            
            # Find the owner_id from our user_map
            owner_id = user_map.get(row['persona_name'])

            if owner_id:
                transaction = models.Transaction(
                    transaction_id=row['transaction_id'],
                    date=transaction_date,
                    persona_name=row['persona_name'],
                    description=row['description'],
                    category=row['category'],
                    type=row['type'],
                    amount=row['amount'],
                    owner_id=owner_id
                )
                db.add(transaction)
        
        db.commit()
        print(f"Successfully imported {len(df)} transactions.")
    except FileNotFoundError:
        print("Error: datasets.csv not found. Please place it in the backend directory.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred during import: {e}")
else:
    print(f"Database already contains {transaction_count} transactions. Skipping import.")


db.close()
