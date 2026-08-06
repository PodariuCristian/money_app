import Constants
from database.database import db

def seed_categories():
    income = ["Salary", "Investments", "Others"]
    fixed = Constants.fix_spendings
    utilities = Constants.utilities
    subscriptions = Constants.subscriptions
    expenses = Constants.categories
    data = []

    # Income
    for item in income:
        data.append(("Income", item))
    # Fixed
    for item in Constants.fix_spendings:
        data.append(("Fixed", item))
    # Utilities
    for item in Constants.utilities:
        data.append(("Utility", item))
    # Subscriptions
    for item in Constants.subscriptions:
        data.append(("Subscription", item))
    # General expenses
    for item in Constants.categories:
        data.append(("Expense", item))

    #db.executemany("""INSERT INTO categories(name,type) VALUES(?,?)""", data)
    db.executemany("""INSERT OR IGNORE INTO categories (section, name) VALUES (?, ?) """, data)

if __name__ == "__main__":
    seed_categories()