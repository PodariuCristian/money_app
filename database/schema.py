from database.database import db

def create_tables():

    # Categories
    db.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section TEXT NOT NULL,
        name TEXT NOT NULL,
        UNIQUE(section, name)
        )
    """)

    # Monthly values (Income, Expenses, Fixed Costs, etc.)
    db.execute("""
    CREATE TABLE IF NOT EXISTS monthly_values(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY(category_id)
            REFERENCES categories(id),
        UNIQUE(category_id, year, month)
    )
    """)

    # Budgets
    db.execute("""
    CREATE TABLE IF NOT EXISTS budgets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        year INTEGER,
        month INTEGER,
        limit_amount REAL,
        FOREIGN KEY(category_id)
            REFERENCES categories(id)
    )
    """)

    # Settings
    db.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    

if __name__ == "__main__":
    create_tables()