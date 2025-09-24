from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create the tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if user already exists
user = db.query(models.User).filter(models.User.id == 1).first()

if not user:
    # Create a sample user
    db_user = models.User(id=1, username="alex", full_name="Alex")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"User '{db_user.full_name}' created.")

    # Create some initial goals for the user
    goals_to_add = [
        models.Goal(name="Build a House", category="🏠 Housing", target_amount=50000, current_amount=32500, timeframe="5 years", owner_id=1),
        models.Goal(name="New Car Fund", category="🚗 Transportation", target_amount=20000, current_amount=8000, timeframe="2 years", owner_id=1),
        models.Goal(name="Education Fund", category="🎓 Education", target_amount=15000, current_amount=12000, timeframe="3 years", owner_id=1),
    ]
    db.add_all(goals_to_add)
    db.commit()
    print(f"{len(goals_to_add)} initial goals created.")

else:
    print(f"User '{user.full_name}' already exists. No new data added.")

db.close()