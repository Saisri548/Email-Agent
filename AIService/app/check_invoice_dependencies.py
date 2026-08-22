import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"


def check_dependencies():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    print("=" * 70)
    print("INVOICE DEPENDENCY CHECK")
    print("=" * 70)

    # -------------------------------------------------
    # 1. Tasks → Invoices
    # -------------------------------------------------
    print("\n========== TASKS → INVOICES ==========")

    cursor.execute("""
        SELECT
            t.task_id,
            t.email_id,
            t.invoice_id
        FROM tasks t
        LEFT JOIN invoices i
            ON t.invoice_id = i.invoice_id
        WHERE t.invoice_id IS NOT NULL
          AND i.invoice_id IS NULL
    """)

    broken_tasks = cursor.fetchall()

    if broken_tasks:
        print("❌ Missing invoice records referenced by tasks:")

        for row in broken_tasks:
            print(dict(row))
    else:
        print("✅ All task invoice references are valid.")

    # -------------------------------------------------
    # 2. Disputes → Invoices
    # -------------------------------------------------
    print("\n========== DISPUTES → INVOICES ==========")

    cursor.execute("""
        SELECT
            d.dispute_id,
            d.email_id,
            d.invoice_id
        FROM disputes d
        LEFT JOIN invoices i
            ON d.invoice_id = i.invoice_id
        WHERE d.invoice_id IS NOT NULL
          AND i.invoice_id IS NULL
    """)

    broken_disputes = cursor.fetchall()

    if broken_disputes:
        print("❌ Missing invoice records referenced by disputes:")

        for row in broken_disputes:
            print(dict(row))
    else:
        print("✅ All dispute invoice references are valid.")

    # -------------------------------------------------
    # 3. Invoices → Emails
    # -------------------------------------------------
    print("\n========== INVOICES → EMAILS ==========")

    cursor.execute("""
        SELECT
            i.invoice_id,
            i.email_id
        FROM invoices i
        LEFT JOIN emails e
            ON i.email_id = e.email_id
        WHERE i.email_id IS NOT NULL
          AND e.email_id IS NULL
    """)

    broken_invoice_emails = cursor.fetchall()

    if broken_invoice_emails:
        print("❌ Missing emails referenced by invoices:")

        for row in broken_invoice_emails:
            print(dict(row))
    else:
        print("✅ All invoice email references are valid.")

    # -------------------------------------------------
    # 4. Summary of existing invoices
    # -------------------------------------------------
    print("\n========== EXISTING INVOICES ==========")

    cursor.execute("""
        SELECT
            invoice_id,
            email_id,
            vendor,
            amount,
            currency,
            status
        FROM invoices
        ORDER BY invoice_id
    """)

    invoices = cursor.fetchall()

    if invoices:
        for row in invoices:
            print(dict(row))
    else:
        print("⚠️ No invoices found.")

    # -------------------------------------------------
    # 5. Invoice IDs required by Tasks
    # -------------------------------------------------
    print("\n========== INVOICE IDs REQUIRED BY TASKS ==========")

    cursor.execute("""
        SELECT DISTINCT invoice_id
        FROM tasks
        WHERE invoice_id IS NOT NULL
        ORDER BY invoice_id
    """)

    task_invoice_ids = cursor.fetchall()

    for row in task_invoice_ids:
        print(row["invoice_id"])

    # -------------------------------------------------
    # 6. Invoice IDs required by Disputes
    # -------------------------------------------------
    print("\n========== INVOICE IDs REQUIRED BY DISPUTES ==========")

    cursor.execute("""
        SELECT DISTINCT invoice_id
        FROM disputes
        WHERE invoice_id IS NOT NULL
        ORDER BY invoice_id
    """)

    dispute_invoice_ids = cursor.fetchall()

    for row in dispute_invoice_ids:
        print(row["invoice_id"])

    connection.close()

    print("\n" + "=" * 70)
    print("CHECK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    check_dependencies()