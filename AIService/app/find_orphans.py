import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row


def check(query, title):
    print(f"\n========== {title} ==========")

    rows = connection.execute(query).fetchall()

    if not rows:
        print("✅ No broken relationships")
    else:
        for row in rows:
            print(dict(row))


# Invoices → Emails
check(
    """
    SELECT i.invoice_id, i.email_id
    FROM invoices i
    LEFT JOIN emails e
        ON i.email_id = e.email_id
    WHERE e.email_id IS NULL
    """,
    "Invoices → Emails"
)


# Tasks → Emails
check(
    """
    SELECT t.task_id, t.email_id
    FROM tasks t
    LEFT JOIN emails e
        ON t.email_id = e.email_id
    WHERE e.email_id IS NULL
    """,
    "Tasks → Emails"
)


# Tasks → Invoices
check(
    """
    SELECT t.task_id, t.invoice_id
    FROM tasks t
    LEFT JOIN invoices i
        ON t.invoice_id = i.invoice_id
    WHERE t.invoice_id IS NOT NULL
      AND i.invoice_id IS NULL
    """,
    "Tasks → Invoices"
)


# Disputes → Emails
check(
    """
    SELECT d.dispute_id, d.email_id
    FROM disputes d
    LEFT JOIN emails e
        ON d.email_id = e.email_id
    WHERE e.email_id IS NULL
    """,
    "Disputes → Emails"
)


# Disputes → Invoices
check(
    """
    SELECT d.dispute_id, d.invoice_id
    FROM disputes d
    LEFT JOIN invoices i
        ON d.invoice_id = i.invoice_id
    WHERE d.invoice_id IS NOT NULL
      AND i.invoice_id IS NULL
    """,
    "Disputes → Invoices"
)


# Audit Logs → Emails
check(
    """
    SELECT a.audit_id, a.email_id
    FROM audit_logs a
    LEFT JOIN emails e
        ON a.email_id = e.email_id
    WHERE a.email_id IS NOT NULL
      AND e.email_id IS NULL
    """,
    "Audit Logs → Emails"
)


connection.close()