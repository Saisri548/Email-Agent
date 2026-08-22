from database import get_connection

connection = get_connection()

queries = {
    "Invoices → Emails": """
        SELECT *
        FROM invoices
        WHERE email_id IS NOT NULL
        AND email_id NOT IN (
            SELECT email_id FROM emails
        );
    """,

    "Tasks → Emails": """
        SELECT *
        FROM tasks
        WHERE email_id IS NOT NULL
        AND email_id NOT IN (
            SELECT email_id FROM emails
        );
    """,

    "Tasks → Invoices": """
        SELECT *
        FROM tasks
        WHERE invoice_id IS NOT NULL
        AND invoice_id NOT IN (
            SELECT invoice_id FROM invoices
        );
    """,

    "Disputes → Emails": """
        SELECT *
        FROM disputes
        WHERE email_id IS NOT NULL
        AND email_id NOT IN (
            SELECT email_id FROM emails
        );
    """,

    "Disputes → Invoices": """
        SELECT *
        FROM disputes
        WHERE invoice_id IS NOT NULL
        AND invoice_id NOT IN (
            SELECT invoice_id FROM invoices
        );
    """,

    "Audit → Emails": """
        SELECT *
        FROM audit_logs
        WHERE email_id IS NOT NULL
        AND email_id NOT IN (
            SELECT email_id FROM emails
        );
    """
}

for name, query in queries.items():
    rows = connection.execute(query).fetchall()

    print(f"\n{name}")

    if rows:
        print("❌ Orphan records found:")
        for row in rows:
            print(dict(row))
    else:
        print("✅ No orphan records")

connection.close()