from database import get_connection
import sqlite3

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT email_id, COUNT(*)
    FROM emails
    GROUP BY email_id
    HAVING COUNT(*) > 1
""")

duplicates = cursor.fetchall()

for row in duplicates:
    print(row)

connection.close()

def show_data():

    connection = get_connection()

    print("\n========== EMAILS ==========")

    rows = connection.execute("""
        SELECT email_id, sender, subject
        FROM emails
        ORDER BY email_id
    """).fetchall()

    for row in rows:
        print(dict(row))

    print("\n========== INVOICES ==========")

    rows = connection.execute("""
        SELECT invoice_id, email_id, vendor, amount
        FROM invoices
        ORDER BY invoice_id
    """).fetchall()

    for row in rows:
        print(dict(row))

    connection.close()


