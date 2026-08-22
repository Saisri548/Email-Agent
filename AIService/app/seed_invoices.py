from datetime import datetime
from app.database import get_connection


INVOICES = [
    ("INV-4418", "email_011", "Acme Retail", 5200.00, "USD"),
    ("SL-2088", "email_012", "Silverline", 3100.00, "USD"),
    ("DS-774", "email_013", "DevSource", 4500.00, "USD"),
    ("PW-5530", "email_015", "PixelWorks", 2800.00, "USD"),
    ("INV-9811", "email_016", "Eastern Traders", 6200.00, "USD"),
    ("NT-1207", "email_017", "NovaTek", 3900.00, "USD"),
    ("6688", "email_019", "DataServe", 2100.00, "USD"),
    ("AE-4430", "email_020", "Atlas Engineering", 7100.00, "USD"),

    ("INV-7777", "email_021", "XYZ", 4800.00, "USD"),
    ("MS-771", "email_022", "MediaSource", 650.00, "USD"),
    ("OC-4401", "email_024", "Oak Consulting", 9000.00, "USD"),
    ("INV-882", "email_028", "WestBridge", 3500.00, "USD"),
]


def seed_invoices():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        for invoice_id, email_id, vendor, amount, currency in INVOICES:

            cursor.execute(
                """
                INSERT OR IGNORE INTO invoices
                (
                    invoice_id,
                    email_id,
                    vendor,
                    amount,
                    currency,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    invoice_id,
                    email_id,
                    vendor,
                    amount,
                    currency,
                    "EXISTING",
                    datetime.now().isoformat()
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    print("Existing invoices seeded successfully.")


if __name__ == "__main__":
    seed_invoices()