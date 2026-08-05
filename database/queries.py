from database.database import db

###########################################################
# CATEGORY
###########################################################
def get_categories(category_type=None):
    if category_type is None:
        return db.fetchall("""
            SELECT *
            FROM categories
            ORDER BY name
        """)
    return db.fetchall("""
        SELECT *
        FROM categories
        WHERE type=?
        ORDER BY name
    """, (category_type,))

def get_category_id(name):
    row = db.fetchone("""
        SELECT id
        FROM categories
        WHERE name=?
    """, (name,))
    if row:
        return row["id"]
    return None

###########################################################
# TRANSACTIONS
###########################################################
def add_transaction(category, amount, date, notes=""):
    category_id = get_category_id(category)
    db.execute("""
        INSERT INTO transactions
        (category_id,amount,date,notes)
        VALUES(?,?,?,?)
    """,
    (category_id, amount, date, notes))

def update_transaction(transaction_id,
                       category,
                       amount,
                       date,
                       notes=""):
    category_id = get_category_id(category)
    db.execute("""
        UPDATE transactions
        SET
            category_id=?,
            amount=?,
            date=?,
            notes=?
        WHERE id=?
    """,
    (category_id,
     amount,
     date,
     notes,
     transaction_id))


def delete_transaction(transaction_id):
    db.execute("""
        DELETE FROM transactions
        WHERE id=?
    """,
    (transaction_id,))

###########################################################
# MONTHLY TOTALS
###########################################################
def monthly_income(year, month):
    row = db.fetchone("""
        SELECT
            COALESCE(SUM(amount),0) total
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type='Income'
        AND strftime('%Y',date)=?
        AND strftime('%m',date)=?
    """,
    (str(year), f"{month:02d}"))
    return row["total"]

def monthly_expenses(year, month):
    row = db.fetchone("""
        SELECT
            COALESCE(SUM(ABS(amount)),0) total
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type!='Income'
        AND strftime('%Y',date)=?
        AND strftime('%m',date)=?
    """,
    (str(year), f"{month:02d}"))
    return row["total"]

###########################################################
# YEAR TOTALS
###########################################################
def yearly_income(year):
    row = db.fetchone("""
        SELECT
            COALESCE(SUM(amount),0) total
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type='Income'
        AND strftime('%Y',date)=?
    """,
    (str(year),))
    return row["total"]

def yearly_expenses(year):
    row = db.fetchone("""
        SELECT
            COALESCE(SUM(ABS(amount)),0) total
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type!='Income'
        AND strftime('%Y',date)=?
    """,
    (str(year),))
    return row["total"]


###########################################################
# CHARTS
###########################################################
def expenses_by_category(year, month):
    return db.fetchall("""
        SELECT
            c.name,
            ABS(SUM(amount)) amount
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type!='Income'
        AND strftime('%Y',date)=?
        AND strftime('%m',date)=?
        GROUP BY c.name
        ORDER BY amount DESC
    """,
    (str(year),
     f"{month:02d}"))


def income_per_month(year):
    return db.fetchall("""
        SELECT
            strftime('%m',date) month,
            SUM(amount) amount
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type='Income'
        AND strftime('%Y',date)=?
        GROUP BY month
    """,
    (str(year),))

def expenses_per_month(year):
    return db.fetchall("""
        SELECT
            strftime('%m',date) month,
            ABS(SUM(amount)) amount
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            c.type!='Income'
        AND strftime('%Y',date)=?
        GROUP BY month
    """,
    (str(year),))

###########################################################
# TABLE DATA
###########################################################
def transactions_for_month(year, month):
    return db.fetchall("""
        SELECT
            t.id,
            c.name,
            c.type,
            t.amount,
            t.date,
            t.notes
        FROM transactions t
        JOIN categories c
        ON t.category_id=c.id
        WHERE
            strftime('%Y',date)=?
        AND strftime('%m',date)=?
        ORDER BY date
    """,
    (str(year),
     f"{month:02d}"))


###########################################################
# SAVE MONTLY VALUES
###########################################################
def save_monthly_value(category, year, month, amount):
    """
    Inserts or updates a monthly value for a category.
    """
    category_id = get_category_id(category)
    if category_id is None:
        raise ValueError(f"Unknown category: {category}")
    db.execute(
        """
        INSERT INTO monthly_values
            (category_id, year, month, amount)
        VALUES
            (?, ?, ?, ?)
        ON CONFLICT(category_id, year, month)
        DO UPDATE SET
            amount = excluded.amount
        """,
        (
            category_id,
            year,
            month,
            amount
        )
    )

def get_yearly_values(year, category_type="Income"):
    """
    Returns all monthly values for a given category type.
    """
    return db.fetchall(
        """
        SELECT
            c.name,
            mv.month,
            mv.amount
        FROM monthly_values mv
        JOIN categories c
            ON mv.category_id = c.id
        WHERE mv.year = ?
          AND c.type = ?
        ORDER BY c.name, mv.month
        """,
        (
            year,
            category_type
        )
    )

def load_monthly_values(year, category_type):
    """
    Returns all monthly values for a given category type.
    Example output:
    {
        "Salary": {1: 3500, 2: 3600},
        "Investments": {1: 100},
        "Others": {}
    }
    """
    rows = db.fetchall(
        """
        SELECT
            c.name,
            mv.month,
            mv.amount
        FROM monthly_values mv
        JOIN categories c
            ON mv.category_id = c.id
        WHERE mv.year = ?
          AND c.type = ?
        """,
        (year, category_type)
    )

    data = {}
    for row in rows:
        category = row["name"]
        month = row["month"]
        amount = row["amount"]
        if category not in data:
            data[category] = {}
        data[category][month] = amount
    return data