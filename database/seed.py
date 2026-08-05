import Constants
from database.database import db

def seed_categories():
    income = [
        "Salary",
        "Investments",
        "Others"
    ]
    fixed = Constants.fix_spendings
    utilities = Constants.utilities
    subscriptions = Constants.subscriptions
    expenses = Constants.categories
    data = []
    for item in income:
        data.append((item, "Income"))
    for item in fixed:
        data.append((item, "Fixed"))
    for item in utilities:
        data.append((item, "Utility"))
    for item in subscriptions:
        data.append((item, "Subscription"))
    for item in expenses:
        data.append((item, "Expense"))
    db.executemany("""
    INSERT OR IGNORE INTO categories(name,type)
    VALUES(?,?)
    """, data)

if __name__ == "__main__":
    seed_categories()