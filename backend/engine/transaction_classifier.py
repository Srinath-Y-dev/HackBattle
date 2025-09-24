# backend/engine/transaction_classifier.py
from transformers import pipeline

# IMPORTANT: We load the model once when the application starts.
# This prevents reloading the 1.6GB model on every API call.
print("Loading Zero-Shot Classification model...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print("Model loaded successfully.")

# These are our custom, intelligent categories.
SMART_CATEGORIES = [
    "Wealth Building",       # Investments, savings, education
    "Essential Spending",    # Rent, groceries, utilities
    "Discretionary Spending",# Restaurants, shopping, entertainment
    "Income",                # Salary, freelance payments
    "Debt Repayment",        # Loan or credit card payments
    "Business Expense",      # Work-related software or purchases
]

def classify_transaction(description: str) -> str:
    """
    Takes a raw transaction description and returns the most likely smart category.
    """
    if not description or not isinstance(description, str):
        return "Uncategorized"

    # The AI model does the work here.
    result = classifier(description, candidate_labels=SMART_CATEGORIES)

    # We return the label with the highest score.
    return result['labels'][0]