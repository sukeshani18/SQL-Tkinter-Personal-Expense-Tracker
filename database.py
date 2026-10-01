import mysql.connector


# =========================
# DATABASE CONNECTION
# =========================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1995",
    database="expense_tracker"
)

cursor = connection.cursor()


# =========================
# ADD EXPENSE
# =========================

def add_expense(expense_date, category, description, amount):

    query = """
    INSERT INTO expenses
    (expense_date, category, description, amount)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (expense_date, category, description, amount)
    )

    connection.commit()


# =========================
# GET EXPENSES
# =========================

def get_expenses(selected_date):

    query = """
    SELECT id, expense_date, category, description, amount
    FROM expenses
    WHERE expense_date = %s
    ORDER BY id
    """

    cursor.execute(
        query,
        (selected_date,)
    )

    return cursor.fetchall()


# =========================
# GET DAILY TOTAL
# =========================

def get_daily_total(selected_date):

    query = """
    SELECT COALESCE(SUM(amount), 0)
    FROM expenses
    WHERE expense_date = %s
    """

    cursor.execute(
        query,
        (selected_date,)
    )

    return cursor.fetchone()[0]


# =========================
# UPDATE EXPENSE
# =========================

def update_expense(
    expense_id,
    expense_date,
    category,
    description,
    amount
):

    query = """
    UPDATE expenses
    SET expense_date = %s,
        category = %s,
        description = %s,
        amount = %s
    WHERE id = %s
    """

    cursor.execute(
        query,
        (
            expense_date,
            category,
            description,
            amount,
            expense_id
        )
    )

    connection.commit()


# =========================
# DELETE EXPENSE
# =========================

def delete_expense(expense_id):

    query = """
    DELETE FROM expenses
    WHERE id = %s
    """

    cursor.execute(
        query,
        (expense_id,)
    )

    connection.commit()

    return cursor.rowcount